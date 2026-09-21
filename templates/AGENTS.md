# 🧭 Multi-Agent Directory & Quick-Reference Matrix

This document provides a single source of truth for all autonomous agents, personas, and trigger prefixes active in this project.

---

## 🤖 Agent Matrix

| Agent / Persona | Trigger / Mode | Core Mission | Essential Tools & MCPs |
| :--- | :--- | :--- | :--- |
| **Solution Architecture Co-Pilot** | Free text / Questions | Architectural sparring on BTP Integration Suite, APIM, Clean Core | `sap_help_get_policy`<br>`sap_api_hub_get_api`<br>`sap_docs_community` |
| **Content & Fact-Check Critic** | `#review-arch`<br>`#fact-check` | Rigorous verification of architectural blueprints against SAP standards | `sap_help_search`<br>`sap-developers-search` |

---

## 🎯 Architectural Guardrails for Agents
1. **Zero Hallucinations:** Never guess XML policy syntax or HTTP error codes. Use MCP tools to verify official parameters.
2. **Layered Explanation:** Always provide Developer, Architect, and Management insights for enterprise decisions.
