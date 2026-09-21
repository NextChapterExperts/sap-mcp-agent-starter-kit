# xAI Grok / Grok Build Enterprise Architecture Rules

## 1. Grounding & Mandatory MCP Tool Discipline
Every architectural proposal, code snippet, and policy configuration must be verified against the five configured Model Context Protocol (MCP) servers:
1. **sap-help-portal-local:** Use `sap_help_get_policy` for APIM XML schemas (`SpikeArrest`, `Quota`, `VerifyAPIKey`, `RaiseFault`, `JSONThreatProtection`), parameters, and fault rules.
2. **sap-api-hub-local:** Use `sap_api_hub_get_api` for S/4HANA OData v2/v4 entity sets, REST endpoints, and `sap_api_hub_list_events` for CloudEvents 1.0 (SAP Event Mesh).
3. **sap-notes:** Search official SAP Support Notes and KBAs on `me.sap.com` for release restrictions and bug notes.
4. **sap-docs-community:** Search community blogs, ABAP Cloud Feature Matrix, and SAP Discovery Center.
5. **sap-developers-search:** Search official developer tutorials and guided missions on `developers.sap.com`.

Do not hallucinate XML namespaces, parameter names, or HTTP status codes.

## 2. Response Delivery Standard (Two-Stage Architecture)
Deliver every architectural response using the following structure without decorative emojis or conversational filler:

### Stage 1: Executive Principle & Mermaid Signal Flow
- **Executive Statement:** 1 to 2 precise sentences stating the architectural pattern, trade-offs, and Clean Core alignment.
- **Mermaid Diagram:** A syntax-validated Mermaid diagram (`flowchart TD` or `sequenceDiagram`) with double-quoted edge labels (`-->|"label"|`).

### Stage 2: Three-Perspective Technical Breakdown
- **Developer Perspective:** Concrete endpoints, XML policy configurations, HTTP status codes (401, 429, 503), error condition variables, and payload pruning rules.
- **Solution Architect Perspective:** System boundaries, asynchronous decoupling, Clean Core compliance (Contract C1 Released APIs vs. Classic RFCs), and Integration Cell execution prerequisites.
- **Enterprise Governance Perspective:** FinOps (token economy and APIM licensing), compliance (NIS-2, KRITIS, EU AI Act Article 12 auditability), and IP reputation protection.
