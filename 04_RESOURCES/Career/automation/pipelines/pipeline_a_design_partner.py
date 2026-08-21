"""
Pipeline A: Design Partner Discovery
Discovers robotics/physical AI companies that would PAY for physics verification (paid pilots).
Priority: companies already using MuJoCo/Isaac/robosuite/sim-to-real.
"""

import asyncio
import httpx
import re
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from .base import BasePipeline, PipelineResult


class DesignPartnerDiscoveryPipeline(BasePipeline):
    """Pipeline A: Design Partner Discovery - finds robotics companies for paid pilots."""

    # Target companies using simulation/robotics (from target_investors_partners.md Tier 4)
    TARGET_COMPANIES = [
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
    ]

    COMMON_TEAM_PATHS = [
        "", "about", "about-us", "team", "our-team", "leadership",
        "people", "company", "contact", "meet-the-team", "staff"
    ]

    EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    def __init__(self):
        super().__init__("Pipeline A: Design Partner Discovery", "design_partner_discovery")
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; HagaBot/1.0; +https://haga.mushoodhanif.com/bot)"},
            follow_redirects=True
        )

    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a web page with error handling."""
        try:
            response = await self.client.get(url)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(f"  ⚠️  Failed to fetch {url}: {e}")
        return None

    async def discover_pages(self, domain: str) -> List[tuple]:
        """Discover team/contact pages for a domain."""
        base = f"https://{domain}"
        pages = []
        for path in self.COMMON_TEAM_PATHS:
            url = urljoin(base + "/", path)
            html = await self.fetch_page(url)
            if html:
                pages.append((url, html))
        return pages

    def extract_emails_and_names(self, pages: List[tuple], domain: str) -> List[Dict]:
        """Extract email/name pairs from pages."""
        pairs = []
        for url, html in pages:
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(" ", strip=True)
            emails = {e for e in self.EMAIL_RE.findall(text) if e.lower().endswith("@" + domain.lower())}
            
            # Check mailto links first (usually near names)
            for a in soup.find_all("a", href=True):
                if a["href"].lower().startswith("mailto:"):
                    email = a["href"].split(":", 1)[1].split("?")[0].strip()
                    if email.lower().endswith("@" + domain.lower()):
                        name = a.get_text(strip=True) or (a.parent.get_text(" ", strip=True) if a.parent else "")
                        name = self._clean_name(name)
                        if name:
                            pairs.append({"name": name, "email": email, "source_url": url})
                        emails.discard(email)
            
            # Fallback: emails without names
            for email in emails:
                pairs.append({"name": "", "email": email, "source_url": url})
        
        return pairs

    def _clean_name(self, raw: str) -> str:
        raw = re.sub(r"[^A-Za-z\s\-']", "", raw).strip()
        parts = raw.split()
        return " ".join(parts[:2]) if len(parts) >= 2 else ""

    async def process_company(self, company_info: Dict) -> Dict:
        """Process a single company - fetch pages, extract contacts."""
        domain = company_info["domain"]
        name = company_info["name"]
        signals = company_info["signals"]
        
        print(f"  🔍 Processing {name} ({domain})...")
        
        pages = await self.discover_pages(domain)
        if not pages:
            return {
                "name": name,
                "domain": domain,
                "homepage": f"https://{domain}",
                "score": 0,
                "tier": "Unconfirmed",
                "emails": [],
                "team_members": [],
                "linkedin_profiles": [],
                "signals": signals,
                "pages_crawled": 0
            }
        
        pairs = self.extract_emails_and_names(pages, domain)
        
        # Deduplicate emails
        seen_emails = set()
        unique_emails = []
        team_members = []
        for pair in pairs:
            if pair["email"] not in seen_emails:
                seen_emails.add(pair["email"])
                unique_emails.append(pair["email"])
            if pair["name"]:
                team_members.append(pair["name"])
        
        # Determine tier
        if unique_emails:
            tier = "Verified"
            score = 90
        elif team_members:
            tier = "Probable"
            score = 60
        else:
            tier = "Unconfirmed"
            score = 30
        
        return {
            "name": name,
            "domain": domain,
            "homepage": f"https://{domain}",
            "score": score,
            "tier": tier,
            "emails": unique_emails,
            "team_members": team_members[:10],  # Limit
            "linkedin_profiles": [],  # Would need LinkedIn scraping
            "signals": signals,
            "pages_crawled": len(pages)
        }

    async def run(self) -> PipelineResult:
        """Run the design partner discovery pipeline."""
        print(f"\n🚀 Starting {self.name}...")
        
        companies = []
        for company_info in self.TARGET_COMPANIES:
            result = await self.process_company(company_info)
            companies.append(result)
            await asyncio.sleep(1)  # Be polite
        
        # Calculate summary metrics
        total_processed = len(companies)
        with_emails = sum(1 for c in companies if c["emails"])
        verified = sum(1 for c in companies if c["tier"] == "Verified")
        inferred = sum(1 for c in companies if c["tier"] == "Probable")
        total_emails = sum(len(c["emails"]) for c in companies)
        
        result = PipelineResult(
            pipeline_name=self.name,
            pipeline_type=self.pipeline_type,
            timestamp=self.timestamp,
            status="success" if with_emails > 0 else "partial",
            total_processed=total_processed,
            with_emails=with_emails,
            verified=verified,
            inferred=inferred,
            total_emails=total_emails,
            companies=companies,
            metadata={"toolchain": "httpx", "method": "team_page_scraping"}
        )
        
        # Save outputs
        md_path = self.save_result(result)
        json_path = self.save_json(result)
        print(f"  ✅ Saved: {md_path}")
        print(f"  ✅ Saved: {json_path}")
        
        return result

    async def close(self):
        await self.client.aclose()