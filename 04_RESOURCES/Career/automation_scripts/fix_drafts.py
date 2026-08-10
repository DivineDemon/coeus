#!/usr/bin/env python3
import json
import re
from pathlib import Path

# Load enriched contacts
with open('04_RESOURCES/Career/enriched_contacts_2026-08-09.json', 'r') as f:
    data = json.load(f)

# Build a dict: company_name -> list of contacts with normalized names
company_contacts = {}
for company_name, info in data['contacts'].items():
    contacts_list = []
    for contact in info['top_contacts']:
        first = (contact.get('first_name') or '').strip()
        last = (contact.get('last_name') or '').strip()
        email = contact.get('value')
        if email:
            contacts_list.append({
                'first': first,
                'last': last,
                'email': email,
                'first_lower': first.lower(),
                'last_lower': last.lower()
            })
    company_contacts[company_name] = contacts_list

# Process drafts
drafts_dir = Path('01_INBOX/outreach_drafts')
filled = 0
not_found = 0
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
    
    # Now look up the email
    email = None
    if company_name_from_file in company_contacts:
        contacts = company_contacts[company_name_from_file]
        # Look for matching first and last name (case-insensitive)
        for contact in contacts:
            if contact['first_lower'] == first_from_file.lower() and contact['last_lower'] == last_from_file.lower():
                email = contact['email']
                break
    # If not found, we leave the to: line empty (do not guess)
    
    # If email found, update the draft
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
            filled += 1
            print(f"Filled {draft_file.name} -> {email} (company: {company_name_from_file}, first: {first_from_file}, last: {last_from_file})")
        else:
            # Already correct or format unexpected
            pass
    else:
        # No match found. We leave the draft as is (do not fill with company first email to avoid mistakes)
        not_found += 1
        # Optional: print for debugging
        # print(f"No match for {draft_file.name} (company: {company_name_from_file}, first: {first_from_file}, last: {last_from_file})")

print(f"\nFilled: {filled}, Not filled (no match): {not_found}")
