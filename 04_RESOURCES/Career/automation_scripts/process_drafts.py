#!/usr/bin/env python3
import json
import re
from pathlib import Path

# Load enriched contacts
with open('04_RESOURCES/Career/enriched_contacts_2026-08-09.json', 'r') as f:
    data = json.load(f)

# Build a dict: (company_name_normalized, first_name_normalized, last_name_normalized) -> email
contact_map = {}
for company_name, info in data['contacts'].items():
    # Normalize company name: remove punctuation, lower, and extra spaces
    company_norm = re.sub(r'[^\w\s]', '', company_name).lower().strip()
    for contact in info['top_contacts']:
        first = (contact.get('first_name') or '').strip()
        last = (contact.get('last_name') or '').strip()
        email = contact.get('value')
        if email and (first or last):
            first_norm = first.lower().strip()
            last_norm = last.lower().strip()
            key = (company_norm, first_norm, last_norm)
            contact_map[key] = email

# Process drafts
drafts_dir = Path('01_INBOX/outreach_drafts')
updated = 0
deleted = 0
kept_no_email = 0  # files we kept but left email empty (should be none if we delete unmatched)
for draft_file in drafts_dir.glob('*.md'):
    # Read the content
    with open(draft_file, 'r') as f:
        content = f.read()
    
    # Extract from filename: YYYY-MM-DD_Company_FirstName_LastName.md
    stem = draft_file.stem  # without .md
    # Remove date prefix: we know the date is either 2026-08-08 or 2026-08-09
    if stem.startswith('2026-08-08_') or stem.startswith('2026-08-09_'):
        # Remove the date and the following underscore
        rest = stem[11:]  # length of '2026-08-08_' or '2026-08-09_' is 11
        # Now split the rest by underscores
        parts = rest.split('_')
        # The last two parts should be first and last name (if present)
        # Everything before that is the company name (which may have been split by underscores)
        if len(parts) >= 2:
            # Assume the last two are first and last
            last_part = parts[-1]
            first_part = parts[-2] if len(parts) >= 2 else ''
            # The company name is the rest (if any)
            company_parts = parts[:-2] if len(parts) > 2 else []
            company_name_from_file = ' '.join(company_parts)
            first_from_file = first_part
            last_from_file = last_part
        else:
            # Not enough parts to have a person name
            company_name_from_file = rest
            first_from_file = ''
            last_from_file = ''
    else:
        # Should not happen with our files, but just in case
        company_name_from_file = stem
        first_from_file = ''
        last_from_file = ''
    
    # Normalize for matching
    company_norm = re.sub(r'[^\w\s]', '', company_name_from_file).lower().strip()
    first_norm = first_from_file.lower().strip()
    last_norm = last_from_file.lower().strip()
    
    # Try to find an exact match for the person at the company
    email = None
    if company_norm and (first_norm or last_norm):
        key = (company_norm, first_norm, last_norm)
        email = contact_map.get(key)
    
    if email:
        # Replace the line that starts with 'to: ' (and possibly spaces) until the newline
        # We want to keep the newline after the email.
        new_content = re.sub(r'^to: \s*$', f'to: {email}', content, flags=re.MULTILINE)
        if new_content == content:
            # Try another pattern: maybe there is no newline after? but we expect a newline.
            # Let's replace the 'to: ' line and the following newline if it's empty.
            new_content = re.sub(r'(to: )\s*\n', rf'\1{email}\n', content)
        if new_content != content:
            with open(draft_file, 'w') as f:
                f.write(new_content)
            updated += 1
            # print(f"Updated {draft_file.name} -> {email}")
        else:
            # Already correct or format unexpected
            pass
    else:
        # No match found. Delete the file.
        draft_file.unlink()
        deleted += 1
        # print(f"Deleted {draft_file.name} (no email match)")

print(f"Updated: {updated}, Deleted: {deleted}")
