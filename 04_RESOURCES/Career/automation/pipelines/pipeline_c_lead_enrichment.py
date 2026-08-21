"""
Pipeline C: Lead Enrichment
Enriches previously discovered leads with additional contact info and team details.
"""

import asyncio
import httpx
import re
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .base import BasePipeline, PipelineResult


class LeadEnrichmentPipeline(BasePipeline):
    """Pipeline C: Lead Enrichment - enriches companies with more contact data."""

    # Companies to enrich (from previous pipeline results)
    COMPANIES_TO_ENRICH = [
        {
            "name": "Figure",
            "domain": "figure.ai",
            "signals": ["humanoid"]
        },
        {
            "name": "Agility Robotics",
            "domain": "agilityrobotics.com",
            "signals": ["robotics", "automation", "physical ai", "humanoid", "manipulation", "amr"]
        },
        {
            "name": "Locus Robotics",
            "domain": "locusrobotics.com",
            "signals": ["robotics", "automation", "physical ai", "amr", "mobile robot"]
        },
        {
            "name": "Anybotics",
            "domain": "anybotics.com",
            "signals": ["robotics", "automation", "manipulation", "locomotion", "mobile robot"]
        },
        {
            "name": "Siemens",
            "domain": "siemens.com",
            "signals": ["robotics", "automation"]
        },
        {
            "name": "Picknik Robotics",
            "domain": "picknik.ai",
            "signals": ["robotics", "automation", "physical ai", "humanoid", "manipulation", "amr"]
        },
        {
            "name": "Universal Robots",
            "domain": "universal-robots.com",
            "signals": ["robotics", "automation", "physical ai", "cobot", "collaborative robot"]
        },
        {
            "name": "Flexiv",
            "domain": "flexiv.com",
            "signals": ["robotics", "automation", "physical ai"]
        },
    ]

    COMMON_TEAM_PATHS = [
        "", "about", "about-us", "team", "our-team", "leadership",
        "people", "company", "contact", "meet-the-team", "staff"
    ]

    EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    def __init__(self):
        super().__init__("Pipeline C: Lead Enrichment", "lead_enrichment")
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; HagaBot/1.0; +https://haga.mushoodhanif.com/bot)"},
            follow_redirects=True
        )

    async def fetch_page(self, url: str) -> Optional[str]:
        try:
            response = await self.client.get(url)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(f"  ⚠️  Failed to fetch {url}: {e}")
        return None

    async def discover_pages(self, domain: str) -> List[tuple]:
        base = f"https://{domain}"
        pages = []
        for path in self.COMMON_TEAM_PATHS:
            url = urljoin(base + "/", path)
            html = await self.fetch_page(url)
            if html:
                pages.append((url, html))
        return pages

    def extract_emails_and_team(self, pages: List[tuple], domain: str) -> tuple:
        emails = set()
        team_members = []
        
        for url, html in pages:
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(" ", strip=True)
            found = {e for e in self.EMAIL_RE.findall(text) if e.lower().endswith("@" + domain.lower())}
            emails.update(found)
            
            for a in soup.find_all("a", href=True):
                if a["href"].lower().startswith("mailto:"):
                    email = a["href"].split(":", 1)[1].split("?")[0].strip()
                    if email.lower().endswith("@" + domain.lower()):
                        emails.add(email)
            
            # Extract team member names from common patterns
            for tag in soup.find_all(["h2", "h3", "h4", "p", "div", "span"]):
                text = tag.get_text(strip=True)
                if text and len(text) < 100 and re.search(r"(CEO|CTO|VP|Director|Manager|Founder|Lead|Head)", text, re.I):
                    team_members.append(text)
        
        return list(emails), team_members[:15]

    async def process_company(self, company_info: Dict) -> Dict:
        domain = company_info["domain"]
        name = company_info["name"]
        signals = company_info["signals"]
        
        print(f"  🔍 Enriching {name} ({domain})...")
        
        pages = await self.discover_pages(domain)
        emails, team_members = self.extract_emails_and_team(pages, domain)
        
        # Generate common email patterns if none found
        if not emails:
            common = ["info", "contact", "hello", "team", "business", "sales", "partnerships"]
            emails = [f"{c}@{domain}" for c in common]
            tier = "Inferred"
            score = 75
        elif team_members:
            tier = "Verified"
            score = 75
        else:
            tier = "Verified"
            score = 50
        
        return {
            "name": name,
            "domain": domain,
            "homepage": f"https://{domain}",
            "score": score,
            "tier": tier,
            "emails": emails[:10],
            "team_members": team_members,
            "linkedin_profiles": [],
            "signals": signals,
            "pages_crawled": len(pages)
        }

    async def run(self) -> PipelineResult:
        print(f"\n🚀 Starting {self.name}...")
        
        companies = []
        for company_info in self.COMPANIES_TO_ENRICH:
            result = await self.process_company(company_info)
            companies.append(result)
            await asyncio.sleep(0.5)
        
        total_processed = len(companies)
        with_emails = sum(1 for c in companies if c["emails"])
        verified = sum(1 for c in companies if c["tier"] == "Verified")
        inferred = sum(1 for c in companies if c["tier"] == "Inferred")
        total_emails = sum(len(c["emails"]) for c in companies)
        
        result = PipelineResult(
            pipeline_name=self.name,
            pipeline_type=self.pipeline_type,
            timestamp=self.timestamp,
            status="success",
            total_processed=total_processed,
            with_emails=with_emails,
            verified=verified,
            inferred=inferred,
            total_emails=total_emails,
            companies=companies,
            metadata={"toolchain": "httpx", "method": "enrichment_scraping"}
        )
        
        md_path = self.save_result(result)
        json_path = self.save_json(result)
        print(f"  ✅ Saved: {md_path}")
        print(f"  ✅ Saved: {json_path}")
        
        return result

    async def close(self):
        await self.client.aclose()