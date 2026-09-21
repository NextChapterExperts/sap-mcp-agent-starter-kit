#!/usr/bin/env python3
"""
test_mcp_servers.py — Verification Test Runner for Student MCP Servers
=======================================================================
Run this script to verify that your local MCP servers conform to the
Model Context Protocol JSON-RPC 2.0 specification.

Usage:
    python3 scripts/test_mcp_servers.py
"""

import json
import os
import subprocess
import sys

def test_server(script_name: str, test_tool: str, test_args: dict):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, script_name)
    
    print(f"\n👉 Testing: {script_name}")
    print(f"   Path: {script_path}")

    proc = subprocess.Popen(
        [sys.executable, script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        # Step 1: initialize handshake
        init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize"}
        proc.stdin.write(json.dumps(init_req) + "\n")
        proc.stdin.flush()
        init_resp = json.loads(proc.stdout.readline())
        assert init_resp.get("result", {}).get("protocolVersion") == "2024-11-05"
        server_info = init_resp["result"]["serverInfo"]
        print(f"   ✅ [initialize] Connected to '{server_info['name']}' (v{server_info['version']})")

        # Step 2: tools/list
        list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
        proc.stdin.write(json.dumps(list_req) + "\n")
        proc.stdin.flush()
        list_resp = json.loads(proc.stdout.readline())
        tools = [t["name"] for t in list_resp.get("result", {}).get("tools", [])]
        print(f"   ✅ [tools/list] Registered tools: {tools}")

        # Step 3: tools/call
        call_req = {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": test_tool, "arguments": test_args}}
        proc.stdin.write(json.dumps(call_req) + "\n")
        proc.stdin.flush()
        call_resp = json.loads(proc.stdout.readline())
        content = call_resp.get("result", {}).get("content", [])
        assert len(content) > 0
        first_line = content[0]["text"].splitlines()[0] if content[0]["text"] else ""
        print(f"   ✅ [tools/call] Invoked '{test_tool}': {first_line[:60]}...")

    finally:
        proc.terminate()

def main():
    print("=" * 70)
    print("🚀 Verifying Student MCP Servers (JSON-RPC 2.0 stdio)")
    print("=" * 70)

    try:
        test_server("sap_help_mcp_server.py", "sap_help_get_policy", {"policy_name": "SpikeArrest"})
        test_server("sap_api_hub_mcp_server.py", "sap_api_hub_get_api", {"api_name": "API_BUSINESS_PARTNER"})
        print("\n🎉 ALL TESTS PASSED! Your MCP servers are ready for AI Agents.")
        print("=" * 70)
    except Exception as exc:
        print(f"\n❌ Test failed: {exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
