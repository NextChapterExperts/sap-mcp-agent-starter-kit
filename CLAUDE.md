# Claude Code Rules (Community Edition)

License: PolyForm Noncommercial License 1.0.0 (Academic & Student Use Only)
Commercial / Enterprise Consulting Edition: Contact Next Chapter Experts

## Grounding & Tool Disciplines
- Always invoke tools from `config/mcp_config.json` before proposing SAP BTP architectures or APIM policies.
- Primary tools: `sap_help_get_policy`, `sap_help_search`, `sap_api_hub_get_api`, `sap_api_hub_search`, `sap_api_hub_list_events`.
- Grounding sources: `sap-developers-search`, `sap-docs-community`, `sap-notes`.
- Response layout: Executive summary, Mermaid signal flow diagram, followed by Developer, Architect, and Governance perspectives.
- No decorative emojis in tool outputs or code generation.
