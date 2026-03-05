# Burglass CRM Field Mapping

## Lead Status Values

| Status | Description | Turkish |
|--------|-------------|---------|
| new | Newly added, no contact made | Yeni |
| contacted | Initial outreach done | İletişime Geçildi |
| qualified | Confirmed interest/fit | Nitelikli |
| proposal | Proposal/quote sent | Teklif Gönderildi |
| won | Deal closed successfully | Kazanıldı |
| lost | Deal lost/rejected | Kaybedildi |

## Note Types

| Type | Use Case |
|------|----------|
| general | Default, general-purpose notes |
| call | Phone call summaries |
| meeting | Meeting notes and outcomes |
| email | Email correspondence notes |
| task | To-do items and action items |
| important | Flagged/critical information |

## Deal Stages

Pipeline stages match lead_status but are deal-specific:
- `lead` → Initial stage
- `contacted` → Outreach made
- `qualified` → Interest confirmed
- `proposal` → Proposal sent
- `negotiation` → Terms being discussed
- `won` → Closed-won
- `lost` → Closed-lost

## Data Quality Scores

`data_quality` ranges from 0.0 to 1.0:
- **0.8-1.0:** Complete — all key fields filled
- **0.5-0.8:** Partial — some fields missing
- **0.0-0.5:** Sparse — most fields empty

Key fields that affect quality:
- email (highest weight)
- phone
- website
- linkedin
- address
- contacts (at least one)

## Country Names

Countries are stored as full English names (e.g., "Turkey", "Germany", "United Kingdom").
Use exact country names when filtering.

## Sector Names

Sectors are free-text but common values include:
- Glass Manufacturing
- Glass Processing
- Glass Trading
- Glass Recycling
- Automotive Glass
- Architectural Glass
- Glass Packaging
- Solar Glass

Use `/companies/unique-sectors` to get the current list.
