#!/usr/bin/env python3
"""
Generate ALL follow-up drafts for all sent emails (ready to send when due)
"""

import json
from datetime import datetime
from pathlib import Path

crm_path = Path("/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/outreach_crm.json")
with open(crm_path) as f:
    crm_data = json.load(f)

entries = crm_data.get("entries", [])
outreach_dir = Path("/Users/mushood/Documents/code/personal/coeus/01_INBOX/outreach_drafts")
followup_dir = Path("/Users/mushood/Documents/code/personal/coeus/01_INBOX/followup_drafts")
followup_dir.mkdir(parents=True, exist_ok=True)

FOLLOWUP_1_TEMPLATE = """---
to: {contact_email}
cc: 
subject: Re: {original_subject} — following up
---

Hi {contact_name},

Following up on my note from {sent_date} about Haga's physics verification for {company}'s physical AI systems.

I know inboxes get busy. Quick recap: Haga provides independent, third-party physics verification that finds sim-to-real gaps before deployment — critical for safety-critical robotics.

We've verified policies for companies in manipulation, locomotion, and video generation. Happy to share a 2-page case study relevant to {company}'s work.

Worth a 10-minute call this week?

Best,
Mushood Hanif
Founder, Haga
haga@mushoodhanif.com
https://mushoodhanif.com
"""

FOLLOWUP_2_TEMPLATE = """---
to: {contact_email}
cc: 
subject: Re: {original_subject} — case study for {company}
---

Hi {contact_name},

Following up again — I put together a brief case study showing how Haga's physics verification would apply to {company}'s {use_case}.

[Attach 1-page PDF or link]

Key result: Our adversarial stress testing found [X%] more failure modes than standard testing on [similar task]. The position-only consistency checks on real robot video quantified sim-to-real gap at [Y%].

If this is relevant, I'd love to discuss a pilot. If not, no worries — I'll close your file.

Best,
Mushood
"""

BREAKUP_TEMPLATE = """---
to: {contact_email}
cc: 
subject: Closing the loop — Haga physics verification
---

Hi {contact_name},

I've followed up a couple times on Haga's physics verification for {company}. Since I haven't heard back, I'll assume this isn't a priority right now and close your file.

If physics verification becomes relevant later (new deployment, safety review, investor request), feel free to reach out — haga@mushoodhanif.com.

Best of luck with {company}'s work.

Mushood
"""

USE_CASES = {
    "Shadow Robot Company Ltd.": "dexterous manipulation and teleoperation",
    "Fieldwork Robotics Limited": "agricultural robotics and deformable object manipulation",
    "Extend Robotics Limited": "human-robot interface and teleoperation",
    "Apollo Research AI Ltd": "AI safety and interpretability research",
    "CGA Simulation Ltd": "defense simulation and synthetic data generation",
    "HPi Verification Services Ltd": "verification services for safety-critical systems",
    "Oxford Robotics Ltd": "mobile autonomy and legged locomotion",
    "Prosper Robotics Ltd": "general-purpose home robotics",
    "Perceptual Robotics Limited": "wind turbine inspection drones",
    "Mistral AI UK Limited": "frontier model physics grounding",
    "Stability AI Ltd": "video generation physics consistency",
    "Tecosim Technical Simulation Ltd.": "CAE simulation fidelity for automotive/aerospace",
    "The Simulator Company Limited": "simulation platform verification",
    "General Physics (UK) Ltd": "scientific consulting and digital twins",
    "Innovative Physics Limited": "radiation/physics simulation and AI",
    "NVIDIA": "Cosmos world models and Omniverse simulation",
    "Google DeepMind": "video generation and world models",
    "Meta AI (FAIR)": "video generation and embodied AI",
    "OpenAI": "Sora video generation and robotics",
    "Anthropic": "Claude video capabilities and physical reasoning",
    "Tesla AI": "Optimus humanoid and FSD physics validation",
    "Waymo": "autonomous driving simulation verification",
    "Cruise": "self-driving vehicle safety validation",
    "Zoox": "autonomous ride-hailing physics verification",
}

def get_original_subject(company):
    draft_files = list(outreach_dir.glob(f"*{company.replace(' ', '_').replace('.', '').replace('&', 'and').replace(',', '')}*.md"))
    if draft_files:
        with open(draft_files[0]) as f:
            content = f.read()
            for line in content.split('\n'):
                if line.startswith('subject:'):
                    return line.replace('subject:', '').strip()
    return f"Physics verification for {company}'s physical AI systems — Mushood Hanif (Haga founder)"

followup_1_count = 0
followup_2_count = 0
breakup_count = 0

for entry in entries:
    company = entry.get("company", "")
    contact_email = entry.get("contact_email", "")
    contact_name = entry.get("contact_name", "")
    sent_status = entry.get("sent_status", "")
    response_status = entry.get("response_status", "")
    
    if sent_status == "sent" and response_status == "pending":
        sent_date = entry.get("sent_date", "2026-08-09")
        original_subject = get_original_subject(company)
        use_case = USE_CASES.get(company, "physical AI/robotics systems")
        
        safe_company = company.replace(" ", "_").replace(".", "").replace("&", "and").replace(",", "").replace("(", "").replace(")", "")
        safe_contact = f"{entry.get('contact_name', 'unknown').replace(' ', '_')}_{entry.get('contact_position', 'contact').replace(' ', '_').replace('/', '_')}"
        
        # Generate Follow-up 1
        draft1 = FOLLOWUP_1_TEMPLATE.format(
            contact_email=contact_email,
            contact_name=contact_name.split()[0] if contact_name else "Team",
            original_subject=original_subject,
            sent_date=sent_date,
            company=company
        )
        filename1 = f"FOLLOWUP1_{sent_date}_{safe_company}_{safe_contact}.md"
        filepath1 = followup_dir / filename1
        with open(filepath1, "w") as f:
            f.write(draft1)
        followup_1_count += 1
        
        # Generate Follow-up 2
        draft2 = FOLLOWUP_2_TEMPLATE.format(
            contact_email=contact_email,
            contact_name=contact_name.split()[0] if contact_name else "Team",
            original_subject=original_subject,
            company=company,
            use_case=use_case
        )
        filename2 = f"FOLLOWUP2_{sent_date}_{safe_company}_{safe_contact}.md"
        filepath2 = followup_dir / filename2
        with open(filepath2, "w") as f:
            f.write(draft2)
        followup_2_count += 1
        
        # Generate Breakup
        draft3 = BREAKUP_TEMPLATE.format(
            contact_email=contact_email,
            contact_name=contact_name.split()[0] if contact_name else "Team",
            company=company
        )
        filename3 = f"BREAKUP_{sent_date}_{safe_company}_{safe_contact}.md"
        filepath3 = followup_dir / filename3
        with open(filepath3, "w") as f:
            f.write(draft3)
        breakup_count += 1

print(f"\n=== SUMMARY ===")
print(f"Follow-up 1 drafts: {followup_1_count}")
print(f"Follow-up 2 drafts: {followup_2_count}")
print(f"Breakup drafts: {breakup_count}")
print(f"Total: {followup_1_count + followup_2_count + breakup_count}")
print(f"Output directory: {followup_dir}")
