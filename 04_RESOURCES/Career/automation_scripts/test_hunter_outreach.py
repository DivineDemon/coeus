#!/usr/bin/env python3
"""
Focused test: Use Hunter.io to find contacts at priority companies and generate outreach drafts
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('/Users/mushood/.hermes/.env')

HUNTER_API_KEY = os.getenv('HUNTER_API_KEY')
RESEND_API_KEY = os.getenv('RESEND_API_KEY')

BASE_DIR = Path('/Users/mushood/Documents/code/personal/coeus')
CAREER_DIR = BASE_DIR / '04_RESOURCES/Career'
INBOX_DIR = BASE_DIR / '01_INBOX/outreach_drafts'
INBOX_DIR.mkdir(parents=True, exist_ok=True)

TODAY = datetime.now().strftime('%Y-%m-%d')

# Load priority sponsors
with open(CAREER_DIR / 'priority_sponsors.json') as f:
    sponsors = json.load(f)

tier_1 = sponsors.get('priority_tier_1', [])
tier_2 = sponsors.get('priority_tier_2', [])
all_companies = tier_1 + tier_2

print(f"Testing with {len(all_companies)} companies (Tier 1: {len(tier_1)}, Tier 2: {len(tier_2)})")

# Target positions to look for
TARGET_POSITIONS = [
    'cto', 'chief technology officer', 'vp engineering', 'vice president engineering',
    'head of engineering', 'head of ai', 'head of robotics', 'head of research',
    'director of engineering', 'director of ai', 'director of robotics',
    'engineering manager', 'hiring manager', 'technical recruiter',
    'talent acquisition', 'recruiter', 'lead engineer', 'principal engineer',
    'staff engineer', 'senior engineering manager'
]

def hunter_domain_search(domain):
    """Search for emails at a domain using Hunter.io"""
    url = "https://api.hunter.io/v2/domain-search"
    params = {'domain': domain, 'api_key': HUNTER_API_KEY, 'limit': 10}  # Max 10 per API
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  Hunter error for {domain}: {e}")
        return {}

def get_target_contacts(company, domain_search_result):
    """Identify target contacts from Hunter results"""
    contacts = []
    emails = domain_search_result.get('data', {}).get('emails', [])
    
    for email_data in emails:
        position = (email_data.get('position') or '').lower()
        first_name = email_data.get('first_name', '')
        last_name = email_data.get('last_name', '')
        email = email_data.get('value', '')
        confidence = email_data.get('confidence', 0)
        
        if any(target in position for target in TARGET_POSITIONS) and confidence > 50:
            contacts.append({
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'position': email_data.get('position', ''),
                'confidence': confidence,
            })
    
    return contacts

def generate_outreach_email(company, contact):
    """Generate personalized outreach email"""
    contact_name = f"{contact['first_name']} {contact['last_name']}".strip()
    if not contact_name or contact_name.lower() in ['engineering hiring', 'hiring team']:
        contact_name = "Hiring Team"
    
    # Company-specific tech from keywords
    company_keywords = company.get('keywords', [])
    company_tech = company_keywords[0] if company_keywords else "physical AI and robotics"
    
    subject = f"Senior AI/Robotics Engineer at {company['name']} — Physics Verification for Physical AI (Haga)"
    
    body = f"""Hi {contact_name},

Saw that {company['name']} is an A-rated Skilled Worker sponsor — the focus on {company_tech} caught my eye.

I'm the founder of Haga (haga.mushoodhanif.com), where we build independent physics verification for robot learning policies and generative world models. Our benchmark stresses policies under adversarial mass/friction perturbations in MuJoCo/Robosuite (Lift, Stack, Door, PickPlaceCan) and scores physics consistency in generated video (CogVideoX, Physics-IQ) via calibrated detectors — permanence, ballistic, contact, static-hover.

Your work on {company_tech} aligns closely with the sim-to-real gap we're closing. I'd love a 15-min technical conversation to explore fit. Happy to share our Lab evidence (public metrics at haga.mushoodhanif.com/lab).

Note: {company['name']} is listed as an A-rated Skilled Worker sponsor on the UK Home Office register — I'd need sponsorship to join.

Best,
Mushood Hanif
Founder, Haga | haga.mushoodhanif.com
GitHub: DivineDemon/haga-core"""
    
    html_body = body.replace('\n', '<br>')
    
    return {
        'to': contact['email'],
        'subject': subject,
        'body': body,
        'html_body': html_body,
        'contact_name': contact_name,
    }

def save_outreach_draft(email_data, company_name):
    """Save outreach draft as markdown file"""
    safe_company = company_name.replace(' ', '_').replace('.', '').replace('/', '_').replace('&', 'and')
    filename = f"{safe_company}_{TODAY}.md"
    filepath = INBOX_DIR / filename
    
    content = f"""# Outreach Draft

**To:** {email_data['to']}
**Subject:** {email_data['subject']}
**Date:** {TODAY}
**Company:** {company_name}
**Contact:** {email_data['contact_name']}

---

{email_data['body']}

---

## HTML Version

{email_data['html_body']}
"""
    
    filepath.write_text(content)
    return str(filepath)

def log_to_local_crm(email_data, draft_path, company, contact):
    """Log outreach to local CRM file"""
    log_file = CAREER_DIR / 'outreach_crm.json'
    
    # Load existing
    if log_file.exists():
        with open(log_file) as f:
            crm_data = json.load(f)
    else:
        crm_data = {'entries': []}
    
    entry = {
        'id': len(crm_data['entries']) + 1,
        'company': company['name'],
        'role': 'Senior AI/Robotics Engineer',
        'contact_email': contact['email'],
        'contact_name': email_data['contact_name'],
        'contact_position': contact['position'],
        'email_draft_path': draft_path,
        'sent_status': 'drafted',
        'response_status': 'pending',
        'pipeline_stage': 'Drafted',
        'created_at': datetime.now().isoformat(),
        'sponsor_tier': company.get('tier', 1),
        'company_domain': company.get('domain', ''),
    }
    
    crm_data['entries'].append(entry)
    
    with open(log_file, 'w') as f:
        json.dump(crm_data, f, indent=2)
    
    return entry

def send_resend_email(email_data):
    """Send email via Resend API"""
    if not RESEND_API_KEY:
        print("  Resend API key not configured")
        return False
    
    url = "https://api.resend.com/emails"
    headers = {'Authorization': f'Bearer {RESEND_API_KEY}', 'Content-Type': 'application/json'}
    payload = {
        'from': 'Mushood Hanif <haga@mushoodhanif.com>',
        'to': [email_data['to']],
        'subject': email_data['subject'],
        'html': email_data['html_body'],
        'text': email_data['body'],
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code in (200, 201):
            print(f"  ✓ Email sent via Resend to {email_data['to']}")
            return True
        else:
            print(f"  ✗ Resend error: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"  ✗ Resend exception: {e}")
    return False

# Main execution
print(f"\n{'='*60}")
print(f"HUNTER.IO CONTACT ENRICHMENT & OUTREACH GENERATION")
print(f"{'='*60}\n")

all_contacts = []
drafts_created = 0
companies_with_contacts = []

for company in all_companies[:10]:  # Test with first 10 companies
    domain = company.get('domain', '')
    if not domain:
        continue
    
    print(f"\n🔍 {company['name']} ({domain})")
    
    result = hunter_domain_search(domain)
    contacts = get_target_contacts(company, result)
    
    if not contacts:
        print(f"  No target contacts found")
        continue
    
    companies_with_contacts.append(company['name'])
    
    for contact in contacts[:3]:  # Limit to 3 contacts per company
        all_contacts.append({
            'company': company['name'],
            'domain': domain,
            'contact': contact,
        })
        
        print(f"  ✓ {contact['first_name']} {contact['last_name']} - {contact['position']} ({contact['email']}) [conf={contact['confidence']}]")
        
        # Generate outreach
        email_data = generate_outreach_email(company, contact)
        draft_path = save_outreach_draft(email_data, company['name'])
        
        # Log to local CRM
        log_to_local_crm(email_data, draft_path, company, contact)
        
        drafts_created += 1
        print(f"    📝 Draft saved: {draft_path}")

print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"Companies checked: 10")
print(f"Companies with target contacts: {len(companies_with_contacts)}")
print(f"Total contacts found: {len(all_contacts)}")
print(f"Outreach drafts created: {drafts_created}")
print(f"Companies: {', '.join(companies_with_contacts)}")

# Save enriched contacts
enriched_file = CAREER_DIR / f'enriched_contacts_{TODAY}.json'
enriched_file.write_text(json.dumps({
    'date': TODAY,
    'total_contacts': len(all_contacts),
    'contacts': all_contacts
}, indent=2))
print(f"\n💾 Saved enriched contacts to {enriched_file}")