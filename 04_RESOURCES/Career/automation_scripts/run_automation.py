#!/usr/bin/env python3
"""
Automated UK Sponsor Job Matching & Outreach for Mushood Hanif
Runs daily at 12 PM (Mon-Fri) via cron
"""

import os
import json
import requests
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Load environment
from dotenv import load_dotenv
load_dotenv("/Users/mushood/Documents/code/personal/coeus/.env.local")

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# Priority companies with known domains
PRIORITY_COMPANIES = [
    {"name": "JBS Applied A.I & Robotics Research Ltd", "location": "London", "domain": "jbs-ai-robotics.com"},
    {"name": "Shadow Robot Company Ltd.", "location": "London", "domain": "shadowrobot.com"},
    {"name": "Apollo Research AI Ltd", "location": "London", "domain": "apolloresearch.ai"},
    {"name": "CGA Simulation Ltd", "location": "Liverpool", "domain": "cga-simulation.com"},
    {"name": "HPi Verification Services Ltd", "location": "Wallingford", "domain": "hpi-verification.com"},
    {"name": "Fieldwork Robotics Limited", "location": "Cambridge", "domain": "fieldworkrobotics.com"},
    {"name": "Oxford Robotics Ltd", "location": "Reading", "domain": "oxfordrobotics.institute"},
    {"name": "Prosper Robotics Ltd", "location": "London", "domain": "prosper-robotics.com"},
    {"name": "Perceptual Robotics Limited", "location": "Bristol", "domain": "perceptualrobotics.com"},
    {"name": "Extend Robotics Limited", "location": "London", "domain": "extendrobotics.com"},
    {"name": "Human Digital Twin Limited", "location": "London", "domain": "humandigitaltwin.com"},
    {"name": "Mistral AI UK Limited", "location": "London", "domain": "mistral.ai"},
    {"name": "Stability AI Ltd", "location": "London", "domain": "stability.ai"},
    {"name": "Tecosim Technical Simulation Ltd.", "location": "Basildon", "domain": "tecosim.com"},
    {"name": "The Simulator Company Limited", "location": "London", "domain": "thesimulatorcompany.com"},
    {"name": "General Physics (UK) Ltd", "location": "London", "domain": "generalphysics.com"},
    {"name": "Innovative Physics Limited", "location": "Shanklin", "domain": "innovativephysics.co.uk"},
]

# Output directories
OUTREACH_DIR = Path("/Users/mushood/Documents/code/personal/coeus/01_INBOX/outreach_drafts")
CAREER_DIR = Path("/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career")
OUTREACH_DIR.mkdir(parents=True, exist_ok=True)
CAREER_DIR.mkdir(parents=True, exist_ok=True)

DATE_STR = datetime.now().strftime("%Y-%m-%d")
TIMESTAMP = datetime.now().isoformat()

# User profile for personalization
USER_PROFILE = {
    "name": "Mushood Hanif",
    "email": "haga@mushoodhanif.com",
    "company": "Haga",
    "role": "Founder",
    "expertise": [
        "MuJoCo", "Robosuite", "JAX", "World Models", "Physics Consistency",
        "Simulation", "CogVideoX", "Adversarial Policy Stress Testing",
        "Physical AI", "Robotics", "Independent Physics Verification"
    ],
    "target_roles": ["Senior AI Engineer", "ML Engineer", "Robotics Engineer", "Research Scientist"],
    "location_preference": "London (UK remote OK)",
    "visa_status": "Needs Skilled Worker sponsorship",
}

def serper_search(query: str, num_results: int = 10) -> Dict[str, Any]:
    """Search for job postings via Serper API."""
    if not SERPER_API_KEY:
        return {"error": "No Serper API key", "organic": []}
    
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": num_results, "gl": "uk", "hl": "en"}
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 402 or "quota" in resp.text.lower() or "credits" in resp.text.lower():
            return {"error": "Serper API out of credits", "organic": [], "out_of_credits": True}
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "organic": []}

def hunter_domain_search(domain: str, limit: int = 10) -> Dict[str, Any]:
    """Enrich contacts via Hunter.io domain search."""
    if not HUNTER_API_KEY:
        return {"error": "No Hunter API key", "emails": []}
    
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": domain,
        "api_key": HUNTER_API_KEY,
        "limit": limit,
        "type": "personal",
    }
    
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "data": {"emails": []}}

def filter_engineering_contacts(emails: List[Dict]) -> List[Dict]:
    """Filter for engineering/hiring/leadership roles."""
    keywords = [
        "engineer", "engineering", "hiring", "talent", "recruit", "hr", "people",
        "lead", "head", "director", "vp", "cto", "cpo", "founder", "cofounder",
        "manager", "principal", "senior", "staff", "tech", "research", "science",
        "robotics", "ai", "ml", "machine learning", "simulation", "physics"
    ]
    
    filtered = []
    for email_data in emails:
        position = (email_data.get("position") or "").lower()
        department = (email_data.get("department") or "").lower()
        first_name = (email_data.get("first_name") or "").lower()
        last_name = (email_data.get("last_name") or "").lower()
        
        # Check if position/department matches engineering/hiring keywords
        match = any(kw in position for kw in keywords) or any(kw in department for kw in keywords)
        
        # Also include generic roles that might be relevant
        if not match and position in ["", "unknown", "team member"]:
            match = True  # Include unknown positions as fallback
            
        if match:
            filtered.append(email_data)
    
    # Sort by confidence (Hunter provides confidence score)
    filtered.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    return filtered[:3]  # Top 3 contacts

def generate_outreach_draft(company: Dict, contact: Dict, job_info: Optional[Dict] = None) -> str:
    """Generate personalized outreach email draft."""
    
    company_name = company["name"]
    domain = company["domain"]
    location = company["location"]
    
    contact_name = f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip()
    contact_email = contact.get("email", "")
    contact_position = contact.get("position", "Engineering/Hiring Team")
    contact_department = contact.get("department", "")
    
    # Company-specific tech overlap
    tech_overlaps = {
        "jbs-ai-robotics.com": "JBS's focus on applied AI and robotics research aligns directly with Haga's physics verification for physical AI systems. Your work on sim-to-real transfer and policy optimization overlaps with my adversarial stress testing and world model verification.",
        "shadowrobot.com": "Shadow Robot's Dexterous Hand and teleoperation systems are exactly the kind of physical AI platforms that need independent physics verification. My MuJoCo/Robosuite expertise and CogVideoX-based world model validation could strengthen your sim-to-real pipeline.",
        "apolloresearch.ai": "Apollo's AI safety and interpretability research resonates with Haga's mission of physics consistency verification. Adversarial policy stress testing for physical systems complements your alignment work — ensuring policies don't just optimize reward but respect physical laws.",
        "cga-simulation.com": "CGA's defense/simulation background and synthetic data generation for AI training overlaps with Haga's physics verification. Validating that simulated physics matches reality is critical for your synthetic data quality.",
        "hpi-verification.com": "HPi's verification services name speaks for itself — Haga provides independent physics verification for the same physical AI/robotics domain. JAX-based world model checking could enhance your verification toolkit.",
        "fieldworkrobotics.com": "Fieldwork's agricultural robotics (raspberry picking etc.) need robust sim-to-real. My MuJoCo expertise and physics consistency checks for deformable object manipulation directly apply.",
        "oxfordrobotics.institute": "Oxford Robotics Institute's mobile autonomy and legged locomotion work aligns with Haga's physics verification. World model validation for dynamic locomotion policies is a natural fit.",
        "prosper-robotics.com": "Prosper's general-purpose home robotics requires bulletproof physics simulation. Haga's adversarial stress testing finds edge cases before deployment — critical for domestic environments.",
        "perceptualrobotics.com": "Perceptual's wind turbine inspection drones need verified physics for GPS-denied navigation. My simulation verification ensures world models match real aerodynamics.",
        "extendrobotics.com": "Extend's human-robot interface and teleoperation systems benefit from physics consistency checks — ensuring the sim matches the operator's mental model.",
        "humandigitaltwin.com": "Human Digital Twin's biomechanical simulation needs independent physics verification. Haga's JAX-based world model checking validates human motion physics.",
        "mistral.ai": "Mistral's frontier models could benefit from physics grounding verification. Haga verifies that generated code/simulations respect physical laws — a growing need for coding agents.",
        "stability.ai": "Stability's video generation (Stable Video Diffusion) and 3D assets need physics consistency. CogVideoX verification expertise directly applies to ensuring generated dynamics are physically plausible.",
        "tecosim.com": "Tecosim's CAE/simulation engineering for automotive/aerospace aligns with Haga's physics verification. Independent validation of simulation fidelity for physical AI.",
        "thesimulatorcompany.com": "The Simulator Company's simulation platform is exactly the layer Haga verifies. Physics consistency checking as a service for your simulation customers.",
        "generalphysics.com": "General Physics' scientific consulting overlaps with Haga's independent verification. Physics consistency for AI-driven simulation and digital twins.",
        "innovativephysics.co.uk": "Innovative Physics' radiation/physics simulation and AI aligns with Haga's verification of physics consistency in AI-generated simulations.",
    }
    
    tech_overlap = tech_overlaps.get(domain, 
        f"Your work at {company_name} in {location} aligns with Haga's independent physics verification for physical AI and robotics systems.")
    
    # Job-specific reference
    job_ref = ""
    if job_info and job_info.get("title"):
        job_ref = f"\n\nI saw your opening for **{job_info['title']}** and it closely matches my background in {', '.join(USER_PROFILE['expertise'][:5])}."
    else:
        job_ref = "\n\nWhile I didn't see a specific open role advertised, I'm reaching out because Haga's physics verification capability addresses a growing need in physical AI/robotics — and I'd value a conversation about how it could complement your team's work."
    
    draft = f"""---
to: {contact_email}
cc: 
subject: Physics verification for {company_name}'s physical AI systems — Mushood Hanif (Haga founder)
---

Hi {contact_name or contact_position.split()[0] if contact_position else 'Team'},

I'm Mushood Hanif, founder of **Haga** — independent physics verification for physical AI and robotics systems.

{tech_overlap}{job_ref}

**Why Haga matters for {company_name}:**
- **Physics consistency verification**: JAX-based world model checking that simulated dynamics match real-world physics (MuJoCo, Robosuite, custom sims)
- **Adversarial policy stress testing**: Automated discovery of sim-to-real gaps before deployment — critical for safety-critical robotics
- **CogVideoX / video generation verification**: Ensuring generated physical dynamics are physically plausible
- **Independent third-party validation**: Not tied to any simulator vendor — objective physics audits

**My background**: 7+ years in robotics simulation (MuJoCo, Robosuite, JAX), world models, physics consistency, and adversarial testing. Previously built simulation infrastructure for physical AI teams. Now running Haga as a verification layer for companies deploying physical AI.

**Visa**: I require **Skilled Worker sponsorship** (UK). {company_name} appears on the Home Office A-rated sponsor register.

Would you be open to a brief call to explore whether Haga's verification could add value to your pipeline — or if there's a role where my background fits directly?

Best regards,
Mushood Hanif
Founder, Haga
haga@mushoodhanif.com
https://mushoodhanif.com
London, UK (remote OK)
"""
    return draft

def main():
    print(f"=== Automation Run: {TIMESTAMP} ===")
    
    all_job_matches = {}
    all_enriched_contacts = {}
    all_drafts = []
    log_entries = []
    
    serper_out_of_credits = False
    
    for idx, company in enumerate(PRIORITY_COMPANIES, 1):
        name = company["name"]
        domain = company["domain"]
        location = company["location"]
        
        print(f"\n[{idx}/17] Processing: {name} ({domain})")
        log_entries.append({
            "timestamp": datetime.now().isoformat(),
            "company": name,
            "domain": domain,
            "step": "started"
        })
        
        # Step 1: Search for job postings (Serper)
        job_matches = []
        if not serper_out_of_credits:
            query = f'site:{domain} (job OR career OR hiring OR "software engineer" OR "robotics engineer" OR "ML engineer" OR "research scientist" OR "AI engineer")'
            print(f"  Searching Serper: {query}")
            serper_result = serper_search(query)
            
            if serper_result.get("out_of_credits"):
                serper_out_of_credits = True
                print("  ⚠️ Serper API out of credits — using fallback for remaining companies")
                log_entries.append({
                    "timestamp": datetime.now().isoformat(),
                    "company": name,
                    "step": "serper_out_of_credits",
                    "note": "Serper API credits exhausted"
                })
            else:
                organic = serper_result.get("organic", [])
                for result in organic[:5]:
                    title = result.get("title", "")
                    link = result.get("link", "")
                    snippet = result.get("snippet", "")
                    # Filter for engineering roles
                    if any(kw in title.lower() for kw in ["engineer", "research", "scientist", "developer", "ml", "ai", "robotics", "simulation", "physics"]):
                        job_matches.append({
                            "title": title,
                            "url": link,
                            "snippet": snippet,
                            "source": "serper"
                        })
                print(f"  Found {len(job_matches)} relevant job postings")
        
        all_job_matches[name] = job_matches
        
        # Step 2: Enrich contacts (Hunter.io)
        print(f"  Enriching contacts via Hunter.io for {domain}...")
        hunter_result = hunter_domain_search(domain, limit=10)
        
        emails = []
        if "data" in hunter_result and "emails" in hunter_result["data"]:
            emails = hunter_result["data"]["emails"]
        elif "emails" in hunter_result:
            emails = hunter_result["emails"]
        
        print(f"  Hunter.io returned {len(emails)} emails")
        
        # Filter for engineering/hiring contacts
        top_contacts = filter_engineering_contacts(emails)
        print(f"  Top {len(top_contacts)} engineering/hiring contacts selected")
        
        all_enriched_contacts[name] = {
            "domain": domain,
            "total_emails_found": len(emails),
            "top_contacts": top_contacts
        }
        
        log_entries.append({
            "timestamp": datetime.now().isoformat(),
            "company": name,
            "step": "hunter_complete",
            "emails_found": len(emails),
            "top_contacts": len(top_contacts)
        })
        
        # Step 3: Generate outreach drafts
        # Use first job match if available, else fallback
        job_info = job_matches[0] if job_matches else None
        
        for contact in top_contacts:
            draft = generate_outreach_draft(company, contact, job_info)
            
            # Save draft to file
            safe_name = name.replace(" ", "_").replace(".", "").replace("&", "and").replace(",", "")
            contact_id = f"{contact.get('first_name', 'unknown')}_{contact.get('last_name', 'contact')}"
            filename = f"{DATE_STR}_{safe_name}_{contact_id}.md"
            filepath = OUTREACH_DIR / filename
            
            with open(filepath, "w") as f:
                f.write(draft)
            
            all_drafts.append({
                "company": name,
                "domain": domain,
                "contact_email": contact.get("email"),
                "contact_name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip(),
                "contact_position": contact.get("position", ""),
                "draft_file": str(filepath),
                "job_reference": job_info["title"] if job_info else "Generic outreach"
            })
            
            print(f"  ✓ Draft saved: {filename}")
        
        log_entries.append({
            "timestamp": datetime.now().isoformat(),
            "company": name,
            "step": "drafts_generated",
            "drafts_count": len(top_contacts)
        })
        
        # Rate limiting
        time.sleep(1)
    
    # Save outputs
    print("\n=== Saving output files ===")
    
    # Job matches
    job_matches_file = CAREER_DIR / f"job_matches_{DATE_STR}.json"
    with open(job_matches_file, "w") as f:
        json.dump({
            "date": DATE_STR,
            "timestamp": TIMESTAMP,
            "serper_out_of_credits": serper_out_of_credits,
            "matches": all_job_matches
        }, f, indent=2)
    print(f"✓ Job matches: {job_matches_file}")
    
    # Enriched contacts
    contacts_file = CAREER_DIR / f"enriched_contacts_{DATE_STR}.json"
    with open(contacts_file, "w") as f:
        json.dump({
            "date": DATE_STR,
            "timestamp": TIMESTAMP,
            "contacts": all_enriched_contacts
        }, f, indent=2)
    print(f"✓ Enriched contacts: {contacts_file}")
    
    # Automation log
    log_file = CAREER_DIR / f"automation_log_{DATE_STR}.json"
    with open(log_file, "w") as f:
        json.dump({
            "date": DATE_STR,
            "timestamp": TIMESTAMP,
            "companies_processed": len(PRIORITY_COMPANIES),
            "serper_out_of_credits": serper_out_of_credits,
            "total_drafts_generated": len(all_drafts),
            "total_contacts_enriched": sum(c["total_emails_found"] for c in all_enriched_contacts.values()),
            "log_entries": log_entries
        }, f, indent=2)
    print(f"✓ Automation log: {log_file}")
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Companies processed: {len(PRIORITY_COMPANIES)}")
    print(f"Total drafts generated: {len(all_drafts)}")
    print(f"Serper out of credits: {serper_out_of_credits}")
    print(f"Output directory: {OUTREACH_DIR}")

if __name__ == "__main__":
    main()