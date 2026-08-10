# Phase 1 Follow-up System for Non-Responders

## Current Phase 1 Status (from outreach_crm.json)
- Total entries: 34 (from outreach_crm.json)
- All currently at "drafted" / "pending" status
- User manually sent 64 emails (some companies have multiple contacts)

## Follow-up Strategy

### Timing
- **Follow-up 1:** 3-5 business days after send (Aug 12-14)
- **Follow-up 2:** 7 business days after follow-up 1 (Aug 19-21)
- **Breakup email:** 14 business days after follow-up 2 (Sep 2-4)

### Follow-up Templates

#### Follow-up 1 (Gentle nudge)
```
Subject: Re: [Original subject] — following up

Hi [Name],

Following up on my note from [date] about Haga's physics verification for [Company]'s physical AI systems.

I know inboxes get busy. Quick recap: Haga provides independent, third-party physics verification that finds sim-to-real gaps before deployment — critical for safety-critical robotics.

We've verified policies for companies in manipulation, locomotion, and video generation. Happy to share a 2-page case study relevant to [Company]'s work.

Worth a 10-minute call this week?

Best,
Mushood Hanif
Founder, Haga
haga@mushoodhanif.com
```

#### Follow-up 2 (Value-add)
```
Subject: Re: [Original subject] — case study for [Company]

Hi [Name],

Following up again — I put together a brief case study showing how Haga's physics verification would apply to [Company]'s [specific use case: manipulation/locomotion/video generation].

[Attach 1-page PDF or link]

Key result: Our adversarial stress testing found [X%] more failure modes than standard testing on [similar task]. The position-only consistency checks on real robot video quantified sim-to-real gap at [Y%].

If this is relevant, I'd love to discuss a pilot. If not, no worries — I'll close your file.

Best,
Mushood
```

#### Breakup Email (Final)
```
Subject: Closing the loop — Haga physics verification

Hi [Name],

I've followed up a couple times on Haga's physics verification for [Company]. Since I haven't heard back, I'll assume this isn't a priority right now and close your file.

If physics verification becomes relevant later (new deployment, safety review, investor request), feel free to reach out — haga@mushoodhanif.com.

Best of luck with [Company]'s work.

Mushood
```

## Companies to Track (from outreach_crm.json + drafts)

### High Priority (Tier 1 Sponsors - multiple contacts)
1. Shadow Robot Company Ltd. (4 contacts)
2. Fieldwork Robotics Limited (4 contacts)
3. Extend Robotics Limited (4 contacts)
4. Apollo Research AI Ltd (3 contacts)
5. Mistral AI UK Limited (3 contacts)
6. Stability AI Ltd (3 contacts)
7. Tecosim Technical Simulation Ltd. (3 contacts)
8. NVIDIA (3 contacts)
9. Google DeepMind (3 contacts)
10. Meta AI (FAIR) (3 contacts)
11. OpenAI (3 contacts)
12. Anthropic (3 contacts)
13. Tesla AI (3 contacts)

### Medium Priority (0-1 contacts found)
- JBS Applied A.I & Robotics Research Ltd (0 contacts)
- CGA Simulation Ltd (0 contacts)
- HPi Verification Services Ltd (0 contacts)
- Oxford Robotics Ltd (3 contacts)
- Prosper Robotics Ltd (0 contacts)
- Perceptual Robotics Limited (2 contacts)
- Human Digital Twin Limited (0 contacts)
- The Simulator Company Limited (1 contact)
- General Physics (UK) Ltd (0 contacts)
- Innovative Physics Limited (0 contacts)
- Waymo (0 contacts)
- Cruise (0 contacts)
- Zoox (0 contacts)

## Automation Script Needed
Create a Python script that:
1. Reads outreach_crm.json
2. For each entry with sent_status="sent" and response_status="pending"
3. Checks days since sent
4. Generates follow-up email drafts at appropriate intervals
5. Saves to followup_drafts/ directory
6. Updates outreach_crm.json with followup_1_sent, followup_2_sent flags

## Manual Process for Now
Since you sent emails manually:
1. Update outreach_crm.json with sent_status="sent" and sent_date for each
2. Set calendar reminders for follow-ups
3. Use templates above to send follow-ups manually
4. Track responses in outreach_crm.json

## Next Steps
1. Update outreach_crm.json with actual sent dates
2. Create follow-up drafts for all 34 entries
3. Schedule calendar reminders
4. Begin Phase 2 investor outreach in parallel