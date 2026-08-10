# Phase 2 Investor/Partner Outreach Tracker

## Top 10 Targets - Status Tracking

| # | Target | Tier | Contact | Email | Status | Sent Date | Follow-up 1 | Follow-up 2 | Response | Meeting Booked | Notes |
|---|--------|------|---------|-------|--------|-----------|-------------|-------------|----------|----------------|-------|
| 1 | Lux Capital | 1 VC | Bilal Zuberi | bilal@luxcapital.com | 📝 Draft Ready | | | | | | Josh Wolfe also |
| 2 | Playground Global | 1 VC | General | info@playgroundglobal.com | 📝 Draft Ready | | | | | | Andy Rubin founded |
| 3 | Eclipse Ventures | 1 VC | General | info@eclipse.vc | 📝 Draft Ready | | | | | | Industrial focus |
| 4 | Refactor Capital | 1 VC | General | info@refactor.capital | 📝 Draft Ready | | | | | | Ex-Playground partners |
| 5 | NVIDIA (Cosmos/Omniverse) | 3 Corp | Research | research@nvidia.com | 📝 Draft Ready | | | | | | NVentures for investment |
| 6 | Google DeepMind | 3 Corp | Research | research@deepmind.com | 📝 Draft Ready | | | | | | World models/video gen |
| 7 | Figure AI | 6 Robotics | General | contact@figure.ai | 📝 Draft Ready | | | | | | $675M+ raised |
| 8 | Boston Dynamics | 6 Robotics | General | info@bostondynamics.com | 📝 Draft Ready | | | | | | Hyundai owned |
| 9 | 1X Technologies | 6 Robotics | General | contact@1x.tech | 📝 Draft Ready | | | | | | OpenAI partnership |
| 10 | ANSYS | 4 Sim | Partnerships | partnerships@ansys.com | 📝 Draft Ready | | | | | | ANSYS Ventures |

## Status Legend
- 📝 Draft Ready - Template created, ready to personalize & send
- 📤 Sent - Email sent, awaiting response
- ⏳ Follow-up 1 - First follow-up sent (3-5 business days)
- ⏳ Follow-up 2 - Second follow-up sent (1 week after follow-up 1)
- ✅ Responded - Got response (positive/negative/meeting)
- 🤝 Meeting Booked - Call/demo scheduled
- 🔄 In Discussion - Active conversation
- ❌ Declined - Not interested
- 📭 Bounced - Email failed

## Follow-up Schedule
- **Follow-up 1:** 3-5 business days after initial send
- **Follow-up 2:** 7 business days after follow-up 1
- **Final follow-up:** 14 business days after follow-up 2 (breakup email)

## Response Tracking Template
When response received, update:
- Date responded
- Response type (interested/meeting request/not interested/referral)
- Key contact name/role
- Next steps
- Meeting date if booked

## Materials to Attach/Link
- [ ] Pitch deck (PDF)
- [ ] Technical deep-dive (PDF)
- [ ] Demo video link (Loom/YouTube unlisted)
- [ ] One-pager (PDF)
- [ ] Haga value proposition (already created)
- [ ] Technical integration spec (for simulation companies)

## Week 1 Goals (Aug 11-15)
- [ ] Send all 10 initial emails
- [ ] Track in CRM/airtable/notion
- [ ] Set calendar reminders for follow-ups
- [ ] Prepare for potential quick responses

## Week 2 Goals (Aug 18-22)
- [ ] Send Follow-up 1 to non-responders
- [ ] Book meetings for responders
- [ ] Refine pitch based on feedback
- [ ] Expand target list to next 10

## CRM Fields to Track (add to outreach_crm.json)
- target_type: "investor" | "partner" | "customer"
- tier: 1-6
- outreach_phase: 1 | 2
- email_template_used: filename
- sent_timestamp
- followup_1_sent: boolean + timestamp
- followup_2_sent: boolean + timestamp
- response_received: boolean + timestamp
- response_type: "positive" | "negative" | "meeting_request" | "referral" | "no_response"
- meeting_date: timestamp
- notes: string