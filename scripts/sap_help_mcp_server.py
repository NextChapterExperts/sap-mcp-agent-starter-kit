#!/usr/bin/env python3
"""
sap_help_mcp_server.py — Didactic MCP Server for SAP Help Portal & APIM Policies
==================================================================================
Educational Model Context Protocol (MCP) server written in pure Python
with zero external dependencies (standard library only).

Protocol Details:
- Transport: stdio (Standard Input / Standard Output)
- Format: JSON-RPC 2.0
- Supported Methods:
  * 'initialize': Protocol handshake and capabilities exchange.
  * 'tools/list': Exposes available tools with strict JSON schemas.
  * 'tools/call': Executes the selected tool and returns structured content.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

# =============================================================================
# 1. Curated Policy Knowledge Base (Offline & Flight-Mode Safe SSoT)
# =============================================================================
POLICY_KNOWLEDGE_BASE = {
    "SpikeArrest": {
        "name": "SpikeArrest",
        "category": "Traffic Management",
        "purpose": "Protects against sudden traffic spikes and Denial of Service (DoS) attacks by smoothing traffic bursts in milliseconds (traffic shaping).",
        "placement": "ProxyEndpoint -> PreFlow (at the very beginning, prior to authentication)",
        "xml_template": """<SpikeArrest async="false" continueOnError="false" enabled="true" xmlns="http://www.sap.com/apimgmt">
    <!-- Rate: Requests per minute (pm) or per second (ps) -->
    <Rate>30ps</Rate>
    <UseEffectiveParam>true</UseEffectiveParam>
</SpikeArrest>""",
        "parameters": [
            {"param": "Rate", "type": "string", "example": "30ps or 100pm", "description": "Permitted rate per second (ps) or minute (pm)."},
            {"param": "UseEffectiveParam", "type": "boolean", "default": "false", "description": "Enables dynamic rate adjustment via variables."}
        ],
        "fault_rules": {
            "error_code": "policies.ratelimit.SpikeArrestViolation",
            "http_status": 429
        },
        "official_doc": "https://help.sap.com/docs/sap-api-management"
    },
    "Quota": {
        "name": "Quota",
        "category": "Traffic Management",
        "purpose": "Business tier rate limiting and billing quotas over prolonged intervals (e.g., 10,000 requests per month per partner).",
        "placement": "ProxyEndpoint -> PreFlow (after VerifyAPIKey to enforce quota per client id)",
        "xml_template": """<Quota async="false" continueOnError="false" enabled="true" type="calendar" xmlns="http://www.sap.com/apimgmt">
    <Allow count="1000" countRef="request.header.allowed_quota"/>
    <Interval ref="request.header.quota_count">1</Interval>
    <TimeUnit ref="request.header.quota_unit">month</TimeUnit>
    <Identifier ref="verifyapikey.verify-api-key.client_id"/>
    <Distributed>true</Distributed>
    <Synchronous>true</Synchronous>
</Quota>""",
        "parameters": [
            {"param": "Allow count", "type": "integer", "description": "Maximum number of allowed requests in the time interval."},
            {"param": "TimeUnit", "type": "string", "values": ["minute", "hour", "day", "month"], "description": "Time unit for quota window."},
            {"param": "Identifier", "type": "string", "description": "Unique key (e.g. client_id or developer app ID)."}
        ],
        "fault_rules": {
            "error_code": "policies.ratelimit.QuotaViolation",
            "http_status": 429
        },
        "official_doc": "https://help.sap.com/docs/sap-api-management"
    },
    "VerifyAPIKey": {
        "name": "VerifyAPIKey",
        "category": "Security",
        "purpose": "Validates the provided API key against registered apps in the Developer Portal.",
        "placement": "ProxyEndpoint -> PreFlow (before Quota and Mediation)",
        "xml_template": """<VerifyAPIKey async="false" continueOnError="false" enabled="true" xmlns="http://www.sap.com/apimgmt">
    <APIKey ref="request.header.APIKey"/>
</VerifyAPIKey>""",
        "parameters": [
            {"param": "APIKey ref", "type": "variable", "example": "request.header.APIKey", "description": "Header or query parameter containing the key."}
        ],
        "fault_rules": {
            "error_code": "steps.oauth.v2.FailedToResolveAPIKey",
            "http_status": 401
        },
        "official_doc": "https://help.sap.com/docs/sap-api-management"
    },
    "RaiseFault": {
        "name": "RaiseFault",
        "category": "Fault Handling (Kill-Switch)",
        "purpose": "Immediately halts pipeline execution and returns a customized emergency error response. Serves as a technical Kill-Switch or Circuit Breaker.",
        "placement": "FaultRules or Conditional Flow (e.g., when Header 'X-Kill-Switch' is active)",
        "xml_template": """<RaiseFault async="false" continueOnError="false" enabled="true" xmlns="http://www.sap.com/apimgmt">
    <FaultResponse>
        <Set>
            <Headers>
                <Header name="Content-Type">application/json</Header>
            </Headers>
            <Payload contentType="application/json">
                {"error": "SERVICE_EMERGENCY_ISOLATION", "message": "Interface temporarily locked by API Governance."}
            </Payload>
            <StatusCode>503</StatusCode>
            <ReasonPhrase>Service Unavailable</ReasonPhrase>
        </Set>
    </FaultResponse>
</RaiseFault>""",
        "parameters": [
            {"param": "StatusCode", "type": "integer", "description": "HTTP status code (e.g. 503 or 403)."}
        ],
        "fault_rules": {
            "error_code": "fault.name = 'RaiseFault'",
            "http_status": 503
        },
        "official_doc": "https://help.sap.com/docs/sap-api-management"
    }
}

# =============================================================================
# 2. Tool Definitions (MCP Schema)
# =============================================================================
TOOLS = [
    {
        "name": "sap_help_search",
        "description": "Searches the official SAP Help Portal (Integration Suite & APIM) for keywords.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term (e.g., 'Spike Arrest', 'OAuth', 'Cloud Connector')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 5)"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "sap_help_get_policy",
        "description": "Retrieves official specification, XML template, parameters, and fault codes for an SAP APIM policy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "policy_name": {
                    "type": "string",
                    "description": "Name of the policy (e.g., 'SpikeArrest', 'Quota', 'VerifyAPIKey', 'RaiseFault')"
                }
            },
            "required": ["policy_name"]
        }
    },
    {
        "name": "sap_help_list_policies",
        "description": "Lists all available APIM policies in the catalog.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]

# =============================================================================
# 3. Tool Implementations (Business Logic)
# =============================================================================
def tool_search(query: str, limit: int = 5) -> str:
    """Executes live query against SAP Help Portal public search API."""
    url = f"https://help.sap.com/http.svc/search?q={urllib.parse.quote(query)}&product=CLOUD_INTEGRATION&language=en-US&state=PRODUCTION"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Student-MCP-Server/1.0", "Accept": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            results = data.get("data", {}).get("results", [])
            if not results:
                return f"No online results found on SAP Help Portal for '{query}'."

            lines = [f"### SAP Help Portal Live Results for '{query}':\n"]
            for r in results[:limit]:
                title = r.get("title", "Untitled")
                link = "https://help.sap.com" + r.get("url", "")
                snippet = r.get("snippet", "").replace("<b>", "**").replace("</b>", "**")
                lines.append(f"- **[{title}]({link})**\n  {snippet}\n")
            return "\n".join(lines)
    except Exception as err:
        # Graceful offline fallback
        matches = [k for k in POLICY_KNOWLEDGE_BASE if query.lower() in k.lower() or query.lower() in POLICY_KNOWLEDGE_BASE[k]["purpose"].lower()]
        if matches:
            return f"(Note: Offline fallback active - {err})\nMatching local policies: {', '.join(matches)}"
        return f"Error connecting to SAP Help Portal: {err}"

def tool_get_policy(policy_name: str) -> str:
    """Returns details and XML template for a policy."""
    policy = POLICY_KNOWLEDGE_BASE.get(policy_name)
    if not policy:
        for k, v in POLICY_KNOWLEDGE_BASE.items():
            if k.lower() == policy_name.lower():
                policy = v
                break
    if not policy:
        return f"Policy '{policy_name}' not found. Available policies: {list(POLICY_KNOWLEDGE_BASE.keys())}"

    out = [
        f"## SAP APIM Policy: {policy['name']}",
        f"**Category:** {policy['category']}",
        f"**Purpose:** {policy['purpose']}",
        f"**Recommended Placement:** `{policy['placement']}`\n",
        "### XML Configuration Template:",
        f"```xml\n{policy['xml_template']}\n```\n",
        "### Parameters:"
    ]
    for p in policy["parameters"]:
        out.append(f"- `{p['param']}` ({p.get('type', 'string')}): {p['description']}")

    fr = policy.get("fault_rules", {})
    if fr:
        out.append("\n### Fault Handling & Status Codes:")
        out.append(f"- **Error Code:** `{fr.get('error_code')}`")
        out.append(f"- **HTTP Status:** `{fr.get('http_status')}`")

    out.append(f"\n**Official Documentation:** {policy['official_doc']}")
    return "\n".join(out)

def tool_list_policies() -> str:
    """Lists all cataloged policies."""
    lines = ["## Available SAP APIM Policies in MCP Server:\n"]
    for k, v in POLICY_KNOWLEDGE_BASE.items():
        lines.append(f"- **{k}** ({v['category']}): {v['purpose']}")
    return "\n".join(lines)

# =============================================================================
# 4. JSON-RPC 2.0 Dispatcher (Core MCP Protocol)
# =============================================================================
def handle_rpc(line: str) -> Optional[str]:
    """Parses one line of JSON-RPC and generates the response."""
    try:
        msg = json.loads(line)
    except Exception:
        return None

    method = msg.get("method")
    req_id = msg.get("id")

    # 1. MCP Handshake
    if method == "initialize":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "student-sap-help-portal",
                    "version": "1.0.0"
                }
            }
        })

    # 2. List tools
    if method == "tools/list":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS}
        })

    # 3. Call tool
    if method == "tools/call":
        params = msg.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})

        if tname == "sap_help_search":
            res = tool_search(args.get("query", ""), args.get("limit", 5))
        elif tname == "sap_help_get_policy":
            res = tool_get_policy(args.get("policy_name", ""))
        elif tname == "sap_help_list_policies":
            res = tool_list_policies()
        else:
            res = f"Unknown tool: {tname}"

        return json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": res}]
            }
        })

    return None

def main():
    """Main stdio loop."""
    sys.stderr.write("🚀 [Student-MCP] SAP Help Portal MCP Server started (stdio mode)\n")
    sys.stderr.flush()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        response = handle_rpc(line)
        if response:
            sys.stdout.write(response + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
