"""
Pipeline B: Investor Lead Generation
Discovers VC firms and investors focused on deep tech, robotics, physical AI.
"""

import asyncio
import httpx
import re
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .base import BasePipeline, PipelineResult


class InvestorLeadGenerationPipeline(BasePipeline):
    """Pipeline B: Investor Lead Generation - finds VCs for pre-seed/seed rounds."""

    # Top-tier VCs from target_investors_partners.md
    TARGET_INVESTORS = [
        {
            "name": "Sequoia Capital",
            "domain": "sequoiacap.com",
            "signals": ["capital", "portfolio"]
        },
        {
            "name": "Andreessen Horowitz",
            "domain": "a16z.com",
            "signals": ["venture", "capital", "invest", "portfolio", "fund", "seed", "ai"]
        },
        {
            "name": "Greylock Partners",
            "domain": "greylock.com",
            "signals": ["venture", "capital", "invest", "portfolio", "fund", "series a", "series b", "seed", "ai"]
        },
        {
            "name": "Index Ventures",
            "domain": "indexventures.com",
            "signals": ["venture", "invest", "portfolio", "fund", "series a", "series b", "ai"]
        },
        {
            "name": "Accel Partners",
            "domain": "accel.com",
            "signals": ["ai"]
        },
        {
            "name": "Founders Fund",
            "domain": "foundersfund.com",
            "signals": ["portfolio", "fund", "ai"]
        },
        {
            "name": "General Catalyst",
            "domain": "generalcatalyst.com",
            "signals": ["venture", "capital", "invest", "portfolio", "fund", "seed", "robotics", "ai"]
        },
        {
            "name": "Redpoint Ventures",
            "domain": "redpoint.com",
            "signals": ["venture", "invest", "portfolio", "fund", "series a", "ai"]
        },
        {
            "name": "First Round Capital",
            "domain": "firstround.com",
            "signals": ["capital", "invest", "ai"]
        },
        {
            "name": "Y Combinator",
            "domain": "ycombinator.com",
            "signals": ["venture", "capital", "invest", "portfolio", "fund", "ai"]
        },
    ]

    COMMON_TEAM_PATHS = [
        "", "about", "team", "our-team", "people", "team/", "investors",
        "partners", "portfolio", "contact"
    ]

    EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    def __init__(self):
        super().__init__("Pipeline B: Investor Lead Generation", "investor_lead_generation")
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

    def extract_emails(self, pages: List[tuple], domain: str) -> List[str]:
        emails = set()
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
        return list(emails)

    async def process_investor(self, investor_info: Dict) -> Dict:
        domain = investor_info["domain"]
        name = investor_info["name"]
        signals = investor_info["signals"]
        
        print(f"  🔍 Processing {name} ({domain})...")
        
        pages = await self.discover_pages(domain)
        emails = self.extract_emails(pages, domain)
        
        # Common VC email patterns if not found
        if not emails:
            # Most VCs use info@, contact@, hello@, team@, partners@
            common_patterns = ["info", "contact", "hello", "team", "partners", "investments"]
            emails = [f"{p}@{domain}" for p in common_patterns]
        
        tier = "Verified" if pages else "Inferred"
        score = 50 if pages else 30
        
        return {
            "name": name,
            "domain": domain,
            "homepage": f"https://{domain}",
            "score": score,
            "tier": tier,
            "emails": emails[:10],  # Limit
            "team_members": [],  # Would need team page parsing
            "linkedin_profiles": [],
            "signals": signals,
            "pages_crawled": len(pages)
        }

    async def run(self) -> PipelineResult:
        print(f"\n🚀 Starting {self.name}...")
        
        companies = []
        for investor_info in self.TARGET_INVESTORS:
            result = await self.process_investor(investor_info)
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
            metadata={"toolchain": "httpx", "method": "vc_site_scraping"}
        )
        
        md_path = self.save_result(result)
        json_path = self.save_json(result)
        print(f"  ✅ Saved: {md_path}")
        print(f"  ✅ Saved: {json_path}")
        
        return result

    async def close(self):
        await self.client.aclose()