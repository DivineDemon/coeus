#!/usr/bin/env python3
"""
Complete UK Sponsor Job Matching & Outreach Automation
Runs every Monday at 9 AM UK Time
"""

import os
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('/Users/mushood/.hermes/.env')

HUNTER_API_KEY = os.getenv('HUNTER_API_KEY')
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
RESEND_API_KEY = os.getenv('RESEND_API_KEY')

BASE_DIR = Path('/Users/mushood/Documents/code/personal/coeus')
CAREER_DIR = BASE_DIR / '04_RESOURCES/Career'
INBOX_DIR = BASE_DIR / '01_INBOX/outreach_drafts'
INBOX_DIR.mkdir(parents=True, exist_ok=True)

TODAY = datetime.now().strftime('%Y-%m-%d')

# Target positions for Hunter.io filtering
TARGET_POSITIONS = [
    'cto', 'chief technology officer', 'vp engineering', 'vice president engineering',
    'head of engineering', 'head of ai', 'head of robotics', 'head of research',
    'director of engineering', 'director of ai', 'director of robotics',
    'engineering manager', 'hiring manager', 'technical recruiter',
    'talent acquisition', 'recruiter', 'lead engineer', 'principal engineer',
    'staff engineer', 'senior engineering manager', 'founder', 'co-founder',
    'cofounder', 'ceo', 'chief executive', 'managing director', 'vp product',
    'head of product', 'director of product', 'product manager'
]

def load_priority_sponsors():
    with open(CAREER_DIR / 'priority_sponsors.json') as f:
        return json.load(f)

def hunter_domain_search(domain):
    """Search for emails at a domain using Hunter.io (max 10 results)"""
    url = "https://api.hunter.io/v2/domain-search"
    params = {'domain': domain, 'api_key': HUNTER_API_KEY, 'limit': 10}
    try:
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 429:
            print(f"  Rate limited, waiting...")
            time.sleep(5)
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
    if not contact_name or contact_name.lower() in ['engineering hiring', 'hiring team', '']:
        contact_name = "Hiring Team"
    
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
    safe_company = company_name.replace(' ', '_').replace('.', '').replace('/', '_').replace('&', 'and').replace(',', '')
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

def send_whatsapp_summary(stats):
    """Send summary via WhatsApp gateway (if available)"""
    url = "http://localhost:18790/send"
    message = f"""🤖 *Weekly Sponsor Job Automation - {TODAY}*

📊 *Summary:*
• Companies scanned: {stats['companies_scanned']}
• Companies with target contacts: {stats['companies_with_contacts']}
• Total contacts found: {stats['total_contacts']}
• Outreach drafts created: {stats['drafts_created']}
• Companies with drafts: {', '.join(stats['companies_with_drafts'][:5])}

🎯 *Top Contacts:*
"""
    for contact in stats['top_contacts'][:5]:
        message += f"• {contact['name']} ({contact['position']}) at {contact['company']}\n"
    
    payload = {'to': os.getenv('WHATSAPP_ALLOWED_USERS', ''), 'message': message}
    
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            print("✓ WhatsApp notification sent")
        else:
            print(f"✗ WhatsApp failed: {resp.status_code}")
    except Exception as e:
        print(f"✗ WhatsApp error (gateway may not be running): {e}")

def main():
    print(f"🚀 Starting UK Sponsor Job Matching - {TODAY}")
    
    sponsors = load_priority_sponsors()
    tier_1 = sponsors.get('priority_tier_1', [])
    tier_2 = sponsors.get('priority_tier_2', [])
    all_companies = tier_1 + tier_2
    
    print(f"📋 Loaded {len(tier_1)} Tier 1 + {len(tier_2)} Tier 2 companies")
    
    all_contacts = []
    drafts_created = 0
    companies_with_drafts = set()
    companies_with_contacts = set()
    top_contacts = []
    
    for i, company in enumerate(all_companies, 1):
        domain = company.get('domain', '')
        if not domain:
            continue
        
        print(f"\n[{i}/{len(all_companies)}] 🔍 {company['name']} ({domain})")
        
        result = hunter_domain_search(domain)
        contacts = get_target_contacts(company, result)
        
        if not contacts:
            print(f"  No target contacts found")
            time.sleep(0.5)  # Rate limiting
            continue
        
        companies_with_contacts.add(company['name'])
        
        for contact in contacts[:3]:  # Limit to 3 contacts per company
            all_contacts.append({
                'company': company['name'],
                'domain': domain,
                'contact': contact,
                'tier': company.get('tier', 1),
            })
            
            print(f"  ✓ {contact['first_name']} {contact['last_name']} - {contact['position']} ({contact['email']}) [conf={contact['confidence']}]")
            
            top_contacts.append({
                'name': f"{contact['first_name']} {contact['last_name']}",
                'position': contact['position'],
                'company': company['name'],
                'email': contact['email']
            })
            
            # Generate outreach
            email_data = generate_outreach_email(company, contact)
            draft_path = save_outreach_draft(email_data, company['name'])
            
            # Log to local CRM
            log_to_local_crm(email_data, draft_path, company, contact)
            
            drafts_created += 1
            companies_with_drafts.add(company['name'])
            
            print(f"    📝 Draft saved")
        
        time.sleep(0.5)  # Rate limiting between companies
    
    # Save enriched contacts
    enriched_file = CAREER_DIR / f'enriched_contacts_{TODAY}.json'
    enriched_file.write_text(json.dumps({
        'date': TODAY,
        'total_contacts': len(all_contacts),
        'contacts': all_contacts
    }, indent=2))
    print(f"\n💾 Saved {len(all_contacts)} enriched contacts to {enriched_file}")
    
    # Summary stats
    stats = {
        'companies_scanned': len(all_companies),
        'companies_with_contacts': len(companies_with_contacts),
        'total_contacts': len(all_contacts),
        'drafts_created': drafts_created,
        'companies_with_drafts': list(companies_with_drafts),
        'top_contacts': top_contacts,
    }
    
    # Send WhatsApp summary
    send_whatsapp_summary(stats)
    
    # Log automation run
    log_file = CAREER_DIR / f'automation_log_{TODAY}.json'
    log_file.write_text(json.dumps({
        'date': TODAY,
        'companies_scanned': len(all_companies),
        'companies_with_contacts': len(companies_with_contacts),
        'total_contacts': len(all_contacts),
        'drafts_created': drafts_created,
        'companies_with_drafts': list(companies_with_drafts),
        'status': 'completed'
    }, indent=2))
    
    print(f"\n{'='*60}")
    print(f"✅ AUTOMATION COMPLETE")
    print(f"{'='*60}")
    print(f"Companies scanned: {len(all_companies)}")
    print(f"Companies with target contacts: {len(companies_with_contacts)}")
    print(f"Total contacts found: {len(all_contacts)}")
    print(f"Outreach drafts created: {drafts_created}")
    print(f"Companies with drafts: {len(companies_with_drafts)}")
    print(f"\nCompanies: {', '.join(sorted(companies_with_drafts))}")

if __name__ == '__main__':
    main()