---
name: burglass-crm
description: |
  Burglass CRM integration for B2B lead generation & outreach.
  Use when: (1) searching/listing companies or contacts, (2) viewing company details or timeline,
  (3) creating or updating contacts/notes, (4) checking pipeline deals, (5) viewing campaign stats
  or dashboard KPIs, (6) discovering new leads via scraping.
  Do NOT use for general questions unrelated to CRM data.
metadata:
  openclaw:
    emoji: "\U0001F4BC"
    homepage: https://burglass.com
    primaryEnv: BURGLASS_API_KEY
    requires:
      env:
        - BURGLASS_API_KEY
        - BURGLASS_API_URL
      bins:
        - curl
        - jq
---

# Burglass CRM

Burglass V12 is a B2B lead generation & email outreach CRM.
All endpoints require the `Authorization: Bearer $BURGLASS_API_KEY` header.
Base URL is `$BURGLASS_API_URL` (e.g. `https://crm.burglass.com/api/v1`).

## Auth Header

Every request must include:

```
-H "Authorization: Bearer $BURGLASS_API_KEY" -H "Content-Type: application/json"
```

Use the shorthand `$AUTH` defined below in examples:

```bash
AUTH="Authorization: Bearer $BURGLASS_API_KEY"
BASE="$BURGLASS_API_URL"
```

---

## Companies

### List / Search Companies

```bash
curl -s "$BASE/companies?search=glass&country=Turkey&page=1&per_page=20" \
  -H "$AUTH" | jq '.data[] | {id, name, country, sector, lead_status, email}'
```

Query params: `search`, `country`, `sector`, `lead_status` (new/contacted/qualified/proposal/won/lost), `source`, `data_status`, `page` (1-based), `per_page` (max 500).

### Get Company Detail

```bash
curl -s "$BASE/companies/42" -H "$AUTH" | jq '.'
```

Returns full company record: name, email, phone, website, linkedin, address, city, country, sector, lead_status, lead_score, tags, data_quality, notes, created_at.

### Company Timeline

```bash
curl -s "$BASE/companies/42/timeline?limit=20" -H "$AUTH" | jq '.'
```

Returns unified activity feed: notes, tasks, emails, communications, deals.

### Create Company

```bash
curl -X POST "$BASE/companies" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"place_id":"ChIJ...","name":"Acme Corp","country":"Germany","sector":"Manufacturing"}'
```

Required: `place_id` (Google Places ID) or `name`.

### Update Company

```bash
curl -X PUT "$BASE/companies/42" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"lead_status":"qualified","notes":"Met at trade fair."}'
```

Updatable fields: name, email, phone, website, linkedin, address, city, country, sector, notes, lead_status, lead_score, tags, company_size, employee_count.

---

## Contacts

### List Contacts for Company

```bash
curl -s "$BASE/contacts/company/42" -H "$AUTH" | jq '.[] | {id, name, email, role, is_primary}'
```

### Create Contact

```bash
curl -X POST "$BASE/contacts" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"company_id":42,"name":"John Doe","email":"john@acme.com","role":"CEO","is_primary":1}'
```

### Update Contact

```bash
curl -X PUT "$BASE/contacts/99" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"role":"CTO","phone":"+49123456789"}'
```

---

## Notes

### List Notes for Company

```bash
curl -s "$BASE/notes/company/42" -H "$AUTH" | jq '.[] | {id, title, note_type, created_at}'
```

### Create Note

```bash
curl -X POST "$BASE/notes" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"company_id":42,"note_type":"call","title":"Initial call","content":"Discussed pricing."}'
```

Note types: `general`, `call`, `meeting`, `email`, `task`, `important`.

---

## Pipeline / Deals

### List Deals

```bash
curl -s "$BASE/pipeline/deals?stage=proposal" -H "$AUTH" | jq '.[] | {id, title, value, stage}'
```

### Pipeline Summary (Kanban counts)

```bash
curl -s "$BASE/pipeline/summary" -H "$AUTH" | jq '.'
```

Returns count and total value per stage.

### Create Deal

```bash
curl -X POST "$BASE/pipeline/deals" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"company_id":42,"title":"Glass supply contract","value":25000,"currency":"EUR","stage":"proposal","probability":60}'
```

### Update Deal Stage

```bash
curl -X PUT "$BASE/pipeline/deals/7" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"stage":"won","won_reason":"Best price"}'
```

---

## Dashboard & Analytics

### Dashboard Stats

```bash
curl -s "$BASE/dashboard/stats" -H "$AUTH" | jq '.'
```

Returns: total_companies, total_emails, total_phones, total_linkedin, active_campaigns, active_deals.

### Dashboard KPIs

```bash
curl -s "$BASE/dashboard/kpis" -H "$AUTH" | jq '.'
```

Returns: email_coverage_rate, pipeline_total_value, won_value, monthly_cost.

### Country Breakdown

```bash
curl -s "$BASE/dashboard/countries-breakdown" -H "$AUTH" | jq '.'
```

### Campaign Metrics

```bash
curl -s "$BASE/analytics/campaign/5" -H "$AUTH" | jq '.'
```

Returns: sent, opened, clicked, replied, bounced + rates.

### Analytics Overview

```bash
curl -s "$BASE/analytics/overview" -H "$AUTH" | jq '.'
```

Global email performance across all campaigns.

---

## Campaigns

### List Campaigns

```bash
curl -s "$BASE/campaigns" -H "$AUTH" | jq '.[] | {id, name, status, campaign_type}'
```

### Get Campaign Detail

```bash
curl -s "$BASE/campaigns/5" -H "$AUTH" | jq '.'
```

### Start / Pause / Resume Campaign

```bash
curl -X POST "$BASE/campaigns/5/start" -H "$AUTH"
curl -X POST "$BASE/campaigns/5/pause" -H "$AUTH"
curl -X POST "$BASE/campaigns/5/resume" -H "$AUTH"
```

---

## Lead Scoring

### Top Scored Leads

```bash
curl -s "$BASE/scoring/top?limit=10" -H "$AUTH" | jq '.[] | {company_id, name, score}'
```

### Score Breakdown for Company

```bash
curl -s "$BASE/scoring/42" -H "$AUTH" | jq '.'
```

### Recalculate Score

```bash
curl -X POST "$BASE/scoring/calculate?company_id=42" -H "$AUTH"
```

---

## Discover (Lead Generation)

### Scrape Google Places

```bash
curl -X POST "$BASE/discover/scrape" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"api_key":"AIza...","keyword":"glass manufacturer","city":"Istanbul","country":"Turkey","sector":"Glass"}'
```

### Web Crawl (no API key needed)

```bash
curl -X POST "$BASE/discover/crawl" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"keyword":"glass manufacturer","city":"Berlin","country":"Germany","sector":"Glass","max_results":50}'
```

### Check Queue Status

```bash
curl -s "$BASE/discover/queue?limit=10" -H "$AUTH" | jq '.[] | {id, kind, status, created_at}'
```

---

## Safety & Best Practices

- Always confirm with the user before creating, updating, or deleting records.
- For bulk operations (delete, rescrape), list affected items first and ask for confirmation.
- Use `--json` output with `jq` for readable formatting.
- Pagination: always check `total` and `pages` in response to determine if more pages exist.
- Rate limits apply; if you receive HTTP 429, wait and retry.
- When searching, prefer specific filters (country + sector) over broad `search` queries.
- All timestamps are UTC in ISO 8601 format.
