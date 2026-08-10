#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

# Load enriched contacts
with open('04_RESOURCES/Career/enriched_contacts_2026-08-09.json', 'r') as f:
    data = json.load(f)

# Build mapping: (company_normalized, first_name_lower, last_name_lower) -> email
contact_map = {}
for company_name, info in data['contacts'].items():
    # Normalize company name: remove punctuation, lower
    company_norm = re.sub(r'[^\w\s]', '', company_name).lower().strip()
    for contact in info['top_contacts']:
        first = contact.get('first_name', '').lower().strip()
        last = contact.get('last_name', '').lower().strip()
        email = contact.get('value')
        if email and (first or last):  # ignore empty names
            key = (company_norm, first, last)
            contact_map[key] = email

# Process drafts
drafts_dir = Path('01_INBOX/outreach_drafts')
updated = 0
for draft_file in drafts_dir.glob('*.md'):
    # Read content
    with open(draft_file, 'r') as f:
        content = f.read()
    # Extract parts from filename: YYYY-MM-DD_Company_FirstName_LastName.md
    stem = draft_file.stem  # without .md
    # Remove date prefix (first 10 chars YYYY-MM-DD plus underscore?)
    if stem.startswith('2026-08-08_') or stem.startswith('2026-08-09_'):
        # split by _
        parts = stem.split('_')
        # parts[0] = date, parts[1] = start of company, last two parts are first and last? but company may have spaces.
        # Actually format: YYYY-MM-DD_Company_Name_FirstName_LastName.md
        # So we need to reconstruct: company is everything between date and the last two parts.
        if len(parts) >= 4:
            # date = parts[0]
            # first = parts[-2]
            # last = parts[-1]
            # company_parts = parts[1:-2]
            first = parts[-2]
            last = parts[-1]
            company_parts = parts[1:-2]
            company_name_from_file = ' '.join(company_parts)
        else:
            # fallback: maybe format YYYY-MM-DD_Company_Hiring_Team.md
            # We'll treat as generic and maybe keep first email.
            company_name_from_file = ''
            first = ''
            last = ''
    else:
        # Should not happen
        company_name_from_file = ''
        first = ''
        last = ''
    # Normalize for lookup
    company_norm = re.sub(r'[^\w\s]', '', company_name_from_file).lower().strip()
    first_norm = first.lower().strip()
    last_norm = last.lower().strip()
    # Try to find exact match
    email = None
    if company_norm and (first_norm or last_norm):
        key = (company_norm, first_norm, last_norm)
        email = contact_map.get(key)
    # If not found, try fuzzy: maybe first/last swapped or extra spaces.
    if not email and company_norm:
        # Try to find any contact for this company with matching first or last
        for (c_norm, f_norm, l_norm), e in contact_map.items():
            if c_norm == company_norm:
                # If first matches or last matches (or both empty)
                if (not first_norm or f_norm == first_norm) and (not last_norm or l_norm == last_norm):
                    email = e
                    break
    # If still not found, fall back to first email for that company (if any)
    if not email and company_name_from_file:
        # Find company in enriched contacts
        for c_name, info in data['contacts'].items():
            if re.sub(r'[^\w\s]', '', c_name).lower().strip() == company_norm:
                if info['top_contacts']:
                    email = info['top_contacts'][0].get('value')
                break
    # If email found, replace the to: line
    if email:
        new_content = re.sub(r'(to: )\s*(\n)', r'\1' + email + r'\2', content)
        if new_content != content:
            with open(draft_file, 'w') as f:
                f.write(new_content)
            updated += 1
            print(f"Updated {draft_file.name} -> {email} (company: {company_name_from_file}, first: {first}, last: {last})")
        else:
            # No change needed maybe already correct
            pass
    else:
        # Leave as is (maybe empty)
        print(f"No email found for {draft_file.name} (company: {company_name_from_file}, first: {first}, last: {last})")

print(f"\nUpdated {updated} draft files.")
