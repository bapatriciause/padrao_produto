# API Access & Existing Data Checklist

Document your product's existing APIs, data sources, and integration points that could be used during the workshop.

---

## VBU Name: [Your VBU]

## API Inventory

### API #1: [API Name]

- **Base URL:** [e.g. https://api.yourproduct.com/v2]
- **Documentation:** [Link to API docs]
- **Authentication:** [e.g. API key, OAuth2, JWT]
- **Rate Limits:** [e.g. 100 requests/minute]
- **Sandbox / Test Environment Available?** [Yes / No]
- **Key Endpoints:**

  | Endpoint | Method | Description |
  |----------|--------|-------------|
  | `/resource` | GET | [What it returns] |
  | `/resource` | POST | [What it creates] |

### API #2: [API Name]

*Repeat as needed.*

---

## Access Credentials for Workshop

> **Do NOT put secrets in this file.** Bring credentials securely on the day (1Password, Azure Key Vault, or share in person).

- [ ] I have sandbox/test API credentials ready to share securely during the workshop
- [ ] I have confirmed the sandbox environment will be available during workshop dates
- [ ] Rate limits are sufficient for workshop prototyping (or can be temporarily increased)

## Existing Data Exports

List any data exports or files you're bringing:

| File | Format | Description | Size | Location |
|------|--------|-------------|------|----------|
| [Filename] | [CSV/JSON/Excel] | [What it contains] | [e.g. 5MB] | `prework/[filename]` |

## Integration Points

What systems does your product currently integrate with?

| System | Integration Type | Description |
|--------|-----------------|-------------|
| [e.g. Salesforce] | [REST API / Webhook / File export] | [What data flows where] |

## Known Limitations

- [e.g. "API does not support bulk export, max 100 records per request"]
- [e.g. "No webhook support, would need polling"]
- [e.g. "Authentication tokens expire every 30 minutes"]
