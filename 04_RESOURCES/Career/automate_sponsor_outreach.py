#!/usr/bin/env python3
"""
Automated UK Sponsor Job Matching & Outreach for Mushood Hanif
Run weekly to find jobs at A-rated sponsors and generate personalized outreach drafts.
"""

import os
import json
import csv
import re
import requests
import base64
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/Users/mushood/Documents/code/personal/coeus/.env.local")

# Configuration
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

# API Keys
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Keywords for matching companies
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

# Known domains for priority companies
KNOWN_DOMAINS = {
    "JBS Applied A.I & Robotics Research Ltd": "jbs-ai-robotics.com",
    "Shadow Robot Company Ltd.": "shadowrobot.com",
    "Apollo Research AI Ltd": "apolloresearch.ai",
    "CGA Simulation Ltd": "cga-simulation.com",
    "HPi Verification Services Ltd": "hpi-verification.com",
    "Fieldwork Robotics Limited": "fieldworkrobotics.com",
    "Oxford Robotics Ltd": "oxfordrobotics.institute",
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

# Priority companies built from KNOWN_DOMAINS
PRIORITY_COMPANIES = [
    {"name": name, "location": "London", "domain": domain, "keywords": []}
    for name, domain in KNOWN_DOMAINS.items()
]


def scan_csv_for_priority_companies():
    """Scan the full CSV for A-rated sponsors matching tech keywords"""
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

            # Only A-rated Skilled Worker sponsors
            if 'A rating' not in sponsor_type or 'Skilled Worker' not in route:
                continue

            org_lower = org.lower()
            key = f"{org_lower}_{city.lower()}"
            if key in seen:
                continue

            # Check for tech keywords
            matched_keywords = [kw for kw in TECH_KEYWORDS if kw in org_lower]
            if matched_keywords:
                # Exclude obvious non-tech
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
                        "name": org,
                        "city": city,
                        "county": county,
                        "sponsor_type": sponsor_type,
                        "route": route,
                        "matched_keywords": matched_keywords[:5]
                    })
                    seen.add(key)

    return matches


def search_jobs_serper(company_name, domain=None):
    """Search for job postings using Serper API"""
    if not SERPER_API_KEY:
        print("  ⚠️  SERPER_API_KEY not set, skipping job search")
        return []

    if domain:
        query = f'site:{domain} ("Senior AI" OR "ML Engineer" OR "Robotics Engineer" OR "Research Scientist" OR "Simulation Engineer" OR "Physics Engineer" OR "Computer Vision") careers jobs'
    else:
        query = f'"{company_name}" ("Senior AI Engineer" OR "ML Engineer" OR "Robotics Engineer" OR "Research Scientist" OR "Simulation Engineer") careers jobs UK'

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 10}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            jobs = []
            for result in data.get("organic", []):
                jobs.append({
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "company": company_name
                })
            return jobs
    except Exception as e:
        print(f"  ❌ Serper error for {company_name}: {e}")
    return []


def find_company_domain(company_name):
    """Try to find company domain via search"""
    if not SERPER_API_KEY:
        return None

    query = f'"{company_name}" official website'
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 5}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            for result in data.get("organic", []):
                link = result.get("link", "")
                from urllib.parse import urlparse
                parsed = urlparse(link)
                domain = parsed.netloc.replace("www.", "")
                if domain and not any(x in domain for x in ["linkedin", "glassdoor", "indeed", "github", "crunchbase"]):
                    return domain
    except Exception as e:
        print(f"  ❌ Domain search error for {company_name}: {e}")
    return None


def hunter_domain_search(domain):
    """Search for emails at a domain using Hunter.io"""
    if not HUNTER_API_KEY:
        print("  ⚠️  HUNTER_API_KEY not set")
        return []

    url = f"https://api.hunter.io/v2/domain-search"
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
                    "department": email_data.get("department")
                })
            return emails
    except Exception as e:
        print(f"  ❌ Hunter domain search error for {domain}: {e}")
    return []


def filter_relevant_contacts(emails):
    """Filter for engineering/hiring/leadership roles"""
    relevant = []
    target_keywords = [
        "engineer", "engineering", "cto", "vp", "head", "lead", "principal",
        "director", "manager", "hiring", "talent", "recruit", "technical",
        "research", "science", "robotics", "ai", "ml", "machine learning",
        "simulation", "physics", "computer vision", "autonomy", "autonomous"
    ]

    for e in emails:
        position = (e.get("position") or "").lower()
        department = (e.get("department") or "").lower()

        if any(kw in position for kw in target_keywords) or any(kw in department for kw in target_keywords):
            relevant.append(e)

    return relevant


def generate_outreach_draft(company, job, contact):
    """Generate personalized outreach email draft"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_company = re.sub(r'[^\w\s-]', '', company["name"]).replace(" ", "_")
    safe_role = re.sub(r'[^\w\s-]', '', job.get("title", "Role")).replace(" ", "_")[:50]

    filename = f"{safe_company}_{safe_role}_{date_str}.md"
    filepath = Path(DRAFTS_DIR) / filename

    job_snippet = job.get("snippet", "")
    company_name = company["name"]

    company_tech_map = {
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

    company_tech = "cutting-edge robotics and simulation"
    for key, val in company_tech_map.items():
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

    filepath.write_text(draft)
    return str(filepath)


def send_email_resend(to_email, subject, html_body, text_body, attachment_path=None):
    """Send email via Resend API with optional attachment"""
    if not RESEND_API_KEY:
        print("  ⚠️  RESEND_API_KEY not set, skipping email send")
        return False

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "from": "Mushood Hanif <haga@mushoodhanif.com>",
        "to": [to_email],
        "subject": subject,
        "html": html_body,
        "text": text_body
    }

    if attachment_path and Path(attachment_path).exists():
        with open(attachment_path, "rb") as f:
            file_content = base64.b64encode(f.read()).decode()
        payload["attachments"] = [{
            "filename": "Mushood_Hanif_Resume.pdf",
            "content": file_content
        }]

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            print(f"  ✅ Email sent to {to_email} via Resend")
            return True
        else:
            print(f"  ❌ Resend error: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        print(f"  ❌ Resend exception: {e}")
        return False


def main():
    print("=" * 60)
    print("🤖 HAGA UK SPONSOR JOB AUTOMATION")
    print(f"⏰ Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Step 1: Scan CSV for priority companies
    print("\n📊 Step 1: Scanning UK Sponsor Register CSV...")
    csv_matches = scan_csv_for_priority_companies()
    print(f"   Found {len(csv_matches)} A-rated tech sponsors in CSV")

    # Merge with priority list
    all_companies = PRIORITY_COMPANIES + [
        {**m, "keywords": m["matched_keywords"]} for m in csv_matches
        if m["name"] not in [p["name"] for p in PRIORITY_COMPANIES]
    ]
    print(f"   Total companies to process: {len(all_companies)}")

    # Save updated priority list
    priority_data = {
        "updated": datetime.now().isoformat(),
        "total_companies": len(all_companies),
        "priority_tier_1": PRIORITY_COMPANIES,
        "csv_discovered": csv_matches[:50]
    }
    Path(PRIORITY_JSON).write_text(json.dumps(priority_data, indent=2))
    print(f"   ✅ Saved priority list to {PRIORITY_JSON}")

    # Step 2-4: Process each priority company
    print("\n🔍 Step 2-4: Finding jobs, enriching contacts, generating drafts...")

    date_str = datetime.now().strftime("%Y-%m-%d")
    all_jobs = []
    all_contacts = []
    all_drafts = []

    # Process Tier 1 companies (limit to 5 for first run)
    for i, company in enumerate(PRIORITY_COMPANIES[:5]):
        print(f"\n   [{i+1}/5] Processing: {company['name']}")

        domain = company.get("domain")
        if domain:
            print(f"      🌐 Domain: {domain}")
        else:
            print(f"      ⚠️  No known domain, searching...")
            domain = find_company_domain(company["name"])
            if not domain:
                name_clean = re.sub(r'[^\w]', '', company["name"].lower().replace(" ", ""))
                domain = f"{name_clean}.com"
                print(f"      🔄 Trying guessed domain: {domain}")

        # Search for jobs
        jobs = search_jobs_serper(company["name"], domain)
        print(f"      💼 Found {len(jobs)} potential job postings")

        for job in jobs[:3]:
            job["company_name"] = company["name"]
            job["company_location"] = company.get("location", "")
            all_jobs.append(job)

        # ALWAYS enrich contacts for priority companies (even without specific job postings)
        emails = hunter_domain_search(domain)
        print(f"      📧 Hunter found {len(emails)} emails at {domain}")

        relevant = filter_relevant_contacts(emails)
        print(f"      🎯 {len(relevant)} relevant engineering/hiring contacts")

        # If no specific jobs found, use generic "Careers" as fallback
        job_contexts = jobs[:3] if jobs else [{
            "title": "Careers / Opportunities",
            "url": f"https://{domain}/careers" if domain else "",
            "snippet": f"Exploring opportunities at {company['name']} in robotics, AI, simulation, or related fields."
        }]

        # Only generate drafts if we have relevant contacts
        if relevant:
            for job in job_contexts:
                # For each job context, create drafts for top contacts
                for contact in relevant[:3]:
                    contact["company"] = company["name"]
                    contact["domain"] = domain
                    all_contacts.append(contact)

                    # Generate draft
                    draft_path = generate_outreach_draft(company, job, contact)
                    all_drafts.append({
                        "draft_path": draft_path,
                        "company": company["name"],
                        "job_title": job.get("title"),
                        "contact_email": contact.get("email"),
                        "contact_name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}"
                    })
                    print(f"      ✍️  Draft created: {Path(draft_path).name}")
        else:
            print(f"      ⏭️  Skipping drafts - no relevant contacts found")

    # Save outputs
    print("\n💾 Saving outputs...")

    jobs_file = Path(JOBS_DIR) / f"job_matches_{date_str}.json"
    jobs_file.write_text(json.dumps(all_jobs, indent=2))
    print(f"   ✅ Jobs: {jobs_file}")

    contacts_file = Path(CONTACTS_DIR) / f"enriched_contacts_{date_str}.json"
    contacts_file.write_text(json.dumps(all_contacts, indent=2))
    print(f"   ✅ Contacts: {contacts_file}")

    # Log
    log_data = {
        "run_date": date_str,
        "run_time": datetime.now().isoformat(),
        "companies_processed": len(PRIORITY_COMPANIES[:5]),
        "jobs_found": len(all_jobs),
        "contacts_enriched": len(all_contacts),
        "drafts_generated": len(all_drafts),
        "drafts": all_drafts
    }
    log_file = Path(LOG_DIR) / f"automation_log_{date_str}.json"
    log_file.write_text(json.dumps(log_data, indent=2))
    print(f"   ✅ Log: {log_file}")

    # Summary
    print("\n" + "=" * 60)
    print("📋 RUN SUMMARY")
    print("=" * 60)
    print(f"Companies processed: {len(PRIORITY_COMPANIES[:5])}")
    print(f"Job postings found: {len(all_jobs)}")
    print(f"Contacts enriched: {len(all_contacts)}")
    print(f"Outreach drafts created: {len(all_drafts)}")
    print(f"\n📁 Drafts in: {DRAFTS_DIR}")
    print(f"📁 Logs in: {LOG_DIR}")

    if all_drafts:
        print("\n📧 Drafts ready for review:")
        for d in all_drafts:
            print(f"   • {d['company']} — {d['job_title']} → {d['contact_name']} ({d['contact_email']})")

    # WhatsApp notification
    try:
        whatsapp_msg = f"""🤖 *Haga Job Automation Run Complete* ({date_str})

📊 *Results:*
• Companies processed: {len(PRIORITY_COMPANIES[:5])}
• Job postings found: {len(all_jobs)}
• Contacts enriched: {len(all_contacts)}
• Outreach drafts created: {len(all_drafts)}

📧 *Drafts ready for review:*
{chr(10).join([f'• {d["company"]} — {d["job_title"]}' for d in all_drafts[:5]])}

📁 Drafts: `01_INBOX/outreach_drafts/`
"""
        resp = requests.post("http://localhost:18790/send",
                           json={"message": whatsapp_msg}, timeout=5)
        if resp.status_code == 200:
            print("\n📱 WhatsApp notification sent!")
        else:
            print("\n📱 WhatsApp gateway not available (port 18790)")
    except Exception as e:
        print(f"\n📱 WhatsApp notification skipped: {e}")

    print("\n✅ Automation complete!")


if __name__ == "__main__":
    main()