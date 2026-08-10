#!/usr/bin/env python3
"""
Fill email addresses in outreach draft files based on enriched contacts data
"""

import json
import os
import re
from pathlib import Path

# Load enriched contacts
with open('04_RESOURCES/Career/enriched_contacts_2026-08-09.json', 'r') as f:
    data = json.load(f)

# Build email mapping: company -> list of emails
email_map = {}
for company_name, info in data['contacts'].items():
    emails = []
    if info['top_contacts']:
        for contact in info['top_contacts']:
            if contact.get('value'):
                emails.append(contact['value'])
    email_map[company_name] = emails

# Process all draft files
drafts_dir = Path('01_INBOX/outreach_drafts')
filled_count = 0

for draft_file in drafts_dir.glob('*.md'):
    # Extract company name from filename
    # Format: YYYY-MM-DD_Company_Name_FirstName_LastName.md
    # or YYYY-MM-DD_Company_Name_Hiring_Team.md
    filename = draft_file.stem  # removes .md
    
    # Remove date prefix
    if '_' in filename:
        parts = filename.split('_', 2)  # Split into max 3 parts: date, rest
        if len(parts) >= 2:
            company_part = parts[1]  # This might be just first part of company name
            
            # Special handling: if we have more parts and the next part looks like continuation
            if len(parts) >= 3:
                # Check if parts[2] looks like a person name (starts with capital) or "Hiring"
                if parts[2][0].isupper() if parts[2] else False or parts[2] in ['Hiring', 'Team']:
                    # Company name might be parts[1] + ' ' + parts[2] etc until we hit a person name
                    # But simpler approach: try to match against known company names
                    pass
            
            # Try to find matching company in email_map
            matched_company = None
            for company in email_map.keys():
                # Normalize for comparison: remove punctuation, extra spaces
                norm_company = re.sub(r'[^\w\s]', '', company).lower().strip()
                norm_filename_part = re.sub(r'[^\w\s]', '', filename.split('_')[1]).lower().strip()
                
                # Check if filename part is in company name or vice versa
                if (norm_filename_part in norm_company or 
                    norm_company in norm_filename_part or
                    company.lower() in filename.lower() or
                    filename.lower() in company.lower()):
                    matched_company = company
                    break
            
            if matched_company and email_map[matched_company]:
                # Read the draft
                with open(draft_file, 'r') as f:
                    content = f.read()
                
                # Replace the empty "to: " line with first email
                # Pattern: to: \n
                new_content = re.sub(
                    r'(to: )\s*(\n)',
                    r'\1' + email_map[matched_company][0] + r'\2',
                    content
                )
                
                # Write back
                with open(draft_file, 'w') as f:
                    f.write(new_content)
                
                filled_count += 1
                print(f"Filled {draft_file.name} -> {email_map[matched_company][0]}")

print(f"\nFilled {filled_count} draft files with email addresses")
