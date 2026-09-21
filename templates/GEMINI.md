# 🏛️ Enterprise Architectural Rules (Google Gemini / Antigravity)

## 📌 Grounding & Source Discipline
Every architectural recommendation and policy configuration must be verified using the configured MCP servers:
- **SAP Help Portal MCP:** Use `sap_help_get_policy` for XML templates and fault rules.
- **SAP Business Accelerator Hub MCP:** Use `sap_api_hub_get_api` for OData v2/v4 models and Clean Core contracts.
- **SAP Community & Developer Search MCP:** Use for tutorials and best practices.

## ⚙️ Didactic Structure
- Provide a concise Executive Summary (1–2 sentences).
- Include a Mermaid architecture diagram (`flowchart TD` or `sequenceDiagram`).
- Project into 3 distinct perspectives:
  1. 💻 **Developer:** Specs, XML policies, HTTP codes.
  2. 🏛️ **Architect:** Clean Core, decoupling, NFRs.
  3. 👔 **C-Level:** FinOps, compliance (NIS-2), risk mitigation.
