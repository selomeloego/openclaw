# Burglass CRM — OpenClaw Setup Guide

## Prerequisites

1. **Burglass CRM instance** running (local or remote)
2. **Admin access** to create API tokens

## Step 1: Generate an API Token

1. Open Burglass CRM → Settings page
2. Scroll to **API Tokens** card (right column)
3. Enter a name like `openclaw` and click **Create**
4. **Copy the token immediately** — it's shown only once!

Or via CLI:
```bash
curl -X POST "http://localhost:8912/api/v1/api-tokens" \
  -H "Cookie: access_token=YOUR_SESSION_COOKIE" \
  -H "Content-Type: application/json" \
  -d '{"name":"openclaw","scopes":"*"}'
```

## Step 2: Configure OpenClaw Environment

Add these to your OpenClaw environment (e.g. `~/.openclaw/config` or shell profile):

```bash
export BURGLASS_API_KEY="your-64-char-hex-token-here"
export BURGLASS_API_URL="http://localhost:8912/api/v1"
```

For remote instances:
```bash
export BURGLASS_API_URL="https://crm.burglass.com/api/v1"
```

## Step 3: Verify Connection

```bash
curl -s "$BURGLASS_API_URL/api-tokens/validate" \
  -X POST \
  -H "Authorization: Bearer $BURGLASS_API_KEY" | jq '.'
```

Expected response:
```json
{
  "valid": true,
  "name": "openclaw",
  "username": "admin",
  "scopes": "*"
}
```

## Step 4: Test the Skill

Ask OpenClaw:
- "Show me the dashboard stats from Burglass CRM"
- "Search for glass companies in Turkey"
- "What are the top 10 leads by score?"

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 401 Unauthorized | Token may be revoked or invalid. Create a new one in Settings. |
| Connection refused | Check BURGLASS_API_URL. Is the backend running? |
| 429 Too Many Requests | Rate limit hit. Wait a moment and retry. |
| Empty results | Check filters — country/sector names must be exact matches. |

## Security Notes

- API tokens have full admin access (scopes: *)
- Tokens don't expire by default — revoke when no longer needed
- Use HTTPS in production (`BURGLASS_API_URL=https://...`)
- Token is stored in `api_tokens` table, hashed comparison not needed (long random hex)
