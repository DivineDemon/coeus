#!/usr/bin/env python3
"""
Update outreach_crm.json to mark emails as sent with actual date
"""

import json
from datetime import datetime
from pathlib import Path

# You said you sent them yesterday Aug 9, 2026
SENT_DATE = "2026-08-09"  # Change this if you sent on a different date

crm_path = Path("/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/outreach_crm.json")
with open(crm_path) as f:
    crm_data = json.load(f)

entries = crm_data.get("entries", [])

# Update all entries to sent status
updated_count = 0
for entry in entries:
    if entry.get("sent_status") == "drafted":
        entry["sent_status"] = "sent"
        entry["sent_date"] = SENT_DATE
        entry["pipeline_stage"] = "Sent"
        entry["followup_1_sent"] = False
        entry["followup_2_sent"] = False
        entry["breakup_sent"] = False
        entry["last_updated"] = datetime.now().isoformat()
        updated_count += 1

print(f"Updated {updated_count} entries to 'sent' status with date {SENT_DATE}")

# Save updated CRM
with open(crm_path, "w") as f:
    json.dump(crm_data, f, indent=2)

print("CRM updated successfully")
