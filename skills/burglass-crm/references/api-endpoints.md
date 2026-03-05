# Burglass CRM API Reference

## Authentication

All requests require:
```
Authorization: Bearer {BURGLASS_API_KEY}
Content-Type: application/json
```

## Base URL

Set via `BURGLASS_API_URL` environment variable.
Default: `http://localhost:8912/api/v1`

---

## Companies

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies` | List/search companies with pagination |
| GET | `/companies/{id}` | Get company detail |
| GET | `/companies/{id}/timeline` | Activity timeline (notes, tasks, emails, deals) |
| GET | `/companies/recent?limit=20` | Recently added companies |
| GET | `/companies/unique-sectors` | All unique sector values |
| POST | `/companies` | Create company |
| PUT | `/companies/{id}` | Update company fields |
| DELETE | `/companies/{id}` | Delete company |

### List Query Parameters

| Param | Type | Description |
|-------|------|-------------|
| search | string | Full-text search on name, email, website |
| country | string | Exact country name filter |
| sector | string | Exact sector name filter |
| lead_status | string | new, contacted, qualified, proposal, won, lost |
| source | string | Data source filter |
| data_status | string | Data quality status |
| page | int | Page number (1-based, default 1) |
| per_page | int | Results per page (1-500, default 50) |

### Company Fields

```json
{
  "id": 42,
  "place_id": "ChIJ...",
  "name": "Acme Glass Corp",
  "email": "info@acme.com",
  "phone": "+49-123-456789",
  "website": "https://acme.com",
  "linkedin": "https://linkedin.com/company/acme",
  "address": "Hauptstr. 1, Berlin",
  "city": "Berlin",
  "country": "Germany",
  "sector": "Glass Manufacturing",
  "source": "google_places",
  "lead_status": "qualified",
  "lead_score": 75,
  "data_quality": 0.85,
  "tags": "premium,eu",
  "company_size": "medium",
  "employee_count": 150,
  "notes": "Key account for EU region",
  "mail_sent": 1,
  "phone_called": 0,
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-03-01T14:00:00Z"
}
```

---

## Contacts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/contacts/company/{company_id}` | List contacts for company |
| POST | `/contacts` | Create contact |
| PUT | `/contacts/{id}` | Update contact |
| DELETE | `/contacts/{id}` | Delete contact |

### Contact Fields

```json
{
  "id": 99,
  "company_id": 42,
  "name": "John Doe",
  "email": "john@acme.com",
  "phone": "+49-123-000000",
  "linkedin": "https://linkedin.com/in/johndoe",
  "role": "CEO",
  "is_primary": 1,
  "created_at": "2026-02-10T09:00:00Z"
}
```

---

## Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes/company/{company_id}` | List notes for company |
| POST | `/notes` | Create note |
| PUT | `/notes/{id}` | Update note |
| DELETE | `/notes/{id}` | Delete note |

### Note Types
`general`, `call`, `meeting`, `email`, `task`, `important`

---

## Pipeline / Deals

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pipeline/deals` | List deals (optional `?stage=` filter) |
| GET | `/pipeline/stages` | Stage definitions |
| GET | `/pipeline/kanban` | Deals grouped by stage |
| GET | `/pipeline/summary` | Count & total value per stage |
| POST | `/pipeline/deals` | Create deal |
| PUT | `/pipeline/deals/{id}` | Update deal |
| DELETE | `/pipeline/deals/{id}` | Delete deal |

### Deal Fields

```json
{
  "id": 7,
  "company_id": 42,
  "contact_id": 99,
  "title": "Glass supply contract",
  "value": 25000.00,
  "currency": "EUR",
  "stage": "proposal",
  "probability": 60,
  "expected_close": "2026-06-01",
  "notes": "Waiting for board approval",
  "won_reason": null,
  "lost_reason": null,
  "created_at": "2026-02-20T11:00:00Z"
}
```

---

## Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/stats` | Totals: companies, emails, phones, campaigns, deals |
| GET | `/dashboard/kpis` | Email rate, pipeline value, won value |
| GET | `/dashboard/activity?limit=20` | Recent activity feed |
| GET | `/dashboard/countries-breakdown` | Company count per country |
| GET | `/dashboard/sectors-breakdown` | Company count per sector |

---

## Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/overview` | Global email stats |
| GET | `/analytics/campaign/{id}` | Campaign-specific metrics |
| GET | `/analytics/events-timeline?days=30` | Events by date (charting) |

---

## Lead Scoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/scoring/top?limit=10` | Top scored leads |
| GET | `/scoring/{company_id}` | Score breakdown |
| POST | `/scoring/calculate?company_id=42` | Recalculate score |
| POST | `/scoring/bulk` | Bulk recalculation (background) |

---

## Campaigns

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/campaigns` | List campaigns |
| GET | `/campaigns/{id}` | Campaign with sequences |
| GET | `/campaigns/{id}/metrics` | Send/open/click/reply stats |
| POST | `/campaigns` | Create campaign |
| PUT | `/campaigns/{id}` | Update campaign |
| POST | `/campaigns/{id}/start` | Start sending |
| POST | `/campaigns/{id}/pause` | Pause |
| POST | `/campaigns/{id}/resume` | Resume |

---

## Discover (Lead Generation)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/discover/scrape` | Google Places scrape (needs api_key) |
| POST | `/discover/crawl` | Web crawl (no API key needed) |
| POST | `/discover/scrape-url` | Deep-scrape single URL |
| GET | `/discover/queue?limit=10` | Scrape job queue |
| GET | `/discover/countries` | Available countries |
| GET | `/discover/sectors` | Available sectors |

---

## Error Responses

```json
{
  "error": true,
  "error_code": "NOT_FOUND",
  "message": "Company not found",
  "request_id": "abc-123-def"
}
```

Common codes: `NOT_FOUND`, `VALIDATION_ERROR`, `CONFLICT`, `AUTH_ERROR`, `RATE_LIMIT`
