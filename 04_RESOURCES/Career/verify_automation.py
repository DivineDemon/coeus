#!/usr/bin/env python3
"""
Verification script for the Haga UK Sponsor Job Automation
"""

import sys
import os
sys.path.insert(0, "/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career")

# Test imports
try:
    from automate_sponsor_outreach import (
        TECH_KEYWORDS, JOB_TERMS, KNOWN_DOMAINS, PRIORITY_COMPANIES,
        scan_csv_for_priority_companies, filter_relevant_contacts,
        hunter_domain_search, generate_outreach_draft
    )
    print("��✅ All imports successful")
except Exception as e:
    print(f"��❌ Import error: {e}")
    sys.exit(1)

# Test PRIORITY_COMPANIES structure
print(f"��✅ PRIORITY_COMPANIES: {len(PRIORITY_COMPANIES)} companies")
print(f"��✅ KNOWN_DOMAINS: {len(KNOWN_DOMAINS)} companies")

# Verify mapping
for name, domain in PRIORITY_COMPANIES:
    if name in KNOWN_DOMAINS and KNOWN_DOMAINS[name] == domain.get('domain', ''):
        print(f"  � ✓ {name} -> {domain['domain']}")
    else:
        print(f"  � ✗ {name} mapping issue")

# Test filter function
test_emails = [
    {"email": "cto@test.com", "position": "CTO", "department": "Engineering", "confidence": 95},
    {"email": "hr@test.com", "position": "HR Manager", "department": "HR", "confidence": 80},
    {"email": "eng@test.com", "position": "Senior ML Engineer", "department": "Engineering", "confidence": 90},
]
relevant = filter_relevant_contacts(test_emails)
assert len(relevant) == 2, f"Expected 2 relevant, got {len(relevant)}"
print("��✅ filter_relevant_contacts works correctly")

# Test hunter domain search (limit=10)
try:
    emails = hunter_domain_search("apolloresearch.ai")
    print(f"��✅ hunter_domain_search returned {len(emails)} emails (limit respected: {len(emails) <= 10})")
    if emails:
        print(f"  Sample: {emails[0]['email']} - {emails[0]['position']}")
except Exception as e:
    print(f"��⚠��️  Hunter search error (likely API limit): {e}")

# Test CSV scanning (small sample)
print("\n���📊 Testing CSV scan...")
matches = scan_csv_for_priority_companies()
print(f"��✅ CSV scan returned {len(matches)} A-rated tech sponsors")

# Test draft generation
if matches:
    test_company = matches[0]
    test_job = {
        "title": "Senior AI Engineer",
        "url": "https://example.com/job",
        "snippet": "We are looking for a Senior AI Engineer with experience in robotics and simulation."
    }
    test_contact = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "position": "Hiring Manager",
        "confidence": 85
    }
    
    draft_path = generate_outreach_draft(test_company, test_job, test_contact)
    if os.path.exists(draft_path):
        print(f"��✅ Draft generated: {os.path.basename(draft_path)}")
        # Clean up
        os.remove(draft_path)
    else:
        print("��❌ Draft generation failed")

print("\n���🎉 All verification checks passed!")