# SAP MCP Agent Starter Kit — Community Edition

Zero-Config AI Agent Starter Kit for SAP BTP Integration Suite & API Management.  
Designed for students, academic labs, and self-study.

> **License Notice:** This Community Edition is licensed under the **PolyForm Noncommercial License 1.0.0** (Academic & Student Use Only).  
> For commercial use, customer deliverables, or enterprise deployment, the **SAP MCP Consultant Edition** (including all 11 enterprise servers, Clean Core Simplification Database, 37 Reference Architectures, and BTP FinOps Estimators) is available under a commercial license from Next Chapter Experts.

---

## 1. Universal Zero-Config IDE Support

Open this repository in your preferred AI IDE. No file copying, renaming, or manual setup required:

* **Google Antigravity / Gemini CLI:** Automatically reads `GEMINI.md`.
* **Cursor:** Automatically applies `.cursorrules`.
* **Claude Code:** Automatically reads `CLAUDE.md`.
* **Windsurf:** Automatically applies `.windsurfrules`.
* **xAI Grok / Grok Build:** Automatically reads `GROK.md`.
* **Universal Agent Standard:** Reads `AGENTS.md` and `.agents/skills/student-copilot/SKILL.md`.

---

## 2. Quickstart Lab Guide (4 Steps)

### Step 1: Clone Repository
```bash
git clone https://github.com/NextChapterExperts/sap-mcp-agent-starter-kit.git
cd sap-mcp-agent-starter-kit
```

### Step 2: Verify Python Environment (No Pip Packages Required)
```bash
python3 scripts/test_mcp_servers.py
```
Expected output:
```text
======================================================================
Verifying Student MCP Servers (JSON-RPC 2.0 stdio)
======================================================================
[*] Testing: sap_help_mcp_server.py
    [PASS] [initialize] Connected to 'student-sap-help-portal' (v1.0.0)
    [PASS] [tools/list] Registered tools: ['sap_help_search', 'sap_help_get_policy', 'sap_help_list_policies']
    [PASS] [tools/call] Invoked 'sap_help_get_policy': ## SAP APIM Policy: SpikeArrest...
[*] Testing: sap_api_hub_mcp_server.py
    [PASS] [initialize] Connected to 'student-sap-api-hub' (v1.0.0)
    [PASS] [tools/list] Registered tools: ['sap_api_hub_search', 'sap_api_hub_get_api', 'sap_api_hub_list_events']
    [PASS] [tools/call] Invoked 'sap_api_hub_get_api': ## SAP API Specification: Business Partner...
ALL COMMUNITY MCP SERVERS PASSED: Environment ready for AI Agents.
======================================================================
```

### Step 3: Open in Your AI IDE
Launch your IDE in this repository folder:
```bash
antigravity .
# or
cursor .
```

### Step 4: Run Grounded Student Prompts
Test the agent with these real-world scenarios:
* *"Generate an SAP APIM SpikeArrest policy for our student portal with 120 requests per minute."*
* *"What OData v2 entities are available in the Business Partner API, and how do I authenticate against it?"*
* *"Show me how to configure an API Key verification policy in SAP APIM."*

---

## 3. Project Structure

```text
sap-mcp-agent-starter-kit/
├── .agents/
│   └── skills/
│       └── student-copilot/
│           └── SKILL.md       # Student Co-Pilot skill specification
├── .cursorrules               # Auto-loaded rules for Cursor
├── .windsurfrules             # Auto-loaded rules for Windsurf
├── AGENTS.md                  # Universal Agent configuration
├── CLAUDE.md                  # Auto-loaded rules for Claude Code
├── GEMINI.md                  # Auto-loaded rules for Google Antigravity
├── GROK.md                    # Auto-loaded rules for xAI Grok
├── LICENSE                    # PolyForm Noncommercial License 1.0.0
├── README.md                  # Project documentation & lab guide
├── config/
│   └── mcp_config.json        # Community MCP server configuration
├── docs/                      # Technical guides & architecture deep dives
│   ├── MCP_SERVERS_CATALOG.md # Specification of all 11 MCP servers & editions
│   ├── WHAT_IS_MCP.md         # The MCP protocol, transport, and agent mechanics
│   ├── WHAT_IS_MCP_VS_API.md  # Detailed comparison: MCP vs. REST / GraphQL / gRPC
│   └── WHY_MCP_OVER_SCRAPING.md # Why MCP beats web scraping & manual search
└── scripts/
    ├── sap_help_mcp_server.py # Pure Python: APIM XML policies & Help search
    ├── sap_api_hub_mcp_server.py # Pure Python: OData models & CloudEvents
    └── test_mcp_servers.py    # Automated test harness for local servers
```

---

## 4. Community vs. Consultant Edition Matrix

| Feature / Data Source | Community Edition (This Repo) | Consultant Edition (Commercial) |
|---|:---:|:---:|
| **License** | PolyForm Noncommercial (Academic) | Commercial Enterprise License |
| **sap-help (APIM XML Policies)** | Included | Included |
| **sap-api-hub (OData & Events)** | Included | Included |
| **sap-developers-search** | Included | Included |
| **sap-docs-community & sap-notes** | Included | Included |
| **sap-arch-center (37 Reference Archs & RA0029)** | - | **Included** |
| **sap-process-navigator (Scope Items 2DB/190)** | - | **Included** |
| **sap-simplification (Clean Core Contract C1)** | - | **Included** |
| **sap-discovery-pricing (BTP CPEA FinOps)** | - | **Included** |
| **sap-github (github.com/SAP Code Samples)** | - | **Included** |
| **Role-Based Edition Skills (Architect & FinOps)** | - | **Included** |

---

## 5. Architectural Deep Dives (Documentation)

Explore the conceptual guides in `docs/`:

* 📚 **[Enterprise MCP Server Catalog & Technical Specification](docs/MCP_SERVERS_CATALOG.md)**  
  Full technical breakdown of all 11 MCP servers: tools, JSON schemas, parameters, sample payloads, and offline SSoT resilience.
* 📖 **[What is the Model Context Protocol (MCP)?](docs/WHAT_IS_MCP.md)**  
  Architectural overview, stdio vs. SSE transports, building zero-dependency Python MCP servers, the JSON-RPC 2.0 lifecycle, and the four layers of autonomous agents.
* 🔌 **[What is an MCP Server vs. a Traditional API?](docs/WHAT_IS_MCP_VS_API.md)**  
  Detailed comparison of deterministic compile-time APIs (REST, GraphQL, gRPC) versus probabilistic runtime tool execution by LLMs.
* 🛡️ **[Why Use MCP Over Web Scraping & Manual Search?](docs/WHY_MCP_OVER_SCRAPING.md)**  
  Technical analysis of SPA hydration traps, WAF/Akamai bot blocking, token pruning economics, and legal Terms of Service compliance.
