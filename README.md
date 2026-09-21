# 🎓 SAP MCP Agent Starter Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Protocol: MCP](https://img.shields.io/badge/MCP-2024--11--05-brightgreen.svg)](https://modelcontextprotocol.io/)

> **A production-ready, zero-config starter kit for students and engineers to run Model Context Protocol (MCP) servers locally and deploy grounded AI Enterprise Architecture Agents across Google Antigravity, Cursor, Claude Code, Windsurf, and xAI Grok Build.**

---

## 🧭 Table of Contents

1. [Universal Zero-Config IDE Support](#1-universal-zero-config-ide-support)
2. [Quickstart: 4-Step Hands-On Student Lab](#2-quickstart-4-step-hands-on-student-lab)
3. [Repository Layout](#3-repository-layout)
4. [The 5 Pre-Configured MCP Data Sources](#4-the-5-pre-configured-mcp-data-sources)
5. [Architectural Deep Dives (Documentation)](#5-architectural-deep-dives-documentation)
6. [Automated Verification](#6-automated-verification)
7. [License](#7-license)

---

## 1. Universal Zero-Config IDE Support

This repository is engineered for **seamless multi-IDE coexistence**. Because different AI environments look for distinct rule filenames, all configurations sit together in the root directory without conflict. **No file copying, moving, or manual setup scripts are required.**

| Environment | System Rules File (Auto-Loaded) | Multi-Agent Index | Skill Definition Path | MCP Config Location |
| :--- | :--- | :--- | :--- | :--- |
| **Google Antigravity / Gemini** | `GEMINI.md` (root) | `AGENTS.md` (root) | `.agents/skills/student-copilot/SKILL.md` | `config/mcp_config.json` |
| **Anthropic Claude Code** | `CLAUDE.md` (root) | `AGENTS.md` (root) | Built-in tool calling | `claude mcp add` / `.claude.json` |
| **Cursor IDE** | `.cursorrules` (root) | Context rules | `.cursorrules` rules | `~/.cursor/mcp.json` |
| **Windsurf (Cascade)** | `.windsurfrules` (root) | Cascade Memories | Inline workflows | `~/.codeium/windsurf/mcp_config.json` |
| **xAI Grok / Grok Build** | `GROK.md` (root) | `AGENTS.md` (root) | System prompt | IDE Settings / API params |

---

## 2. Quickstart: 4-Step Hands-On Student Lab

### Step 1: Clone the Repository
```bash
git clone https://github.com/NextChapterExperts/sap-mcp-agent-starter-kit.git
cd sap-mcp-agent-starter-kit
```

### Step 2: Verify Local MCP Servers
Execute the automated test runner to ensure protocol compliance and runtime readiness:
```bash
python3 scripts/test_mcp_servers.py
```
*Expected output: Handshakes, tool listings, and sample calls pass with zero errors in under 0.5s.*

### Step 3: Open in Your AI IDE of Choice
Simply open the cloned folder in your environment:
- **Google Antigravity / Gemini:** Open folder. Antigravity automatically detects `GEMINI.md`, `AGENTS.md`, and the `student-copilot` skill in `.agents/skills/`.
- **Cursor:** Open folder. Cursor automatically detects `.cursorrules`. Add servers from `config/mcp_config.json` to your `~/.cursor/mcp.json`.
- **Claude Code:** Launch `claude` in the folder. Claude automatically reads `CLAUDE.md`.
- **Windsurf:** Open folder. Cascade automatically reads `.windsurfrules`.
- **xAI Grok / Grok Build:** Set `GROK.md` as your project system prompt.

### Step 4: Challenge the Architecture Agent
Ask your AI assistant an enterprise integration question:
> *"We need to protect an SAP S/4HANA OData interface against sudden traffic spikes. What APIM policy should we configure, what does its XML look like, and how does it align with SAP Clean Core?"*

**Expected Agent Behavior:**
1. Autonomously calls `sap_help_get_policy(policy_name="SpikeArrest")`.
2. Autonomously calls `sap_api_hub_get_api` to check Clean Core contract classification.
3. Delivers a two-stage response: Executive statement with Mermaid diagram, followed by Developer, Architect, and Governance perspectives.

---

## 3. Repository Layout

```text
sap-mcp-agent-starter-kit/
├── .agents/
│   └── skills/
│       └── student-copilot/
│           └── SKILL.md       # Progressive context skill for Antigravity
├── .cursorrules               # Auto-loaded rules for Cursor IDE
├── .windsurfrules             # Auto-loaded rules for Windsurf (Cascade)
├── AGENTS.md                  # Multi-agent roster and trigger matrix
├── CLAUDE.md                  # Auto-loaded instructions for Claude Code
├── GEMINI.md                  # Auto-loaded rules for Google Antigravity & Gemini CLI
├── GROK.md                    # Auto-loaded rules for xAI Grok / Grok Build
├── LICENSE                    # MIT License
├── README.md                  # Project documentation & lab guide
├── config/
│   └── mcp_config.json        # Unified configuration for all 5 MCP servers
├── docs/                      # Architectural and conceptual deep dives
│   ├── WHAT_IS_MCP.md         # The MCP protocol, transport, and agent mechanics
│   ├── WHAT_IS_MCP_VS_API.md  # Detailed comparison: MCP vs. REST / GraphQL / gRPC
│   └── WHY_MCP_OVER_SCRAPING.md # Why MCP beats web scraping & manual search
└── scripts/
    ├── sap_help_mcp_server.py # Pure Python stdio MCP: APIM XML policies & Help search
    ├── sap_api_hub_mcp_server.py # Pure Python stdio MCP: OData models & CloudEvents
    └── test_mcp_servers.py    # Automated test harness for student verification
```

---

## 4. The 5 Pre-Configured MCP Data Sources

All agents and system rules in this repository are grounded against five authoritative data sources configured in `config/mcp_config.json`:

| Server Name | Transport | Responsibility & Toolsets |
| :--- | :--- | :--- |
| **`sap-help-portal-local`** | Local stdio (Python) | Authoritative APIM XML policies (`SpikeArrest`, `Quota`, `VerifyAPIKey`, `RaiseFault`) via `sap_help_get_policy` and live documentation search via `sap_help_search`. |
| **`sap-api-hub-local`** | Local stdio (Python) | S/4HANA OData v2/v4 models, authentication methods, Clean Core ratings via `sap_api_hub_get_api`, and CloudEvents via `sap_api_hub_list_events`. |
| **`sap-notes`** | Hosted stdio (npx) | Official SAP Support Notes, KBAs, and release notes on `me.sap.com`. |
| **`sap-docs-community`** | Remote HTTP / SSE | Semantic vector search across SAP Community blogs, ABAP Cloud Feature Matrix, and Discovery Center. |
| **`sap-developers-search`** | Remote HTTP / SSE | Official tutorials, hands-on missions, and code samples on `developers.sap.com`. |

---

## 5. Architectural Deep Dives (Documentation)

For in-depth conceptual and architectural foundations, explore the guides in `docs/`:

* 📖 **[What is the Model Context Protocol (MCP)?](docs/WHAT_IS_MCP.md)**  
  Architectural overview, stdio vs. SSE transports, building zero-dependency Python MCP servers, the JSON-RPC 2.0 lifecycle, and the four layers of autonomous agents.
* 🔌 **[What is an MCP Server vs. a Traditional API?](docs/WHAT_IS_MCP_VS_API.md)**  
  Detailed comparison of deterministic compile-time APIs (REST, GraphQL, gRPC) versus probabilistic runtime tool execution by LLMs.
* 🛡️ **[Why Use MCP Over Web Scraping & Manual Search?](docs/WHY_MCP_OVER_SCRAPING.md)**  
  Technical analysis of SPA hydration traps, WAF/Akamai bot blocking, token pruning economics, and legal Terms of Service compliance.

---

## 6. Automated Verification

Students can verify their environment anytime:

```bash
$ python3 scripts/test_mcp_servers.py
======================================================================
🚀 Verifying Student MCP Servers (JSON-RPC 2.0 stdio)
======================================================================

👉 Testing: sap_help_mcp_server.py
   ✅ [initialize] Connected to 'student-sap-help-portal' (v1.0.0)
   ✅ [tools/list] Registered tools: ['sap_help_search', 'sap_help_get_policy', 'sap_help_list_policies']
   ✅ [tools/call] Invoked 'sap_help_get_policy': ## SAP APIM Policy: SpikeArrest...

👉 Testing: sap_api_hub_mcp_server.py
   ✅ [initialize] Connected to 'student-sap-api-hub' (v1.0.0)
   ✅ [tools/list] Registered tools: ['sap_api_hub_search', 'sap_api_hub_get_api', 'sap_api_hub_list_events']
   ✅ [tools/call] Invoked 'sap_api_hub_get_api': ## SAP API Specification: Business Partner (A2X)...

🎉 ALL TESTS PASSED! Your MCP servers are ready for AI Agents.
======================================================================
```

---

## 7. License

This project is licensed under the [MIT License](LICENSE).
