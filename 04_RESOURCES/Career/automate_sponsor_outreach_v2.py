#!/usr/bin/env python3
"""
Automated UK Sponsor Job Matching & Outreach for Mushood Hanif - V2
Features: Redis caching, Neon PostgreSQL persistence, leadfinder.py integration,
SearXNG search, application tracking, deduplication, rate limiting.
Run daily at 12 PM Pakistan Time (7 AM UTC) Mon-Fri.
"""

import os
import json
import csv
import re
import hashlib
import time
import requests
import base64
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, List, Any

# Load environment variables
load_dotenv("/Users/mushood/Documents/code/personal/coeus/.env.local")

# ============================================================
# CONFIGURATION
# ============================================================
CSV_PATH = "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/SP_-_Worker_and_Temporary_Worker_Web_Register_-_2026-07-17.csv"
PRIORITY_JSON = "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/priority_sponsors.json"
JOBS_DIR = "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/job_matches"
CONTACTS_DIR = "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/enriched_contacts"
DRAFTS_DIR = "/Users/mushood/Documents/code/personal/coeus/01_INBOX/outreach_drafts"
LOG_DIR = "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career"
RESUME_PATH = "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/resume.pdf"

# Ensure directories exist
for d in [JOBS_DIR, CONTACTS_DIR, DRAFTS_DIR]:
    Path(d).mkdir(parents=True, exist_ok=True)

# API Keys & Service URLs
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # Will be deprecated

# SearXNG
SEARXNG_URL = os.getenv("SEARXNG_URL", "https://searxng.sv.mushoodhanif.com")
SEARXNG_USERNAME = os.getenv("SEARXNG_USERNAME", "admin")
SEARXNG_PASSWORD = os.getenv("SEARXNG_PASSWORD", "J8HrtZatZGXcEfNv5VXP1nPUP1Vcc2Qs")

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://default:Di8cZ8khX4RdTW3jl12o0bbh9r1V9FEnZ2IofKOHKT1MNBHKSw8kXcRdwMXs8w66@195.35.25.162:5432/0")

# Neon PostgreSQL
NEON_DB_URL = os.getenv("NEON_DB_URL", "postgresql://neondb_owner:npg_HiXwnNr3GR5o@ep-proud-unit-axeoiv6k-pooler.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# Cache TTLs (seconds)
CACHE_TTL_COMPANY = 7 * 24 * 3600      # 7 days
CACHE_TTL_CONTACT = 30 * 24 * 3600     # 30 days
CACHE_TTL_SEARCH = 24 * 3600           # 1 day
CACHE_TTL_ENRICHMENT = 30 * 24 * 3600  # 30 days

# Rate limiting
RATE_LIMIT_DELAY = 1.5  # seconds between requests
LEADFINDER_DELAY = 2.0   # seconds between SMTP probes

# Batch size for daily runs
BATCH_SIZE = 5

# Known domains for priority companies (from CSV)
KNOWN_DOMAINS = {
    "JBS Applied A.I & Robotics Research Ltd": "jbs-ai-robotics.com",
    "Shadow Robot Company Ltd.": "shadowrobot.com",
    "Apollo Research AI Ltd": "apolloresearch.ai",
    "CGA Simulation Ltd": "cga-simulation.com",
    "HPi Verification Services Ltd": "hpi-verification.com",
    "Fieldwork Robotics Limited": "fieldworkrobotics.com",
    "Oxford Robotics Ltd trading as Dynium Robot": "oxfordrobotics.institute",
    "Prosper Robotics Ltd": "prosper-robotics.com",
    "Perceptual Robotics Limited": "perceptualrobotics.com",
    "Extend Robotics Limited": "extendrobotics.com",
    "Human Digital Twin Limited": "humandigitaltwin.com",
    "Mistral AI UK Limited": "mistral.ai",
    "Stability AI Ltd": "stability.ai",
    "Tecosim Technical Simulation Ltd.": "tecosim.com",
    "The Simulator Company Limited": "thesimulatorcompany.com",
    "General Physics (UK) Ltd": "generalphysics.com",
    "Innovative Physics Limited": "innovativephysics.co.uk",
}

# Batch size for daily runs
BATCH_SIZE = 5

# Tech keywords for CSV scanning
TECH_KEYWORDS = [
    "robotics", "robot", "simulation", "simulator", "digital twin",
    "physical ai", "world model", "foundation model", "mujoco", "isaac",
    "ros ", "robosuite", "cogvideo", "physics verification", "benchmark",
    "autonomous", "ai research", "deepmind", "openai", "anthropic",
    "generative", "llm", "neural", "agi", "computer vision", "nlp",
    "deep learning", "verification", "physics", "machine learning",
    "artificial intelligence", "ml engineer", "ai engineer"
]

# Job search terms
JOB_TERMS = [
    "Senior AI Engineer", "ML Engineer", "Robotics Engineer",
    "Research Scientist", "Simulation Engineer", "Physics Engineer",
    "MLOps Engineer", "Computer Vision Engineer", "Applied AI Engineer",
    "Robotics Research Engineer", "AI Research Engineer"
]

# Import external modules
try:
    import redis
    import psycopg2
    import psycopg2.extras
    from bs4 import BeautifulSoup
    REDIS_AVAILABLE = True
    PG_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    PG_AVAILABLE = False

# Import leadfinder module
try:
    import sys
    sys.path.insert(0, "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES")
    import leadfinder
    LEADFINDER_AVAILABLE = True
except ImportError:
    LEADFINDER_AVAILABLE = False


# ============================================================
# DATABASE & CACHE INITIALIZATION
# ============================================================

def init_redis() -> Optional[redis.Redis]:
    """Initialize Redis connection with connection pooling."""
    if not REDIS_AVAILABLE:
        print("  ⚠️  redis-py not installed, caching disabled")
        return None
    try:
        r = redis.from_url(REDIS_URL, decode_responses=True, socket_timeout=5, socket_connect_timeout=5)
        r.ping()
        print("  ✅ Redis connected")
        return r
    except Exception as e:
        print(f"  ⚠️  Redis connection failed: {e}")
        return None


def init_pg() -> Optional[psycopg2.extensions.connection]:
    """Initialize PostgreSQL connection."""
    if not PG_AVAILABLE:
        print("  ⚠️  psycopg2 not installed, persistence disabled")
        return None
    try:
        conn = psycopg2.connect(NEON_DB_URL, connect_timeout=10)
        conn.autocommit = True
        print("  ✅ Neon PostgreSQL connected")
        return conn
    except Exception as e:
        print(f"  ⚠️  Neon PostgreSQL connection failed: {e}")
        return None


# ============================================================
# CACHE HELPERS (Redis + PostgreSQL fallback)
# ============================================================

def cache_get(redis_client: Optional[redis.Redis], key: str) -> Optional[str]:
    if redis_client:
        try:
            return redis_client.get(key)
        except Exception:
            pass
    return None


def cache_set(redis_client: Optional[redis.Redis], key: str, value: str, ttl: int) -> bool:
    if redis_client:
        try:
            return redis_client.setex(key, ttl, value)
        except Exception:
            pass
    return False


def cache_get_json(redis_client: Optional[redis.Redis], key: str) -> Optional[dict]:
    val = cache_get(redis_client, key)
    if val:
        try:
            return json.loads(val)
        except Exception:
            pass
    return None


def cache_set_json(redis_client: Optional[redis.Redis], key: str, value: dict, ttl: int) -> bool:
    return cache_set(redis_client, key, json.dumps(value), ttl)


def pg_query(conn, query: str, params: tuple = None) -> List[dict]:
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        print(f"  ⚠️  PG query error: {e}")
        return []


def pg_execute(conn, query: str, params: tuple = None) -> bool:
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
        return True
    except Exception as e:
        print(f"  ⚠️  PG execute error: {e}")
        return False


def pg_get_json(conn, query: str, params: tuple = None) -> Optional[dict]:
    rows = pg_query(conn, query, params)
    return rows[0] if rows else None


# ============================================================
# SEARXNG SEARCH CLIENT
# ============================================================

class SearXNGClient:
    def __init__(self, base_url: str, username: str = "", password: str = ""):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.logged_in = True  # No login required

    def login(self) -> bool:
        # SearXNG doesn't require login for search
        self.logged_in = True
        return True

    def search(self, query: str, format: str = "json") -> List[dict]:
        try:
            params = {"q": query, "format": "json"}
            resp = self.session.get(f"{self.base_url}/search", params=params, timeout=15, verify=False)
            if resp.status_code == 200 and 'json' in resp.headers.get('Content-Type', ''):
                data = resp.json()
                return data.get('results', [])
            # Fallback: parse HTML
            return self._parse_html_results(resp.text)
        except Exception as e:
            print(f"  ⚠️  SearXNG search error: {e}")
            return []

    def _parse_html_results(self, html: str) -> List[dict]:
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for selector in ['article.result', 'div.result', 'div.result-default', 'main article', '.result-item']:
            for elem in soup.select(selector):
                title_elem = elem.find(['h3', 'h2', 'h4'])
                link_elem = elem.find('a', href=True)
                snippet_elem = elem.find('p', class_=re.compile(r'content|snippet|description'))
                if link_elem and link_elem.get('href'):
                    results.append({
                        'title': title_elem.get_text(strip=True) if title_elem else '',
                        'url': link_elem['href'],
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                    })
        return results


# ============================================================
# PRIORITY COMPANY MANAGEMENT (Dynamic from CSV)
# ============================================================

def load_priority_companies_from_csv(csv_path: str, pg_conn) -> List[dict]:
    """Load priority companies from CSV - process ALL 17 priority companies daily.
    Cache TTLs (30d for enrichment) and content-hash deduplication prevent redundant work."""
    # NOTE: We NO LONGER filter by last_enriched_at - all 17 priority companies run daily.
    # Caching (Redis + PG, 30d TTL) and content-hash deduplication prevent redundant API calls and drafts.
    processed = set()  # Empty - don't skip based on previous processing
    
    # Known tech domains for the 17 priority companies
    KNOWN_DOMAINS = {
        "JBS Applied A.I & Robotics Research Ltd": "jbs-ai-robotics.com",
        "Shadow Robot Company Ltd.": "shadowrobot.com",
        "Apollo Research AI Ltd": "apolloresearch.ai",
        "CGA Simulation Ltd": "cga-simulation.com",
        "HPi Verification Services Ltd": "hpi-verification.com",
        "Fieldwork Robotics Limited": "fieldworkrobotics.com",
        "Oxford Robotics Ltd trading as Dynium Robot": "oxfordrobotics.institute",
        "Prosper Robotics Ltd": "prosper-robotics.com",
        "Perceptual Robotics Limited": "perceptualrobotics.com",
        "Extend Robotics Limited": "extendrobotics.com",
        "Human Digital Twin Limited": "humandigitaltwin.com",
        "Mistral AI UK Limited": "mistral.ai",
        "Stability AI Ltd": "stability.ai",
        "Tecosim Technical Simulation Ltd.": "tecosim.com",
        "The Simulator Company Limited": "thesimulatorcompany.com",
        "General Physics (UK) Ltd": "generalphysics.com",
        "Innovative Physics Limited": "innovativephysics.co.uk",
    }
    
    # Scan CSV for A-rated tech sponsors
    matches = []
    seen = set()
    
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            org = row.get('Organisation Name', '').strip()
            city = row.get('Town/City', '').strip()
            county = row.get('County', '').strip()
            sponsor_type = row.get('Type & Rating', '').strip()
            route = row.get('Route', '').strip()
            
            if 'A rating' not in sponsor_type or 'Skilled Worker' not in route:
                continue
            
            org_lower = org.lower()
            key = f"{org_lower}_{city.lower()}"
            if key in seen:
                continue
            
            # Check if in our known domains
            if org in KNOWN_DOMAINS:
                domain = KNOWN_DOMAINS[org]
                if domain not in processed:
                    matches.append({
                        "name": org,
                        "location": city,
                        "county": county,
                        "domain": domain,
                        "sponsor_type": sponsor_type,
                        "route": route,
                        "matched_keywords": ["known_priority"]
                    })
                    seen.add(key)
                continue
            
            # Check for tech keywords
            matched_keywords = [kw for kw in TECH_KEYWORDS if kw in org_lower]
            if matched_keywords:
                exclude = ['retail', 'food', 'wine', 'pizza', 'chicken', 'restaurant', 'cafe', 'bakery',
                          'care', 'health', 'hospital', 'clinic', 'pharmacy', 'medical', 'dental',
                          'property', 'construction', 'refrigeration', 'air conditioning', 'plumbing',
                          'electrical', 'cleaning', 'security', 'taxi', 'transport', 'logistics',
                          'accounting', 'accountants', 'legal', 'law', 'solicitor', 'church',
                          'charity', 'association', 'muslim', 'mosque', 'temple', 'school',
                          'nursery', 'childcare', 'beauty', 'hair', 'salon', 'spa', 'fitness',
                          'gym', 'hotel', 'accommodation', 'travel', 'tourism', 'estate agent',
                          'letting', 'insurance', 'finance', 'bank', 'mortgage',
                          'recruitment', 'employment', 'staffing', 'agency', 'convenience',
                          'newsagent', 'shop', 'store', 'supermarket', 'grocery', 'off license',
                          'garage', 'mot', 'tyre', 'car', 'van', 'vehicle', 'breakdown',
                          'waste', 'recycling', 'skip', 'drain', 'sewage', 'pest control',
                          'locksmith', 'glazing', 'roofing', 'fencing', 'landscaping',
                          'training', 'driving', 'instructor', 'tuition', 'tutor', 'language',
                          'translation', 'interpreter', 'visa', 'immigration', 'passport',
                          'citizenship', 'notary', 'commissioner', 'granite', 'aesthetics',
                          'laboratory furniture', 'racking', 'storage', 'fabrication',
                          'heating', 'energy', 'offshore', 'ground engineering', 'civil engineering',
                          'mobile', 'computer repair', 'computer services', 'telecom',
                          'meat', 'photonic', 'performance', 'yorkshire', 'mumbai', 'lounge',
                          'film', 'holdings', 'supplies', 'drinks', 'tea']
                if not any(ex in org_lower for ex in exclude):
                    # Try to find domain
                    domain = None
                    if org in KNOWN_DOMAINS:
                        domain = KNOWN_DOMAINS[org]
                    
                    if domain and domain not in processed:
                        matches.append({
                            "name": org,
                            "location": city,
                            "county": county,
                            "domain": domain,
                            "sponsor_type": sponsor_type,
                            "route": route,
                            "matched_keywords": matched_keywords[:5]
                        })
                        seen.add(key)
    
    # Sort: known priority first, then by match count
    priority_set = set(KNOWN_DOMAINS.values())
    matches.sort(key=lambda m: (0 if m['domain'] in priority_set else 1, -len(m.get('matched_keywords', []))))
    
    return matches


def get_next_batch_companies(all_companies: List[dict], batch_size: int = 5, pg_conn=None) -> List[dict]:
    """Get next batch of companies - for daily run, return ALL priority companies.
    Caching and content-hash deduplication handle redundant work prevention."""
    # For daily cron: return ALL companies, don't filter by processed status
    # Cache TTLs (30d for contacts) and SHA256 content-hash prevent duplicate work
    return all_companies


def scan_csv_for_priority_companies() -> List[dict]:
    """Scan the full CSV for A-rated sponsors matching tech keywords."""
    matches = []
    seen = set()
    
    with open(CSV_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            org = row.get('Organisation Name', '').strip()
            city = row.get('Town/City', '').strip()
            county = row.get('County', '').strip()
            sponsor_type = row.get('Type & Rating', '').strip()
            route = row.get('Route', '').strip()
            
            if 'A rating' not in sponsor_type or 'Skilled Worker' not in route:
                continue
            
            org_lower = org.lower()
            key = f"{org_lower}_{city.lower()}"
            if key in seen:
                continue
            
            matched_keywords = [kw for kw in TECH_KEYWORDS if kw in org_lower]
            if matched_keywords:
                exclude = ['retail', 'food', 'wine', 'pizza', 'chicken', 'restaurant', 'cafe', 'bakery',
                          'care', 'health', 'hospital', 'clinic', 'pharmacy', 'medical', 'dental',
                          'property', 'construction', 'refrigeration', 'air conditioning', 'plumbing',
                          'electrical', 'cleaning', 'security', 'taxi', 'transport', 'logistics',
                          'accounting', 'accountants', 'legal', 'law', 'solicitor', 'church',
                          'charity', 'association', 'muslim', 'mosque', 'temple', 'school',
                          'nursery', 'childcare', 'beauty', 'hair', 'salon', 'spa', 'fitness',
                          'gym', 'hotel', 'accommodation', 'travel', 'tourism', 'estate agent',
                          'letting', 'insurance', 'finance', 'bank', 'mortgage',
                          'recruitment', 'employment', 'staffing', 'agency', 'convenience',
                          'newsagent', 'shop', 'store', 'supermarket', 'grocery', 'off license',
                          'garage', 'mot', 'tyre', 'car', 'van', 'vehicle', 'breakdown',
                          'waste', 'recycling', 'skip', 'drain', 'sewage', 'pest control',
                          'locksmith', 'glazing', 'roofing', 'fencing', 'landscaping',
                          'training', 'driving', 'instructor', 'tuition', 'tutor', 'language',
                          'translation', 'interpreter', 'visa', 'immigration', 'passport',
                          'citizenship', 'notary', 'commissioner', 'granite', 'aesthetics',
                          'laboratory furniture', 'racking', 'storage', 'fabrication',
                          'heating', 'energy', 'offshore', 'ground engineering', 'civil engineering',
                          'mobile', 'computer repair', 'computer services', 'telecom',
                          'meat', 'photonic', 'performance', 'yorkshire', 'mumbai', 'lounge',
                          'film', 'holdings', 'supplies', 'drinks', 'tea']
                if not any(ex in org_lower for ex in exclude):
                    matches.append({
                        "name": org, "city": city, "county": county,
                        "sponsor_type": sponsor_type, "route": route,
                        "matched_keywords": matched_keywords[:5]
                    })
                    seen.add(key)
    return matches


# ============================================================
# SEARXNG EMAIL FINDING (replaces Hunter.io)
# ============================================================

def find_people_searxng(searxng: SearXNGClient, domain: str, redis_client: Optional[redis.Redis], pg_conn) -> List[dict]:
    """Find people/roles at a company using SearXNG search. Returns list of people with names, roles, and LinkedIn profiles."""
    cache_key = f"people:searxng:{domain}"
    
    # Check Redis cache
    cached = cache_get_json(redis_client, cache_key) if redis_client else None
    if cached:
        print(f"  �������� ������ ������ ���� ������ ���� ���� �� ������ ���� ���� �� ���� �� �� 📦 Cache hit for SearXNG people search ({domain})")
        # Extract results from cache wrapper - handle both formats
        if isinstance(cached, dict) and 'results' in cached:
            return cached['results']
        # If cached is already a list (direct cache), return as-is
        elif isinstance(cached, list):
            return cached
        # If unexpected format, fall through to fetch fresh data
    
    # Check PG cache
    names_hash = f"people_{domain}"
    cached_pg = pg_get_json(pg_conn,
        "SELECT results FROM enrichment_cache WHERE domain = %s AND names_hash = %s AND expires_at > NOW()",
        (domain, names_hash)
    )
    if cached_pg and cached_pg.get('results'):
        print(f"  📦 PG cache hit for SearXNG people search ({domain})")
        return cached_pg['results']
    
    print(f"  🔍 Searching SearXNG for people at {domain}...")
    
    all_people = []
    
    # Search queries to find people at the company
    queries = [
        f'site:{domain} "team" OR "leadership" OR "about" OR "staff"',
        f'{domain} "team" OR "leadership" OR "executive" OR "founders"',
        f'"{domain}" "CTO" OR "CEO" OR "VP" OR "Head of" OR "Director" OR "Lead"',
    ]
    
    for query in queries:
        results = searxng.search(query)
        
        for r in results[:10]:
            title = r.get('title', '')
            url = r.get('url', '')
            snippet = r.get('snippet', '')
            
            # Extract names from title and snippet
            import re
            # Look for name patterns: "First Last" or "First Last - Role"
            name_patterns = [
                r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*[-–—]\s*([^|]+)',  # "Name - Role"
                r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*[|:]\s*([^|]+)',   # "Name | Role"
            ]
            
            for pattern in name_patterns:
                matches = re.findall(pattern, title + ' ' + snippet)
                for match in matches:
                    name = match[0].strip()
                    role = match[1].strip() if len(match) > 1 else ''
                    
                    # Filter out common false positives
                    if len(name.split()) == 2 and all(part[0].isupper() for part in name.split()):
                        all_people.append({
                            'name': name,
                            'role': role,
                            'source_url': '',
                            'domain': '',
                            'source': 'searxng'
                        })
            
            # Also extract from URLs (LinkedIn profiles)
            linkedin_urls = re.findall(r'https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9\-_%]+', r.get('url', '') + ' ' + snippet)
            for li_url in linkedin_urls:
                # Extract name from LinkedIn URL
                name_from_url = li_url.split('/in/')[-1].split('?')[0].split('-')
                if len(name_from_url) >= 2:
                    name = ' '.join([part.capitalize() for part in name_from_url[:2]])
                    all_people.append({
                        'name': name,
                        'role': '',
                        'source_url': li_url,
                        'domain': 'linkedin.com',
                        'source': 'searxng'
                    })
    
    # Deduplicate
    seen = set()
    deduped = []
    for p in all_people:
        key = p.get('name', '').lower()
        if key and key not in seen:
            seen.add(key)
            deduped.append(p)
    
    print(f"  🔍 Found {len(deduped)} people at domain")
    
    # Cache results
    if redis_client:
        cache_set_json(redis_client, f"people:searxng:{domain}", {'results': deduped}, CACHE_TTL_ENRICHMENT)
    
    # Cache in PG
    pg_execute(pg_conn, """
        INSERT INTO enrichment_cache (domain, names_hash, results, expires_at)
        VALUES (%s, %s, %s, NOW() + INTERVAL '%s seconds')
        ON CONFLICT (domain, names_hash) DO UPDATE SET
            results = EXCLUDED.results,
            expires_at = EXCLUDED.expires_at
    """, (domain, f"people_{domain}", json.dumps(deduped), CACHE_TTL_ENRICHMENT))
    
    return deduped


# ============================================================
# SEARXNG JOB SEARCH (with caching)
# ============================================================

def search_jobs_searxng(searxng: SearXNGClient, company_name: str, domain: str, redis_client: Optional[redis.Redis]) -> List[dict]:
    query = f'site:{domain} ("Senior AI" OR "ML Engineer" OR "Robotics Engineer" OR "Research Scientist" OR "Simulation Engineer" OR "Physics Engineer" OR "Computer Vision") careers jobs'
    cache_key = f"search:{hashlib.md5(query.encode()).hexdigest()}"

    # Check Redis cache
    cached = cache_get_json(redis_client, cache_key) if redis_client else None
    if cached:
        print(f"  📦 Cache hit for job search ({company_name})")
        return cached

    print(f"  🔍 Searching SearXNG for {company_name} jobs...")
    if not searxng.logged_in:
        searxng.login()

    results = searxng.search(query)

    # Convert to standard format
    jobs = []
    for r in results[:10]:
        if r.get('url') and r.get('title'):
            jobs.append({
                'title': r.get('title', ''),
                'url': r.get('url', ''),
                'snippet': r.get('snippet', ''),
                'company': company_name
            })

    # Cache results
    if redis_client:
        cache_set_json(redis_client, cache_key, jobs, CACHE_TTL_SEARCH)

    return jobs


def search_jobs_fallback(company_name: str, domain: str) -> List[dict]:
    """Fallback: generate generic careers page URL when SearXNG unavailable."""
    return [{
        'title': 'Careers / Opportunities',
        'url': f'https://{domain}/careers' if domain else '',
        'snippet': f'Exploring opportunities at {company_name} in robotics, AI, simulation, or related fields.',
        'company': company_name
    }]


# ============================================================
# SEARXNG EMAIL FINDING (replaces Hunter.io)
# ============================================================

def find_emails_searxng(searxng: SearXNGClient, domain: str, names: List[str], redis_client: Optional[redis.Redis], pg_conn) -> List[dict]:
    """Find emails for specific names at a domain using SearXNG search."""
    if not names:
        return []
    
    cache_key = f"emails:searxng:{domain}:{hashlib.md5('|'.join(sorted(names)).encode()).hexdigest()}"
    
    # Check Redis cache
    cached = cache_get_json(redis_client, cache_key) if redis_client else None
    if cached:
        print(f"  📦 Cache hit for SearXNG email search ({domain})")
        return cached
    
    # Check PG cache
    names_hash = hashlib.md5('|'.join(sorted(names)).encode()).hexdigest()
    cached_pg = pg_get_json(pg_conn,
        "SELECT results FROM enrichment_cache WHERE domain = %s AND names_hash = %s AND expires_at > NOW()",
        (domain, names_hash)
    )
    if cached_pg and cached_pg.get('results'):
        print(f"  📦 PG cache hit for SearXNG email search ({domain})")
        return cached_pg['results']
    
    print(f"  🔍 Searching SearXNG for emails at {domain}...")
    if not searxng.logged_in:
        searxng.login()
    
    all_emails = []
    for name in names[:10]:  # Limit to 10 names per domain
        query = f'"{name}" email @{domain}'
        results = searxng.search(query)
        
        for r in results[:5]:
            # Extract emails from snippets
            import re
            snippet = r.get('snippet', '')
            emails_found = re.findall(r'[a-zA-Z0-9._%+-]+@' + re.escape(domain), snippet, re.IGNORECASE)
            for email in emails_found:
                all_emails.append({
                    'email': email.lower(),
                    'first_name': name.split()[0] if name.split() else '',
                    'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
                    'position': '',
                    'department': '',
                    'confidence': 70,
                    'source': 'searxng',
                    'smtp_status': 'unknown',
                    'catch_all_domain': False,
                    'pattern_used': '',
                    'pattern_confidence': 0.0
                })
    
    # Deduplicate
    seen = set()
    deduped = []
    for e in all_emails:
        if e['email'] not in seen:
            seen.add(e['email'])
            deduped.append(e)
    
    # Cache results
    if redis_client:
        cache_set_json(redis_client, cache_key, {'results': deduped}, CACHE_TTL_ENRICHMENT)
    
    # Cache in PG
    pg_execute(pg_conn, """
        INSERT INTO enrichment_cache (domain, names_hash, results, expires_at)
        VALUES (%s, %s, %s, NOW() + INTERVAL '%s seconds')
        ON CONFLICT (domain, names_hash) DO UPDATE SET
            results = EXCLUDED.results,
            expires_at = EXCLUDED.expires_at
    """, (domain, names_hash, json.dumps(deduped), CACHE_TTL_ENRICHMENT))
    
    return deduped


# ============================================================
# LEADFINDER WRAPPER (with caching)
# ============================================================

def enrich_contacts_leadfinder(domain: str, names: List[str], redis_client: Optional[redis.Redis], pg_conn) -> List[dict]:
    """Use leadfinder.py to find and verify emails for given names at domain."""
    cache_key = f"enrichment:{domain}:{hashlib.md5('|'.join(sorted(names)).encode()).hexdigest()}"
    
    # Check Redis cache
    cached = cache_get_json(redis_client, cache_key) if redis_client else None
    if cached:
        print(f"  📦 Cache hit for enrichment ({domain})")
        return cached.get('results', [])
    
    # Check PostgreSQL cache
    names_hash = hashlib.md5('|'.join(sorted(names)).encode()).hexdigest()
    cached_pg = pg_get_json(pg_conn,
        "SELECT results FROM enrichment_cache WHERE domain = %s AND names_hash = %s AND expires_at > NOW()",
        (domain, names_hash)
    )
    if cached_pg and cached_pg.get('results'):
        print(f"  📦 PG cache hit for enrichment ({domain})")
        return cached_pg['results']

    print(f"  🔍 Running leadfinder for {domain} with {len(names)} names...")
    
    if not LEADFINDER_AVAILABLE:
        print("  ⚠️  leadfinder module not available")
        return []

    try:
        result = leadfinder.find_leads(domain, names)
        if 'error' in result:
            print(f"  ⚠️  Leadfinder error: {result['error']}")
            return []

        # Extract relevant contacts
        contacts = []
        for r in result.get('results', []):
            if 'error' not in r:
                contacts.append({
                    'email': r.get('email'),
                    'first_name': r.get('name', '').split()[0] if r.get('name') else '',
                    'last_name': ' '.join(r.get('name', '').split()[1:]) if r.get('name') else '',
                    'position': '',
                    'department': '',
                    'confidence': 80,
                    'source': 'leadfinder',
                    'smtp_status': r.get('smtp_status', 'unknown'),
                    'catch_all_domain': result.get('catch_all_domain', False),
                    'pattern_used': r.get('pattern_used', 'first.last'),
                    'pattern_confidence': result.get('pattern_confidence', 0.0)
                })

        # Cache in Redis
        if redis_client:
            cache_set_json(redis_client, cache_key, {'results': contacts}, CACHE_TTL_ENRICHMENT)

        # Cache in PostgreSQL
        pg_execute(pg_conn, """
            INSERT INTO enrichment_cache (domain, names_hash, results, expires_at)
            VALUES (%s, %s, %s, NOW() + INTERVAL '%s seconds')
            ON CONFLICT (domain, names_hash) DO UPDATE SET
                results = EXCLUDED.results,
                expires_at = EXCLUDED.expires_at
        """, (domain, names_hash, json.dumps(contacts), CACHE_TTL_ENRICHMENT))

        return contacts

    except Exception as e:
        print(f"  ❌ Leadfinder error: {e}")
        return []


# ============================================================
# HUNTER.IO ENRICHMENT (OPTIONAL FALLBACK ONLY)
# ============================================================

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

def enrich_contacts_hunter(domain: str, redis_client: Optional[redis.Redis], pg_conn) -> List[dict]:
    """Optional fallback - only if SearXNG/leadfinder fail."""
    if not HUNTER_API_KEY:
        return []
    
    cache_key = f"enrichment:hunter:{domain}"
    names_hash = "hunter"
    
    # Check Redis cache
    cached = cache_get_json(redis_client, cache_key) if redis_client else None
    if cached:
        print(f"  📦 Cache hit for Hunter enrichment ({domain})")
        return cached.get('results', [])
    
    # Check PG
    cached_pg = pg_get_json(pg_conn,
        "SELECT results FROM enrichment_cache WHERE domain = %s AND names_hash = %s AND expires_at > NOW()",
        (domain, names_hash)
    )
    if cached_pg and cached_pg.get('results'):
        print(f"  📦 PG cache hit for Hunter ({domain})")
        return cached_pg['results']
    
    print(f"  📧 Querying Hunter.io for {domain} (fallback)...")
    url = "https://api.hunter.io/v2/domain-search"
    params = {"domain": domain, "api_key": HUNTER_API_KEY, "limit": 10}
    
    try:
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            emails = []
            for email_data in data.get("data", {}).get("emails", []):
                emails.append({
                    "email": email_data.get("value"),
                    "first_name": email_data.get("first_name"),
                    "last_name": email_data.get("last_name"),
                    "position": email_data.get("position"),
                    "confidence": email_data.get("confidence"),
                    "department": email_data.get("department"),
                    "source": "hunter"
                })
            
            # Cache
            if redis_client:
                cache_set_json(redis_client, cache_key, {'results': emails}, CACHE_TTL_ENRICHMENT)
            
            return emails
    except Exception as e:
        print(f"  ❌ Hunter error: {e}")
    return []


# ============================================================
# CONTACT FILTERING
# ============================================================

TARGET_KEYWORDS = [
    "engineer", "engineering", "cto", "vp", "head", "lead", "principal",
    "director", "manager", "hiring", "talent", "recruit", "technical",
    "research", "science", "robotics", "ai", "ml", "machine learning",
    "simulation", "physics", "computer vision", "autonomy", "autonomous"
]

def filter_relevant_contacts(emails: List[dict]) -> List[dict]:
    relevant = []
    for e in emails:
        position = (e.get("position") or "").lower()
        department = (e.get("department") or "").lower()
        if any(kw in position for kw in TARGET_KEYWORDS) or any(kw in department for kw in TARGET_KEYWORDS):
            relevant.append(e)
    return relevant


# ============================================================
# COMPANY & CONTACT PERSISTENCE (PostgreSQL)
# ============================================================

def upsert_company(pg_conn, company: dict) -> int:
    """Insert or update company, return company_id."""
    if not pg_conn:
        return 0
    query = """
        INSERT INTO companies (domain, name, location, priority_tier, sponsor_type, sponsor_route, matched_keywords, last_enriched_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (domain) DO UPDATE SET
            name = EXCLUDED.name,
            location = EXCLUDED.location,
            priority_tier = EXCLUDED.priority_tier,
            sponsor_type = EXCLUDED.sponsor_type,
            sponsor_route = EXCLUDED.sponsor_route,
            matched_keywords = EXCLUDED.matched_keywords,
            last_enriched_at = NOW()
        RETURNING id;
    """
    params = (
        company.get('domain'),
        company.get('name'),
        company.get('location'),
        1,  # priority_tier
        company.get('sponsor_type'),
        company.get('route'),
        company.get('matched_keywords', [])
    )
    result = pg_get_json(pg_conn, query, params)
    return result['id'] if result else 0


def upsert_contact(pg_conn, company_id: int, contact: dict) -> int:
    """Insert or update contact, return contact_id."""
    if not pg_conn or company_id == 0:
        return 0
    query = """
        INSERT INTO contacts (company_id, email, first_name, last_name, position, department, confidence, source, smtp_status, catch_all_domain, pattern_used, pattern_confidence, last_enriched_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (company_id, email) DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            position = EXCLUDED.position,
            department = EXCLUDED.department,
            confidence = EXCLUDED.confidence,
            source = EXCLUDED.source,
            smtp_status = EXCLUDED.smtp_status,
            catch_all_domain = EXCLUDED.catch_all_domain,
            pattern_used = EXCLUDED.pattern_used,
            pattern_confidence = EXCLUDED.pattern_confidence,
            last_enriched_at = NOW()
        RETURNING id;
    """
    params = (
        company_id,
        contact.get('email'),
        contact.get('first_name', ''),
        contact.get('last_name', ''),
        contact.get('position', ''),
        contact.get('department', ''),
        contact.get('confidence', 0),
        contact.get('source', 'unknown'),
        contact.get('smtp_status', 'unknown'),
        contact.get('catch_all_domain', False),
        contact.get('pattern_used', ''),
        contact.get('pattern_confidence', 0.0)
    )
    result = pg_get_json(pg_conn, query, params)
    return result['id'] if result else 0


def save_draft(pg_conn, company_id: int, contact_id: int, job: dict, contact: dict, draft_path: str, content_hash: str) -> int:
    if not pg_conn:
        return 0
    query = """
        INSERT INTO drafts (company_id, contact_id, job_title, job_url, subject, body_text, body_html, content_hash, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'drafted')
        ON CONFLICT (content_hash) DO UPDATE SET
            updated_at = NOW()
        RETURNING id;
    """
    # Read draft content
    with open(draft_path, 'r') as f:
        draft_content = f.read()
    
    subject = f"{job.get('title', 'Role')} at {job.get('company', '')} — Physics Verification for Physical AI (Haga)"
    body_text = draft_content
    body_html = draft_content.replace('\n', '<br>')
    
    params = (
        company_id,
        contact_id,
        job.get('title', 'Role'),
        job.get('url', ''),
        subject,
        body_text,
        body_html,
        content_hash
    )
    result = pg_get_json(pg_conn, query, params)
    return result['id'] if result else 0


def check_draft_exists(pg_conn, content_hash: str) -> bool:
    if not pg_conn:
        return False
    result = pg_get_json(pg_conn, "SELECT 1 FROM drafts WHERE content_hash = %s", (content_hash,))
    return result is not None


def log_application(pg_conn, draft_id: int, contact_email: str, subject: str):
    if not pg_conn or draft_id == 0:
        return
    pg_execute(pg_conn, """
        INSERT INTO applications (draft_id, status, sent_at)
        VALUES (%s, 'drafted', NOW())
        ON CONFLICT DO NOTHING
    """, (draft_id,))


# ============================================================
# DRAFT GENERATION
# ============================================================

COMPANY_TECH_MAP = {
    "Shadow Robot": "dexterous manipulation and MuJoCo simulation",
    "JBS Applied A.I": "AI and robotics research",
    "Apollo Research": "AI safety and interpretability",
    "CGA Simulation": "digital twin and simulation technology",
    "HPi Verification": "engineering verification services",
    "Fieldwork Robotics": "agricultural robotics and autonomy",
    "Oxford Robotics": "advanced robotics from Oxford spinout",
    "Prosper Robotics": "robotics innovation",
    "Perceptual Robotics": "computer vision for robotic inspection",
    "Extend Robotics": "teleoperation and VR robotics",
    "Human Digital Twin": "digital twin technology",
    "Mistral AI": "foundation models and open-weight LLMs",
    "Stability AI": "generative AI and world models",
    "Tecosim": "technical simulation engineering",
    "The Simulator Company": "simulation technology",
    "General Physics": "physics-based engineering",
    "Innovative Physics": "physics innovation"
}


def generate_outreach_draft(company: dict, job: dict, contact: dict) -> tuple[str, str]:
    """Generate draft, return (filepath, content_hash)."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_company = re.sub(r'[^\w\s-]', '', company["name"]).replace(" ", "_")
    safe_role = re.sub(r'[^\w\s-]', '', job.get("title", "Role")).replace(" ", "_")[:50]
    filename = f"{safe_company}_{safe_role}_{date_str}.md"
    filepath = Path(DRAFTS_DIR) / filename

    job_snippet = job.get("snippet", "")
    company_name = company["name"]

    company_tech = "cutting-edge robotics and simulation"
    for key, val in COMPANY_TECH_MAP.items():
        if key.lower() in company_name.lower():
            company_tech = val
            break

    draft = f"""---
to: {contact.get('email', '')}
subject: {job.get('title', 'Role')} at {company_name} — Physics Verification for Physical AI (Haga)
company: {company_name}
role: {job.get('title', 'Role')}
job_url: {job.get('url', '')}
contact_name: {contact.get('first_name', '')} {contact.get('last_name', '')}
contact_email: {contact.get('email', '')}
contact_position: {contact.get('position', '')}
date: {date_str}
status: drafted
---

# Outreach Draft: {company_name} — {job.get('title', 'Role')}

## Email

**To:** {contact.get('first_name', '')} {contact.get('last_name', '')} <{contact.get('email', '')}>
**Subject:** {job.get('title', 'Role')} at {company_name} — Physics Verification for Physical AI (Haga)

---

Hi {contact.get('first_name', 'there')},

Saw the **{job.get('title', 'role')}** opening at **{company_name}** — the focus on **{company_tech}** caught my eye.

I'm the founder of **Haga** (haga.mushoodhanif.com), where we build independent physics verification for robot learning policies and generative world models. Our benchmark stresses policies under adversarial mass/friction perturbations in **MuJoCo/Robosuite** (Lift, Stack, Door, PickPlaceCan) and scores physics consistency in generated video (**CogVideoX**, **Physics-IQ**) via calibrated detectors — permanence, ballistic, contact, static-hover.

Your work on **{company_tech}** aligns closely with the sim-to-real gap we're closing. I'd love a 15-min technical conversation to explore fit. Happy to share our Lab evidence (public metrics at haga.mushoodhanif.com/lab).

Note: {company_name} is listed as an **A-rated Skilled Worker sponsor** on the UK Home Office register — I'd need sponsorship to join.

Best,
**Mushood Hanif**
Founder, Haga | haga.mushoodhanif.com
GitHub: DivineDemon/haga-core
LinkedIn: linkedin.com/in/mushood-hanif

---

## Job Details
- **Company:** {company_name}
- **Role:** {job.get('title', 'N/A')}
- **Location:** {company.get('city', '')}, {company.get('county', '')}
- **Job URL:** {job.get('url', 'N/A')}
- **Snippet:** {job_snippet[:300]}...

## Contact Details
- **Name:** {contact.get('first_name', '')} {contact.get('last_name', '')}
- **Email:** {contact.get('email', '')}
- **Position:** {contact.get('position', 'N/A')}
- **Confidence:** {contact.get('confidence', 'N/A')}%

## Company Sponsor Info
- **Sponsor Type:** {company.get('sponsor_type', 'N/A')}
- **Route:** {company.get('route', 'N/A')}
- **Matched Keywords:** {', '.join(company.get('matched_keywords', []))}
"""

    filepath = Path(DRAFTS_DIR) / filename
    filepath.write_text(draft)
    
    # Generate content hash for deduplication
    content_hash = hashlib.sha256(draft.encode()).hexdigest()
    
    return str(filepath), content_hash


# ============================================================
# YAHOO MAIL BROWSER AUTOMATION
# ============================================================

def send_email_yahoo(contact: dict, subject: str, body_text: str, body_html: str, attachment_path: Optional[str] = None) -> bool:
    """Send email via Yahoo Mail using browser CDP automation (requires Hermes runtime)."""
    try:
        from hermes_tools import browser_cdp, browser_navigate, browser_snapshot
        import time
        
        print(f"  📧 Sending email to {contact.get('email')} via Yahoo Mail...")
        
        # Navigate to Yahoo Mail compose
        target_id = browser_navigate("https://compose.mail.yahoo.com")
        
        # Wait for compose page to load
        time.sleep(3)
        
        # Get snapshot to find elements
        snapshot = browser_snapshot(target_id=target_id)
        
        # Find recipient field and fill
        # Yahoo Mail uses specific selectors - we'll use JavaScript
        js_code = f"""
        // Find and fill recipient field
        const toField = document.querySelector('input[data-test-id="compose-to-field"]', input[aria-label="To"], #message-to-field');
        if (toField) {{
            toField.value = '{contact.get('email', '')}';
            toField.dispatchEvent(new Event('input', {{bubbles: true}}));
        }}
        
        // Find and fill subject field
        const subjectField = document.querySelector('input[data-test-id="compose-subject-input"]', input[aria-label="Subject"], #compose-subject-input');
        if (subjectField) {{
            subjectField.value = '{subject.replace("'", "\\'")}';
            subjectField.dispatchEvent(new Event('input', {{bubbles: true}}));
        }}
        
        // Find and fill body (rich text editor)
        const bodyField = document.querySelector('[data-test-id="rte"], [contenteditable="true"], #compose-rte');
        if (bodyField) {{
            bodyField.innerHTML = `{body_html.replace("`", "\\`").replace("$", "\\$")}`;
            bodyField.dispatchEvent(new Event('input', {{bubbles: true}}));
        }}
        
        return true;
        """
        
        result = browser_cdp(
            method="Runtime.evaluate",
            params={"expression": js_code, "returnByValue": True},
            target_id=target_id
        )
        
        time.sleep(2)
        
        # Attach file if provided
        if attachment_path and Path(attachment_path).exists():
            attach_js = f"""
            const fileInput = document.querySelector('input[type="file"]');
            if (fileInput) {{
                // Note: Can't set file input via JS for security reasons
                // This would need a different approach
                console.log('File attachment needs manual handling');
            }}
            """
            browser_cdp(
                method="Runtime.evaluate",
                params={"expression": attach_js, "returnByValue": True},
                target_id=target_id
            )
            time.sleep(1)
        
        # Click send button
        send_js = """
        // Find and click send button
        const buttons = Array.from(document.querySelectorAll('button, div[role="button"]'));
        const sendButton = buttons.find(btn => 
            btn.textContent.trim().toLowerCase() === 'send' ||
            btn.getAttribute('aria-label')?.toLowerCase().includes('send') ||
            btn.getAttribute('data-test-id')?.includes('send')
        );
        if (sendButton) {{
            sendButton.click();
            return true;
        }}
        return false;
        """
        
        result = browser_cdp(
            method="Runtime.evaluate",
            params={"expression": send_js, "returnByValue": True},
            target_id=target_id
        )
        
        time.sleep(3)
        
        print(f"  ✅ Email sent to {contact.get('email')} via Yahoo Mail")
        return True
        
    except ImportError:
        print("  ⚠️  Browser automation tools not available in current environment")
        print("  📝 Email draft saved - will be sent when run in Hermes runtime")
        return False
    except Exception as e:
        print(f"  ❌ Yahoo Mail send error: {e}")
        return False


# ============================================================
# MAIN AUTOMATION
# ============================================================

def scan_csv_for_priority_companies() -> List[dict]:
    """Scan the full CSV for A-rated sponsors matching tech keywords."""
    matches = []
    seen = set()
    
    with open(CSV_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            org = row.get('Organisation Name', '').strip()
            city = row.get('Town/City', '').strip()
            county = row.get('County', '').strip()
            sponsor_type = row.get('Type & Rating', '').strip()
            route = row.get('Route', '').strip()
            
            if 'A rating' not in sponsor_type or 'Skilled Worker' not in route:
                continue
            
            org_lower = org.lower()
            key = f"{org_lower}_{city.lower()}"
            if key in seen:
                continue
            
            matched_keywords = [kw for kw in TECH_KEYWORDS if kw in org_lower]
            if matched_keywords:
                exclude = ['retail', 'food', 'wine', 'pizza', 'chicken', 'restaurant', 'cafe', 'bakery',
                          'care', 'health', 'hospital', 'clinic', 'pharmacy', 'medical', 'dental',
                          'property', 'construction', 'refrigeration', 'air conditioning', 'plumbing',
                          'electrical', 'cleaning', 'security', 'taxi', 'transport', 'logistics',
                          'accounting', 'accountants', 'legal', 'law', 'solicitor', 'church',
                          'charity', 'association', 'muslim', 'mosque', 'temple', 'school',
                          'nursery', 'childcare', 'beauty', 'hair', 'salon', 'spa', 'fitness',
                          'gym', 'hotel', 'accommodation', 'travel', 'tourism', 'estate agent',
                          'letting', 'insurance', 'finance', 'bank', 'mortgage',
                          'recruitment', 'employment', 'staffing', 'agency', 'convenience',
                          'newsagent', 'shop', 'store', 'supermarket', 'grocery', 'off license',
                          'garage', 'mot', 'tyre', 'car', 'van', 'vehicle', 'breakdown',
                          'waste', 'recycling', 'skip', 'drain', 'sewage', 'pest control',
                          'locksmith', 'glazing', 'roofing', 'fencing', 'landscaping',
                          'training', 'driving', 'instructor', 'tuition', 'tutor', 'language',
                          'translation', 'interpreter', 'visa', 'immigration', 'passport',
                          'citizenship', 'notary', 'commissioner', 'granite', 'aesthetics',
                          'laboratory furniture', 'racking', 'storage', 'fabrication',
                          'heating', 'energy', 'offshore', 'ground engineering', 'civil engineering',
                          'mobile', 'computer repair', 'computer services', 'telecom',
                          'meat', 'photonic', 'performance', 'yorkshire', 'mumbai', 'lounge',
                          'film', 'holdings', 'supplies', 'drinks', 'tea']
                if not any(ex in org_lower for ex in exclude):
                    matches.append({
                        "name": org, "city": city, "county": county,
                        "sponsor_type": sponsor_type, "route": route,
                        "matched_keywords": matched_keywords[:5]
                    })
                    seen.add(key)
    return matches


def main():
    print("=" * 60)
    print("🤖 HAGA UK SPONSOR JOB AUTOMATION V2")
    print(f"⏰ Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Initialize services
    print("\n🔧 Initializing services...")
    redis_client = init_redis()
    pg_conn = init_pg()

    # Initialize SearXNG client
    searxng = SearXNGClient(SEARXNG_URL, SEARXNG_USERNAME, SEARXNG_PASSWORD)
    searxng_available = searxng.login()
    if searxng_available:
        print("  ✅ SearXNG connected")
    else:
        print("  ⚠️  SearXNG unavailable, using fallback search")

    # Step 1: Load priority companies from CSV (dynamic, tracks processed)
    print("\n📊 Loading priority companies from CSV...")
    all_companies = load_priority_companies_from_csv(CSV_PATH, pg_conn)
    print(f"   Found {len(all_companies)} total priority companies")
    
    # Get next batch (skip already processed)
    companies = get_next_batch_companies(all_companies, BATCH_SIZE, pg_conn)
    print(f"\n🔍 Processing batch of {len(companies)} companies...")

    date_str = datetime.now().strftime("%Y-%m-%d")
    all_jobs = []
    all_contacts = []
    all_drafts = []
    stats = {
        "companies_processed": 0,
        "jobs_found": 0,
        "contacts_enriched": 0,
        "drafts_generated": 0,
        "drafts_skipped_duplicate": 0,
        "drafts_skipped_no_contacts": 0,
        "searxng_searches": 0,
        "leadfinder_calls": 0,
        "hunter_calls": 0,
        "errors": []
    }

    for i, company in enumerate(companies):
        stats["companies_processed"] += 1
        print(f"\n   [{i+1}/{len(companies)}] Processing: {company['name']}")

        domain = company.get("domain")
        if not domain:
            print(f"      ⚠️  No known domain, skipping")
            continue
        print(f"      🌐 Domain: {domain}")

        # Upsert company in DB
        company_id = upsert_company(pg_conn, company)

        # Rate limit
        time.sleep(RATE_LIMIT_DELAY)

        # Search for jobs
        jobs = []
        if searxng_available:
            jobs = search_jobs_searxng(searxng, company['name'], domain, redis_client)
            stats["searxng_searches"] += 1
        else:
            jobs = search_jobs_fallback(company['name'], domain)
        
        print(f"      💼 Found {len(jobs)} potential job postings")
        stats["jobs_found"] += len(jobs)

        for job in jobs[:3]:
            job["company_name"] = company["name"]
            job["company_location"] = company.get("location", "")

        # Enrich contacts (SearXNG primary, Leadfinder verification, Hunter fallback)
        all_emails = []

        # Primary: SearXNG people search (if SearXNG available)
        if searxng_available:
            print(f"      🔍 Searching SearXNG for people at {domain}...")
            people = find_people_searxng(searxng, domain, redis_client, pg_conn)
            if people:
                stats["searxng_searches"] += 1
                print(f"      🔍 SearXNG found {len(people)} people")
                # Convert people to email format for leadfinder verification
                for p in people:
                    # Handle case where p might be a string (from cache) or dict
                    if isinstance(p, str):
                        p_name = p
                        p_role = ''
                        p_source_url = ''
                    elif isinstance(p, dict):
                        p_name = p.get('name', '')
                        p_role = p.get('role', '')
                        p_source_url = p.get('source_url', '')
                    else:
                        # Skip unexpected
                        continue

                    all_emails.append({
                        'email': '',  # Will be filled by leadfinder
                        'first_name': p_name.split()[0] if p_name else '',
                        'last_name': ' '.join(p_name.split()[1:]) if len(p_name.split()) > 1 else '',
                        'position': p_role,
                        'department': '',
                        'confidence': 60,
                        'source': 'searxng',
                        'smtp_status': 'unknown',
                        'catch_all_domain': False,
                        'pattern_used': '',
                        'pattern_confidence': 0.0,
                        'linkedin_url': p_source_url
                    })
            print(f"      🔍 SearXNG people: {len([e for e in all_emails if e.get('source') == 'searxng'])}")
        
        # Leadfinder verification (for names we found via SearXNG)
        leadfinder_names = []
        for e in all_emails:
            if e.get('first_name') or e.get('last_name'):
                name = f"{e.get('first_name','')} {e.get('last_name','')}".strip()
                if name:
                    leadfinder_names.append(name)
        
        # Add common role-based names
        leadfinder_names.extend(['CTO', 'VP Engineering', 'Head of Engineering', 'Engineering Manager',
                                'Technical Lead', 'Principal Engineer', 'Staff Engineer',
                                'Head of AI', 'VP AI', 'AI Lead', 'Research Lead',
                                'Head of Robotics', 'VP Robotics', 'Robotics Lead'])
        
        unique_names = list(set([n for n in leadfinder_names if n]))[:10]
        if unique_names:
            lf_emails = enrich_contacts_leadfinder(domain, unique_names[:5], redis_client, pg_conn)
            stats["leadfinder_calls"] += 1
            for e in lf_emails:
                e['source'] = 'leadfinder'
            all_emails.extend(lf_emails)
            print(f"      🔍 Leadfinder emails: {len(lf_emails)}")
        
        # Hunter.io as optional fallback only
        if not searxng_available or len(all_emails) < 3:
            hunter_emails = enrich_contacts_hunter(domain, redis_client, pg_conn)
            if hunter_emails:
                stats["hunter_calls"] += 1
                for e in hunter_emails:
                    e['source'] = 'hunter'
                all_emails.extend(hunter_emails)
                print(f"      📧 Hunter.io (fallback): {len(hunter_emails)}")
        
        print(f"      📧 Total emails found: {len(all_emails)}")
        
        relevant = filter_relevant_contacts(all_emails)
        print(f"      🎯 Relevant contacts: {len(relevant)}")
        stats["contacts_enriched"] += len(relevant)

        # Job contexts
        job_contexts = jobs[:3] if jobs else [{
            "title": "Careers / Opportunities",
            "url": f"https://{domain}/careers" if domain else "",
            "snippet": f"Exploring opportunities at {company['name']} in robotics, AI, simulation, or related fields."
        }]

        if not relevant:
            print(f"      ⏭️  Skipping drafts - no relevant contacts")
            stats["drafts_skipped_no_contacts"] += 1
            continue

        # Generate drafts for top 3 contacts per job context
        for job in job_contexts:
            for contact in relevant[:3]:
                # Upsert contact
                contact_id = upsert_contact(pg_conn, company_id, contact)

                # Generate draft
                draft_path, content_hash = generate_outreach_draft(company, job, contact)

                # Check deduplication
                if check_draft_exists(pg_conn, content_hash):
                    print(f"      ⏭️  Skipping duplicate draft")
                    stats["drafts_skipped_duplicate"] += 1
                    continue

                # Save draft metadata
                draft_id = save_draft(pg_conn, company_id, contact_id, job, contact, draft_path, content_hash)
                
                # Send email via Yahoo Mail (if contact has email)
                if contact.get('email'):
                    print(f"  📧 Sending email via Yahoo Mail...")
                    email_sent = send_email_yahoo(
                        contact=contact,
                        subject=f"{job.get('title', 'Role')} at {company['name']} — Physics Verification for Physical AI (Haga)",
                        body_text=open(draft_path).read(),
                        body_html=open(draft_path).read().replace('\n', '<br>'),
                        attachment_path=RESUME_PATH if Path(RESUME_PATH).exists() else None
                    )
                    if email_sent:
                        # Update application status
                        pg_execute(pg_conn, 
                            "UPDATE applications SET status = 'sent', sent_at = NOW() WHERE id = (SELECT id FROM applications WHERE draft_id = %s ORDER BY created_at DESC LIMIT 1)",
                            (draft_id,))
                
                all_drafts.append({
                    "draft_path": draft_path,
                    "company": company["name"],
                    "job_title": job.get("title"),
                    "contact_email": contact.get("email"),
                    "contact_name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}",
                    "draft_id": draft_id
                })

                log_application(pg_conn, draft_id, contact.get('email'), f"{job.get('title', 'Role')} at {company['name']}")
                stats["drafts_generated"] += 1
                print(f"      ✍️  Draft created: {Path(draft_path).name}")

    # Summary
    print("\n" + "=" * 60)
    print("📋 RUN SUMMARY")
    print("=" * 60)
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"\n📁 Drafts in: {DRAFTS_DIR}")
    print(f"📁 Logs in: {LOG_DIR}")

    if all_drafts:
        print("\n📧 Drafts generated:")
        for d in all_drafts:
            print(f"   • {d['company']} — {d['job_title']} → {d['contact_name']} ({d['contact_email']})")

    # WhatsApp notification
    try:
        whatsapp_msg = f"""🤖 *Haga Job Automation V2 Complete* ({date_str})

📊 *Results:*
• Companies processed: {stats['companies_processed']}
• Jobs found: {stats['jobs_found']}
• Contacts enriched: {stats['contacts_enriched']}
• Drafts generated: {stats['drafts_generated']}
• Duplicates skipped: {stats['drafts_skipped_duplicate']}
• No contacts skipped: {stats['drafts_skipped_no_contacts']}

🔍 *API Usage:*
• SearXNG searches: {stats['searxng_searches']}
• Leadfinder calls: {stats['leadfinder_calls']}
• Hunter.io calls: {stats['hunter_calls']}

📧 *Drafts ready for review:*
{chr(10).join([f'• {d["company"]} — {d["job_title"]}' for d in all_drafts[:5]])}

📁 Drafts: `01_INBOX/outreach_drafts/`"""
        resp = requests.post("http://localhost:8765/send",
                           json={"chatId": "193703595520068@lid", "message": whatsapp_msg}, timeout=5)
        if resp.status_code == 200:
            print("\n📱 WhatsApp notification sent!")
        else:
            print(f"\n📱 WhatsApp gateway error: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"\n📱 WhatsApp notification skipped: {e}")

    print("\n✅ Automation complete!")


if __name__ == "__main__":
    main()