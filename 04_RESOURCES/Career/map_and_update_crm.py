#!/usr/bin/env python3
"""
Map actual draft files to CRM entries and mark them as sent
"""

import json
import re
from datetime import datetime
from pathlib import Path

# You sent them yesterday Aug 9, 2026
SENT_DATE = "2026-08-09"

crm_path = Path("/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/outreach_crm.json")
with open(crm_path) as f:
    crm_data = json.load(f)

entries = crm_data.get("entries", [])

# Get list of actual sent draft files
draft_dir = Path("/Users/mushood/Documents/code/personal/coeus/01_INBOX/outreach_drafts")
draft_files = list(draft_dir.glob("*.md"))

print(f"Found {len(draft_files)} actual draft files sent via Yahoo")

# Create mapping from draft filename to expected CRM entry pattern
updated_count = 0
not_found = []

for draft_file in draft_files:
    # Extract company and contact from filename
    # Format: 2026-08-08_Company_First_Last.md or 2026-08-09_Company_First_Last.md
    name = draft_file.stem  # removes .md
    parts = name.split("_")
    
    if len(parts) >= 4:
        # Date parts (could be 2026-08-08 or 2026-08-09)
        date_parts = parts[0:3]
        # The rest is company and name
        rest_parts = parts[3:]
        
        # Try to reconstruct company name (might have spaces, &, etc. replaced)
        # This is tricky - we'll do a fuzzy match
        
        # For now, let's try to find matching CRM entry by looking for similar names
        found = False
        for entry in entries:
            email_draft_path = entry.get("email_draft_path", "")
            if email_draft_path and draft_file.name in email_draft_path:
                # Exact match
                entry["sent_status"] = "sent"
                entry["sent_date"] = SENT_DATE
                entry["pipeline_stage"] = "Sent"
                entry["followup_1_sent"] = False
                entry["followup_2_sent"] = False
                entry["breakup_sent"] = False
                entry["last_updated"] = datetime.now().isoformat()
                updated_count += 1
                found = True
                break
        
        if not found:
            # Try fuzzy matching
            draft_company_part = "_".join(rest_parts[:-2]) if len(rest_parts) >= 2 else "_".join(rest_parts)
            draft_company = draft_company_part.replace("_", " ").replace("&", "and").replace("-", " ")
            
            for entry in entries:
                company_name = entry.get("company", "").lower()
                if draft_company.lower() in company_name or company_name in draft_company.lower():
                    # Potential match - check if contact also matches
                    draft_first = rest_parts[-2] if len(rest_parts) >= 2 else ""
                    draft_last = rest_parts[-1] if len(rest_parts) >= 1 else ""
                    
                    entry_first = entry.get("contact_name", "").split()[0] if entry.get("contact_name") else ""
                    entry_last = entry.get("contact_name", "").split()[-1] if entry.get("contact_name") and len(entry.get("contact_name", "").split()) > 1 else ""
                    
                    if (draft_first.lower() in entry_first.lower() or entry_first.lower() in draft_first.lower()) and \
                       (draft_last.lower() in entry_last.lower() or entry_last.lower() in draft_last.lower()):
                        entry["sent_status"] = "sent"
                        entry["sent_date"] = SENT_DATE
                        entry["pipeline_stage"] = "Sent"
                        entry["followup_1_sent"] = False
                        entry["followup_2_sent"] = False
                        entry["breakup_sent"] = False
                        entry["last_updated"] = datetime.now().isoformat()
                        updated_count += 1
                        found = True
                        break
            
            if not found:
                not_found.append(draft_file.name)

print(f"Updated {updated_count} CRM entries to 'sent' status with date {SENT_DATE}")
if not_found:
    print(f"Could not find CRM matches for {len(not_found)} draft files:")
    for nf in not_found[:10]:  # Show first 10
        print(f"  - {nf}")
    if len(not_found) > 10:
        print(f"  ... and {len(not_found) - 10} more")

# Save updated CRM
with open(crm_path, "w") as f:
    json.dump(crm_data, f, indent=2)

print("CRM updated successfully")

# Also, let's count how many are now sent
sent_count = sum(1 for e in entries if e.get("sent_status") == "sent")
print(f"Total entries now marked as 'sent': {sent_count}")
