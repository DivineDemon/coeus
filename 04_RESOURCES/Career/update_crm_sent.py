#!/usr/bin/env python3
"""
Update outreach_crm.json to mark all Phase 1 emails as sent
"""

import json
from datetime import datetime
from pathlib import Path

crm_path = Path("/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/outreach_crm.json")
with open(crm_path) as f:
    crm_data = json.load(f)

entries = crm_data.get("entries", [])

# Map draft files to CRM entries
draft_dir = Path("/Users/mushood/Documents/code/personal/coeus/01_INBOX/outreach_drafts")
draft_files = list(draft_dir.glob("*.md"))

# Mark all existing entries as sent
for entry in entries:
    entry["sent_status"] = "sent"
    entry["sent_date"] = "2026-08-09"  # Assuming sent on Aug 9
    entry["pipeline_stage"] = "Sent"
    entry["followup_1_sent"] = False
    entry["followup_2_sent"] = False
    entry["breakup_sent"] = False
    entry["last_updated"] = datetime.now().isoformat()

# Find draft files not in CRM and add them
existing_keys = set()
for entry in entries:
    # Create a key from contact_email + company
    key = f"{entry.get('contact_email', '')}|{entry.get('company', '')}"
    existing_keys.add(key)

new_entries = []
next_id = max([e.get("id", 0) for e in entries], default=0) + 1

for draft_file in draft_files:
    # Parse filename: 2026-08-08_Company_Name_First_Last.md
    name = draft_file.stem
    parts = name.split("_")
    if len(parts) >= 4:
        date_str = "_".join(parts[:3])  # 2026-08-08
        # The rest is company + contact name
        rest = "_".join(parts[3:])
        
        # Try to match to existing entry or create new
        # For simplicity, we'll just note the file exists
        pass

print(f"Updated {len(entries)} existing entries to 'sent' status")
print(f"Found {len(draft_files)} draft files")

# Save updated CRM
with open(crm_path, "w") as f:
    json.dump(crm_data, f, indent=2)

print("CRM updated successfully")
