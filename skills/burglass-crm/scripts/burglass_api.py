#!/usr/bin/env python3
"""Burglass CRM API helper for OpenClaw.

Usage:
    python3 burglass_api.py companies --search "glass" --country "Turkey" --limit 20
    python3 burglass_api.py company 42
    python3 burglass_api.py contacts 42
    python3 burglass_api.py create-contact 42 --name "John" --email "j@co.com" --role "CEO"
    python3 burglass_api.py create-note 42 --type call --title "Call" --content "Discussed pricing"
    python3 burglass_api.py deals --stage proposal
    python3 burglass_api.py pipeline-summary
    python3 burglass_api.py dashboard
    python3 burglass_api.py kpis
    python3 burglass_api.py top-leads --limit 10
    python3 burglass_api.py campaign-metrics 5
    python3 burglass_api.py search-all "keyword"

Env vars required:
    BURGLASS_API_KEY  — API bearer token
    BURGLASS_API_URL  — Base URL (e.g. https://crm.burglass.com/api/v1)
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

API_KEY = os.environ.get("BURGLASS_API_KEY", "")
API_URL = os.environ.get("BURGLASS_API_URL", "http://localhost:8912/api/v1")


def _request(method: str, path: str, data: dict | None = None, params: dict | None = None) -> dict:
    """Make an authenticated HTTP request to Burglass API."""
    url = f"{API_URL}{path}"
    if params:
        qs = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        url = f"{url}?{qs}"

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        print(json.dumps({"error": True, "status": e.code, "detail": err_body}, indent=2))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": True, "detail": str(e.reason)}, indent=2))
        sys.exit(1)


def cmd_companies(args):
    """List/search companies."""
    params = {
        "search": args.search,
        "country": args.country,
        "sector": args.sector,
        "lead_status": args.status,
        "page": args.page,
        "per_page": args.limit,
    }
    result = _request("GET", "/companies", params=params)
    companies = result.get("data", result) if isinstance(result, dict) else result
    if isinstance(result, dict) and "total" in result:
        print(f"# Total: {result['total']}  Page: {result.get('page', 1)}/{result.get('pages', 1)}")
    for c in (companies if isinstance(companies, list) else []):
        print(json.dumps({
            "id": c.get("id"),
            "name": c.get("name"),
            "country": c.get("country"),
            "sector": c.get("sector"),
            "email": c.get("email"),
            "lead_status": c.get("lead_status"),
            "lead_score": c.get("lead_score"),
        }))


def cmd_company(args):
    """Get single company."""
    result = _request("GET", f"/companies/{args.id}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_contacts(args):
    """List contacts for a company."""
    result = _request("GET", f"/contacts/company/{args.company_id}")
    for c in (result if isinstance(result, list) else []):
        print(json.dumps({
            "id": c.get("id"),
            "name": c.get("name"),
            "email": c.get("email"),
            "phone": c.get("phone"),
            "role": c.get("role"),
            "is_primary": c.get("is_primary"),
        }))


def cmd_create_contact(args):
    """Create a new contact."""
    data = {"company_id": args.company_id, "name": args.name}
    if args.email:
        data["email"] = args.email
    if args.phone:
        data["phone"] = args.phone
    if args.role:
        data["role"] = args.role
    if args.primary:
        data["is_primary"] = 1
    result = _request("POST", "/contacts", data=data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_create_note(args):
    """Create a note on a company."""
    data = {
        "company_id": args.company_id,
        "note_type": args.type,
        "title": args.title,
        "content": args.content,
    }
    result = _request("POST", "/notes", data=data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_deals(args):
    """List pipeline deals."""
    params = {"stage": args.stage} if args.stage else {}
    result = _request("GET", "/pipeline/deals", params=params)
    for d in (result if isinstance(result, list) else []):
        print(json.dumps({
            "id": d.get("id"),
            "title": d.get("title"),
            "value": d.get("value"),
            "currency": d.get("currency"),
            "stage": d.get("stage"),
            "probability": d.get("probability"),
        }))


def cmd_pipeline_summary(args):
    """Pipeline summary by stage."""
    result = _request("GET", "/pipeline/summary")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_dashboard(args):
    """Dashboard stats."""
    result = _request("GET", "/dashboard/stats")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_kpis(args):
    """Dashboard KPIs."""
    result = _request("GET", "/dashboard/kpis")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_top_leads(args):
    """Top scored leads."""
    params = {"limit": args.limit}
    result = _request("GET", "/scoring/top", params=params)
    for lead in (result if isinstance(result, list) else []):
        print(json.dumps({
            "company_id": lead.get("company_id", lead.get("id")),
            "name": lead.get("name"),
            "score": lead.get("lead_score", lead.get("score")),
            "country": lead.get("country"),
            "sector": lead.get("sector"),
        }))


def cmd_campaign_metrics(args):
    """Campaign metrics."""
    result = _request("GET", f"/analytics/campaign/{args.campaign_id}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_search_all(args):
    """Cross-resource search: companies + contacts."""
    print("=== Companies ===")
    companies = _request("GET", "/companies", params={"search": args.query, "per_page": 10})
    for c in companies.get("data", []) if isinstance(companies, dict) else companies:
        print(f"  [{c.get('id')}] {c.get('name')} | {c.get('country')} | {c.get('sector')} | {c.get('lead_status')}")

    print("\n=== Top Leads ===")
    leads = _request("GET", "/scoring/top", params={"limit": 5})
    for l in (leads if isinstance(leads, list) else []):
        print(f"  [{l.get('company_id', l.get('id'))}] {l.get('name')} | score: {l.get('lead_score', l.get('score'))}")


def main():
    parser = argparse.ArgumentParser(description="Burglass CRM CLI helper")
    sub = parser.add_subparsers(dest="command")

    # companies
    p = sub.add_parser("companies", help="List/search companies")
    p.add_argument("--search", "-s", default=None)
    p.add_argument("--country", default=None)
    p.add_argument("--sector", default=None)
    p.add_argument("--status", default=None)
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--limit", type=int, default=20)

    # company detail
    p = sub.add_parser("company", help="Get company detail")
    p.add_argument("id", type=int)

    # contacts
    p = sub.add_parser("contacts", help="List contacts for company")
    p.add_argument("company_id", type=int)

    # create-contact
    p = sub.add_parser("create-contact", help="Create contact")
    p.add_argument("company_id", type=int)
    p.add_argument("--name", required=True)
    p.add_argument("--email", default=None)
    p.add_argument("--phone", default=None)
    p.add_argument("--role", default=None)
    p.add_argument("--primary", action="store_true")

    # create-note
    p = sub.add_parser("create-note", help="Create note on company")
    p.add_argument("company_id", type=int)
    p.add_argument("--type", default="general", choices=["general", "call", "meeting", "email", "task", "important"])
    p.add_argument("--title", required=True)
    p.add_argument("--content", required=True)

    # deals
    p = sub.add_parser("deals", help="List deals")
    p.add_argument("--stage", default=None)

    # pipeline-summary
    sub.add_parser("pipeline-summary", help="Pipeline summary")

    # dashboard
    sub.add_parser("dashboard", help="Dashboard stats")

    # kpis
    sub.add_parser("kpis", help="KPIs")

    # top-leads
    p = sub.add_parser("top-leads", help="Top scored leads")
    p.add_argument("--limit", type=int, default=10)

    # campaign-metrics
    p = sub.add_parser("campaign-metrics", help="Campaign metrics")
    p.add_argument("campaign_id", type=int)

    # search-all
    p = sub.add_parser("search-all", help="Search across resources")
    p.add_argument("query")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if not API_KEY:
        print("Error: BURGLASS_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    commands = {
        "companies": cmd_companies,
        "company": cmd_company,
        "contacts": cmd_contacts,
        "create-contact": cmd_create_contact,
        "create-note": cmd_create_note,
        "deals": cmd_deals,
        "pipeline-summary": cmd_pipeline_summary,
        "dashboard": cmd_dashboard,
        "kpis": cmd_kpis,
        "top-leads": cmd_top_leads,
        "campaign-metrics": cmd_campaign_metrics,
        "search-all": cmd_search_all,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
