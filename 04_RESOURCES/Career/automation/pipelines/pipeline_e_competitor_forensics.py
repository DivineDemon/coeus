"""
Pipeline E: Competitor Forensics
Deep competitor analysis - detailed crawling, team extraction, email discovery, differentiator identification.
"""

import asyncio
import httpx
import re
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .base import BasePipeline, PipelineResult


class CompetitorForensicsPipeline(BasePipeline):
    """Pipeline E: Competitor Forensics - deep competitive intelligence."""

    COMPETITORS = [
        {
            "name": "Agility Robotics",
            "domain": "agilityrobotics.com",
            "signals": ["robotics", "automation", "humanoid", "manipulation", "physical ai", "autonomous", "control", "planning", "ros", "nvidia"]
        },
        {
            "name": "Locus Robotics",
            "domain": "locusrobotics.com",
            "signals": ["robotics", "automation", "manipulation", "physical ai", "autonomous", "perception", "control", "ros", "ai", "amr"]
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
            "name": "Universal Robots",
            "domain": "universal-robots.com",
            "signals": ["robotics", "automation", "humanoid", "physical ai", "control", "planning", "imitation learning", "ros", "nvidia", "unity"]
        },
        {
            "name": "1X Technologies",
            "domain": "1x.tech",
            "signals": ["robotics", "humanoid", "autonomous", "control", "reinforcement learning", "teleoperation", "data collection", "simulation", "ros", "nvidia"]
        },
        {
            "name": "Flexiv",
            "domain": "flexiv.com",
            "signals": ["robotics", "automation", "physical ai", "control", "simulation", "ros", "nvidia", "unity", "ai"]
        },
        {
            "name": "Siemens",
            "domain": "siemens.com",
            "signals": ["robotics", "automation", "control", "planning", "simulation", "ros", "ai"]
        },
        {
            "name": "Figure",
            "domain": "figure.ai",
            "signals": ["humanoid", "autonomous", "control", "reinforcement learning", "ros", "unity", "ai"]
        },
    ]

    DEEP_CRAWL_PATHS = [
        "", "about", "about-us", "team", "our-team", "leadership", "people",
        "technology", "products", "solutions", "platform", "robotics", "automation",
        "ai", "research", "blog", "news", "careers", "jobs", "press", "media",
        "partners", "customers", "case-studies", "resources", "whitepapers"
    ]

    EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    def __init__(self):
        super().__init__("Pipeline E: Competitor Forensics", "competitor_forensics")
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

    def analyze_page(self, html: str, domain: str) -> Dict:
        soup = BeautifulSoup(html, "html.parser")
        
        # Title
        title = soup.title.string.strip() if soup.title else ""
        
        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc.get("content", "") if meta_desc else ""
        
        # All headings
        headings = {}
        for level in range(1, 7):
            headings[f"h{level}"] = [h.get_text(strip=True) for h in soup.find_all(f"h{level}")]
        
        # Content
        text_content = soup.get_text(" ", strip=True)
        content_length = len(text_content)
        
        # Links
        internal_links = len([a for a in soup.find_all("a", href=True) if domain in a["href"]])
        external_links = len([a for a in soup.find_all("a", href=True) if domain not in a["href"] and a["href"].startswith("http")])
        
        # Images
        images = soup.find_all("img")
        images_with_alt = sum(1 for img in images if img.get("alt"))
        
        return {
            "title": title,
            "description": description,
            "headings": headings,
            "content_length": content_length,
            "internal_links": internal_links,
            "external_links": external_links,
            "images_total": len(images),
            "images_with_alt": images_with_alt,
        }

    def extract_emails(self, html: str, domain: str) -> List[str]:
        soup = BeautifulSoup(html, "html.parser")
        emails = set()
        
        text = soup.get_text(" ", strip=True)
        found = {e for e in self.EMAIL_RE.findall(text) if e.lower().endswith("@" + domain.lower())}
        emails.update(found)
        
        for a in soup.find_all("a", href=True):
            if a["href"].lower().startswith("mailto:"):
                email = a["href"].split(":", 1)[1].split("?")[0].strip()
                if email.lower().endswith("@" + domain.lower()):
                    emails.add(email)
        
        return list(emails)

    def extract_team_members(self, html: str) -> List[str]:
        soup = BeautifulSoup(html, "html.parser")
        members = []
        
        # Look for team member patterns
        for tag in soup.find_all(["h2", "h3", "h4", "p", "div", "span", "li"]):
            text = tag.get_text(strip=True)
            if text and 5 < len(text) < 100:
                # Check for title patterns
                if re.search(r"(CEO|CTO|CFO|COO|VP|Vice President|Director|Manager|Founder|Co-Founder|Lead|Head of|Chief|President|Partner)", text, re.I):
                    members.append(text)
        
        return list(set(members))[:20]

    def extract_social_profiles(self, html: str) -> Dict[str, int]:
        social = {}
        platforms = ["linkedin.com", "twitter.com", "x.com", "instagram.com", "youtube.com", "github.com", "facebook.com"]
        for platform in platforms:
            count = html.lower().count(platform)
            if count > 0:
                social[platform.split(".")[0]] = count
        return social

    def calculate_seo_score(self, analysis: Dict) -> int:
        score = 0
        if analysis["title"]: score += 15
        if analysis["description"]: score += 10
        if analysis["headings"]["h1"]: score += 10
        if analysis["content_length"] > 10000: score += 25
        elif analysis["content_length"] > 5000: score += 15
        elif analysis["content_length"] > 1000: score += 10
        if analysis["images_with_alt"] / max(analysis["images_total"], 1) > 0.5: score += 10
        if analysis["internal_links"] > 10: score += 10
        if analysis["headings"]["h2"]: score += 10
        if analysis["headings"]["h3"]: score += 10
        return min(score, 100)

    def identify_strengths_weaknesses(self, analysis: Dict, emails: List[str], social: Dict, team: List[str]) -> tuple:
        strengths = []
        weaknesses = []
        
        content_length = analysis.get("content_length", 0)
        if content_length > 50000:
            strengths.append("Detailed content")
        elif content_length < 5000:
            weaknesses.append("Thin content")
        
        if analysis.get("headings", {}).get("h1"):
            strengths.append("Proper heading structure")
        else:
            weaknesses.append("Missing H1")
        
        images_with_alt = analysis.get("images_with_alt", 0)
        images_total = analysis.get("images_total", 1)
        if images_with_alt / max(images_total, 1) > 0.7:
            strengths.append("Good image accessibility")
        elif images_total > 0:
            weaknesses.append("Missing alt text on images")
        
        if social:
            strengths.append("Active social presence")
        else:
            weaknesses.append("Limited social presence")
        
        if emails:
            strengths.append("Visible contact emails")
        else:
            weaknesses.append("No visible emails")
        
        if team:
            strengths.append("Team information available")
        else:
            weaknesses.append("No team info extracted")
        
        return strengths, weaknesses

    def identify_differentiators(self, signals: List[str], all_signals: List[str]) -> List[str]:
        # Find signals unique to this competitor vs others
        all_other = set()
        for s in all_signals:
            all_other.update(s)
        unique = set(signals) - (all_other - set(signals))
        return list(unique)[:5]

    async def process_competitor(self, competitor_info: Dict, all_signals: List[List[str]]) -> Dict:
        domain = competitor_info["domain"]
        name = competitor_info["name"]
        signals = competitor_info["signals"]
        
        print(f"  🔍 Deep forensics on {name} ({domain})...")
        
        all_content = ""
        pages_crawled = 0
        total_content = 0
        seo_scores = []
        all_emails = set()
        all_team = []
        all_social = {}
        all_keywords = set()
        
        for path in self.DEEP_CRAWL_PATHS:
            url = urljoin(f"https://{domain}/", path)
            html = await self.fetch_page(url)
            if html:
                pages_crawled += 1
                analysis = self.analyze_page(html, domain)
                seo_scores.append(self.calculate_seo_score(analysis))
                total_content += analysis["content_length"]
                all_content += " " + html
                
                emails = self.extract_emails(html, domain)
                all_emails.update(emails)
                
                team = self.extract_team_members(html)
                all_team.extend(team)
                
                social = self.extract_social_profiles(html)
                for k, v in social.items():
                    all_social[k] = all_social.get(k, 0) + v
                
                keywords = [kw for kw in signals if kw.lower() in html.lower()]
                all_keywords.update(keywords)
                
                await asyncio.sleep(0.1)
        
        avg_seo = sum(seo_scores) / len(seo_scores) if seo_scores else 0
        
        # Final analysis of homepage for strengths/weaknesses
        homepage_html = await self.fetch_page(f"https://{domain}/")
        final_analysis = self.analyze_page(homepage_html, domain) if homepage_html else {}
        
        strengths, weaknesses = self.identify_strengths_weaknesses(
            final_analysis, list(all_emails), all_social, all_team
        )
        
        differentiators = self.identify_differentiators(signals, all_signals)
        
        return {
            "name": name,
            "domain": domain,
            "homepage": f"https://{domain}",
            "seo_score": round(avg_seo),
            "pages_crawled": pages_crawled,
            "total_content": total_content,
            "top_keywords": list(all_keywords)[:10],
            "social_platforms": all_social,
            "team_members_found": len(all_team),
            "team_members": all_team[:10],
            "emails_found": list(all_emails)[:5],
            "strengths": strengths,
            "weaknesses": weaknesses,
            "differentiators": differentiators,
            "market_position": "Active in robotics/physical AI" if avg_seo > 50 else "Limited online presence",
            "signals": signals
        }

    async def run(self) -> PipelineResult:
        print(f"\n🚀 Starting {self.name}...")
        
        all_signals = [c["signals"] for c in self.COMPETITORS]
        
        companies = []
        for comp_info in self.COMPETITORS:
            result = await self.process_competitor(comp_info, all_signals)
            companies.append(result)
            await asyncio.sleep(0.5)
        
        total_analyzed = len(companies)
        avg_seo = sum(c["seo_score"] for c in companies) / total_analyzed if total_analyzed else 0
        total_team = sum(c["team_members_found"] for c in companies)
        with_social = sum(1 for c in companies if c["social_platforms"])
        with_emails = sum(1 for c in companies if c["emails_found"])
        
        result = PipelineResult(
            pipeline_name=self.name,
            pipeline_type=self.pipeline_type,
            timestamp=self.timestamp,
            status="success",
            total_processed=total_analyzed,
            with_emails=with_emails,
            verified=sum(1 for c in companies if c["seo_score"] > 80),
            inferred=sum(1 for c in companies if c["seo_score"] <= 80),
            total_emails=sum(len(c["emails_found"]) for c in companies),
            companies=companies,
            metadata={
                "toolchain": "httpx", 
                "method": "deep_competitive_forensics",
                "avg_seo_score": round(avg_seo),
                "total_team_members": total_team,
                "competitors_with_social": with_social,
                "competitors_with_emails": with_emails
            }
        )
        
        md_path = self.save_result(result)
        json_path = self.save_json(result)
        print(f"  ✅ Saved: {md_path}")
        print(f"  ✅ Saved: {json_path}")
        
        return result

    async def close(self):
        await self.client.aclose()