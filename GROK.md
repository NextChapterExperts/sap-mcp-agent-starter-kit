# Grok Build & xAI Agent Instructions (Community Edition)

License: PolyForm Noncommercial License 1.0.0 (Academic & Student Use Only)
Commercial / Enterprise Consulting Edition: Contact Next Chapter Experts

## Grounding & Tool Execution
- Query MCP tools in `config/mcp_config.json` before generating SAP integration advice.
- Active servers:
  1. `sap-help-portal-local` (`sap_help_get_policy`, `sap_help_search`)
  2. `sap-api-hub-local` (`sap_api_hub_get_api`, `sap_api_hub_search`, `sap_api_hub_list_events`)
  3. `sap-developers-search` (`https://developers.sap.com/mcp/search`)
  4. `sap-docs-community` (`https://mcp-sap-docs.marianzeis.de/mcp`)
  5. `sap-notes` (via npx `sap-note-search-mcp`)
- Deliver answers using executive summary, Mermaid flow, and three technical perspectives.
- Emoji policy: Strictly forbidden in code, XML policies, and system messages.
