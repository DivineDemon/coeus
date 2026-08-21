"""
Pipeline D: Competitor Discovery
Discovers and analyzes competitors in the robotics/physical AI space.
Focus: SEO scores, content quality, keyword analysis.
"""

import asyncio
import httpx
import re
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .base import BasePipeline, PipelineResult


class CompetitorDiscoveryPipeline(BasePipeline):
    """Pipeline D: Competitor Discovery - SEO and content analysis."""

    COMPETITORS = [
        {
            "name": "Agility Robotics",
            "domain": "agilityrobotics.com",
            "signals": ["robotics", "automation", "humanoid", "manipulation", "physical ai", "autonomous", "control", "planning", "ros", "nvidia"]
        },
        {
            "name": "Locus Robotics",
            "domain": "locusrobotics.com",
            "signals": ["robotics", "automation", "manipulation", "physical ai", "autonomous", "control", "ros", "ai", "amr", "mobile robot"]
        },
        {
            "name": "Anybotics",
            "domain": "anybotics.com",
            "signals": ["robotics", "automation", "manipulation", "locomotion", "autonomous", "perception", "control", "planning", "reinforcement learning", "data collection"]
        },
        {
            "name": "Picknik",
            "domain": "picknik.ai",
            "signals": ["robotics", "automation", "humanoid", "manipulation", "physical ai", "autonomous", "perception", "control", "planning", "teleoperation"]
        },
        {
            "name": "1X Technologies",
            "domain": "1x.tech",
            "signals": ["robotics", "humanoid", "autonomous", "control", "reinforcement learning", "teleoperation", "data collection", "simulation", "ros", "nvidia"]
        },
        {
            "name": "Universal Robots",
            "domain": "universal-robots.com",
            "signals": ["robotics", "automation", "physical ai", "ros", "nvidia", "unity", "ai", "cobot", "collaborative robot"]
        },
        {
            "name": "Flexiv",
            "domain": "flexiv.com",
            "signals": ["robotics", "automation", "physical ai", "control", "unity", "ai"]
        },
        {
            "name": "Siemens",
            "domain": "siemens.com",
            "signals": ["robotics", "automation", "control", "planning", "simulation", "ros", "ai"]
        },
        {
            "name": "Figure",
            "domain": "figure.ai",
            "signals": ["humanoid", "autonomous", "ros", "unity", "ai"]
        },
    ]

    PAGES_TO_CRAWL = [
        "", "about", "technology", "products", "solutions", "platform",
        "robotics", "automation", "ai", "research", "blog", "news"
    ]

    def __init__(self):
        super().__init__("Pipeline D: Competitor Discovery", "competitor_discovery")
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

    def analyze_seo(self, html: str, domain: str) -> Dict:
        """Analyze SEO metrics from HTML."""
        soup = BeautifulSoup(html, "html.parser")
        
        # Title
        title = soup.title.string.strip() if soup.title else ""
        
        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc.get("content", "") if meta_desc else ""
        
        # H1 tags
        h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]
        
        # Content length
        text_content = soup.get_text(" ", strip=True)
        content_length = len(text_content)
        
        # Keywords in content (from signals)
        # This is simplified - real version would use NLP
        
        # Links
        internal_links = len([a for a in soup.find_all("a", href=True) if domain in a["href"]])
        external_links = len([a for a in soup.find_all("a", href=True) if domain not in a["href"] and a["href"].startswith("http")])
        
        # Images with alt
        images = soup.find_all("img")
        images_with_alt = sum(1 for img in images if img.get("alt"))
        
        # SEO Score (simplified heuristic)
        score = 0
        if title: score += 20
        if description: score += 15
        if h1_tags: score += 15
        if content_length > 5000: score += 20
        if content_length > 20000: score += 10
        if images_with_alt / max(len(images), 1) > 0.5: score += 10
        if internal_links > 5: score += 10
        
        return {
            "title": title,
            "description": description,
            "h1_tags": h1_tags[:5],
            "content_length": content_length,
            "internal_links": internal_links,
            "external_links": external_links,
            "images_total": len(images),
            "images_with_alt": images_with_alt,
            "seo_score": min(score, 100)
        }

    def extract_keywords(self, text: str, target_keywords: List[str]) -> List[str]:
        """Extract target keywords found in text."""
        text_lower = text.lower()
        found = [kw for kw in target_keywords if kw.lower() in text_lower]
        return found

    async def process_competitor(self, competitor_info: Dict) -> Dict:
        domain = competitor_info["domain"]
        name = competitor_info["name"]
        signals = competitor_info["signals"]
        
        print(f"  🔍 Analyzing {name} ({domain})...")
        
        all_content = ""
        pages_analyzed = 0
        total_content_length = 0
        seo_scores = []
        all_keywords = set()
        
        for path in self.PAGES_TO_CRAWL:
            url = urljoin(f"https://{domain}/", path)
            html = await self.fetch_page(url)
            if html:
                pages_analyzed += 1
                seo = self.analyze_seo(html, domain)
                seo_scores.append(seo["seo_score"])
                total_content_length += seo["content_length"]
                all_content += " " + html
                keywords = self.extract_keywords(html, signals)
                all_keywords.update(keywords)
                await asyncio.sleep(0.2)
        
        avg_seo = sum(seo_scores) / len(seo_scores) if seo_scores else 0
        
        # Social platforms (simplified detection)
        social = {}
        for platform in ["linkedin", "twitter", "x", "instagram", "youtube", "github", "facebook"]:
            if platform in all_content.lower():
                social[platform] = 1
        
        return {
            "name": name,
            "domain": domain,
            "homepage": f"https://{domain}",
            "seo_score": round(avg_seo),
            "content_quality": "high" if total_content_length > 50000 else "medium" if total_content_length > 10000 else "low",
            "pages_analyzed": pages_analyzed,
            "total_content_length": total_content_length,
            "top_keywords": list(all_keywords)[:10],
            "social_platforms": social,
            "team_members_found": 0,  # Would need team page parsing
            "signals": signals
        }

    async def run(self) -> PipelineResult:
        print(f"\n🚀 Starting {self.name}...")
        
        companies = []
        for comp_info in self.COMPETITORS:
            result = await self.process_competitor(comp_info)
            companies.append(result)
            await asyncio.sleep(0.5)
        
        total_analyzed = len(companies)
        avg_seo = sum(c["seo_score"] for c in companies) / total_analyzed if total_analyzed else 0
        total_team = sum(c.get("team_members_found", 0) for c in companies)
        with_social = sum(1 for c in companies if c.get("social_platforms"))
        
        result = PipelineResult(
            pipeline_name=self.name,
            pipeline_type=self.pipeline_type,
            timestamp=self.timestamp,
            status="success",
            total_processed=total_analyzed,
            with_emails=with_social,  # Reuse field for "with social"
            verified=sum(1 for c in companies if c["seo_score"] > 80),
            inferred=sum(1 for c in companies if c["seo_score"] <= 80),
            total_emails=0,
            companies=companies,
            metadata={
                "toolchain": "httpx", 
                "method": "seo_content_analysis",
                "avg_seo_score": round(avg_seo),
                "total_team_members": total_team,
                "competitors_with_social": with_social
            }
        )
        
        md_path = self.save_result(result)
        json_path = self.save_json(result)
        print(f"  ✅ Saved: {md_path}")
        print(f"  ✅ Saved: {json_path}")
        
        return result

    async def close(self):
        await self.client.aclose()