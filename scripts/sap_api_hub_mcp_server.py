#!/usr/bin/env python3
"""
sap_api_hub_mcp_server.py — Didactic MCP Server for SAP Business Accelerator Hub
==================================================================================
Educational Model Context Protocol (MCP) server providing access to SAP Business
Accelerator Hub (api.sap.com) metadata, OData services, and CloudEvents.

Protocol Details:
- Transport: stdio (Standard Input / Standard Output)
- Format: JSON-RPC 2.0
- Tools:
  1. 'sap_api_hub_search': Search APIs and integration packages.
  2. 'sap_api_hub_get_api': Retrieve endpoints, OData entities, auth schemes, and Clean Core status.
  3. 'sap_api_hub_list_events': Query CloudEvents specifications for Event-Driven Architectures.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

# =============================================================================
# 1. Curated Reference APIs (Offline SSoT for Labs & Classrooms)
# =============================================================================
API_CATALOG = {
    "API_BUSINESS_PARTNER": {
        "title": "Business Partner (A2X) - OData v2/v4",
        "package": "SAP S/4HANA Cloud Public Edition",
        "protocol": "OData v2 / OData v4",
        "type": "Inbound / Outbound",
        "auth": ["OAuth 2.0 (mTLS)", "Basic Authentication", "Principal Propagation"],
        "description": "Central enterprise service to read, create, and update business partners, customers, suppliers, addresses, and bank accounts.",
        "entities": [
            "A_BusinessPartner (General data, status, blocks)",
            "A_BusinessPartnerAddress (Postal addresses)",
            "A_Customer (Customer master data)",
            "A_Supplier (Supplier master data)"
        ],
        "clean_core_status": "Released API (Contract C1) — Upgrade-stable",
        "url": "https://api.sap.com/api/API_BUSINESS_PARTNER/overview"
    },
    "API_UTILITIES_METER_READING": {
        "title": "Utilities Meter Reading Document (IS-U / Energy)",
        "package": "SAP S/4HANA Utilities",
        "protocol": "REST / OData",
        "type": "Inbound / Outbound",
        "auth": ["OAuth 2.0", "Client Credentials"],
        "description": "High-throughput ingestion and validation of meter readings (Smart Meter Rollout, 15-minute load profiles, periodic readings) for energy utilities.",
        "entities": [
            "MeterReadingDocument (Reading confirmation)",
            "MeterReadingReason (Reading reason: periodic, move-in, move-out)",
            "Register (Physical register / tariff meter)"
        ],
        "clean_core_status": "Clean Core Tier 2 / Cloud Extensibility API",
        "url": "https://api.sap.com/package/SAPS4HANAUtilities/overview"
    },
    "BTP_DESTINATION_SERVICE": {
        "title": "SAP BTP Destination Service API v1",
        "package": "SAP BTP Connectivity Services",
        "protocol": "REST (OpenAPI)",
        "type": "Platform API",
        "auth": ["OAuth 2.0 Client Credentials (XSUAA)"],
        "description": "Management and runtime retrieval of outbound destinations, mTLS certificates, and token exchange for secure SAP backend connectivity.",
        "entities": [
            "GET /destination-configuration/v1/destinations/{name} (Destination metadata & dynamic token fetch)",
            "GET /destination-configuration/v1/certificates/{name} (Certificate download for mTLS handshake)"
        ],
        "clean_core_status": "BTP Native Foundation Service",
        "url": "https://api.sap.com/api/SAP_CP_CF_Connectivity_DestinationService/overview"
    }
}

EVENT_CATALOG = [
    {
        "topic": "sap/s4/beh/businesspartner/v1/BusinessPartner/Created/v1",
        "name": "Business Partner Created",
        "format": "CloudEvents 1.0 (JSON)",
        "description": "Emitted when a new business partner is created in SAP S/4HANA. Ideal trigger for SAP Event Mesh -> Cloud Integration pipelines.",
        "spec_version": "1.0"
    },
    {
        "topic": "sap/s4/beh/utilities/meterreading/v1/MeterReading/Entered/v1",
        "name": "Utilities Meter Reading Entered",
        "format": "CloudEvents 1.0 (JSON)",
        "description": "Signals new incoming meter reading values for plausibility checks and billing in Meter-to-Cash flows.",
        "spec_version": "1.0"
    }
]

# =============================================================================
# 2. Tool Definitions (MCP Schema)
# =============================================================================
TOOLS = [
    {
        "name": "sap_api_hub_search",
        "description": "Searches the SAP Business Accelerator Hub (api.sap.com) for OData and REST APIs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term (e.g., 'Business Partner', 'Meter Reading', 'Destination')"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "sap_api_hub_get_api",
        "description": "Provides technical specifications, entities, authentication methods, and Clean Core rating for an SAP API.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "api_name": {
                    "type": "string",
                    "description": "Technical key or name (e.g., 'API_BUSINESS_PARTNER', 'API_UTILITIES_METER_READING')"
                }
            },
            "required": ["api_name"]
        }
    },
    {
        "name": "sap_api_hub_list_events",
        "description": "Retrieves available CloudEvents (SAP Event Mesh) for event-driven architectural decoupling.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filter_topic": {
                    "type": "string",
                    "description": "Optional filter keyword (e.g., 'businesspartner' or 'meterreading')"
                }
            }
        }
    }
]

# =============================================================================
# 3. Tool Implementations (Business Logic)
# =============================================================================
def tool_search(query: str) -> str:
    """Searches catalog entries."""
    q = query.lower()
    matches = []
    for key, item in API_CATALOG.items():
        if (q in key.lower() or 
            q in item["title"].lower() or 
            q in item["description"].lower()):
            matches.append((key, item))

    if not matches:
        return f"No APIs found in local catalog for '{query}'. Try searching for 'Business Partner', 'Meter Reading', or 'Destination'."

    out = [f"### Found SAP APIs for '{query}':\n"]
    for key, item in matches:
        out.append(f"- **{key}**: {item['title']}")
        out.append(f"  * Package: `{item['package']}` | Protocol: `{item['protocol']}`")
        out.append(f"  * Clean Core: {item['clean_core_status']}")
        out.append(f"  * Documentation: {item['url']}\n")
    return "\n".join(out)

def tool_get_api(api_name: str) -> str:
    """Returns technical details of an API."""
    key = api_name.strip()
    item = API_CATALOG.get(key)
    if not item:
        for k, v in API_CATALOG.items():
            if k.lower() == key.lower():
                item = v
                key = k
                break

    if not item:
        return f"API '{api_name}' not found. Available keys: {list(API_CATALOG.keys())}"

    out = [
        f"## SAP API Specification: {item['title']}",
        f"**Technical Key:** `{key}`",
        f"**Package:** {item['package']}",
        f"**Protocol:** {item['protocol']}",
        f"**Direction:** {item['type']}",
        f"**Clean Core Rating:** {item['clean_core_status']}\n",
        f"### Overview:\n{item['description']}\n",
        "### Supported Authentication Schemes:"
    ]
    for a in item["auth"]:
        out.append(f"- {a}")

    out.append("\n### Core Entities / Endpoints:")
    for e in item["entities"]:
        out.append(f"- `{e}`")

    out.append(f"\n**Direct Link:** {item['url']}")
    return "\n".join(out)

def tool_list_events(filter_topic: Optional[str] = None) -> str:
    """Lists enterprise CloudEvents."""
    events = EVENT_CATALOG
    if filter_topic:
        ft = filter_topic.lower()
        events = [e for e in events if ft in e["topic"].lower() or ft in e["name"].lower()]

    if not events:
        return f"No events found matching '{filter_topic}'."

    out = ["## Available SAP CloudEvents (Event-Driven Architecture):\n"]
    for ev in events:
        out.append(f"### Event: {ev['name']}")
        out.append(f"- **Topic:** `{ev['topic']}`")
        out.append(f"- **Format:** {ev['format']}")
        out.append(f"- **Pattern:** {ev['description']}\n")
    return "\n".join(out)

# =============================================================================
# 4. JSON-RPC Dispatcher
# =============================================================================
def handle_rpc(line: str) -> Optional[str]:
    try:
        msg = json.loads(line)
    except Exception:
        return None

    method = msg.get("method")
    req_id = msg.get("id")

    if method == "initialize":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "student-sap-api-hub",
                    "version": "1.0.0"
                }
            }
        })

    if method == "tools/list":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS}
        })

    if method == "tools/call":
        params = msg.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})

        if tname == "sap_api_hub_search":
            res = tool_search(args.get("query", ""))
        elif tname == "sap_api_hub_get_api":
            res = tool_get_api(args.get("api_name", ""))
        elif tname == "sap_api_hub_list_events":
            res = tool_list_events(args.get("filter_topic"))
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
    sys.stderr.write("🚀 [Student-MCP] SAP API Hub MCP Server started (stdio mode)\n")
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
