# MCP integration path

The `mcp_server/server.py` file is a real MCP tool server using FastMCP. The LangGraph demo keeps direct Python calls for a zero-dependency local execution path. To make the architecture fully MCP-native, replace `app.tools` with an MCP client layer and route each tool invocation through the MCP server.

This deliberate separation is useful in interviews: it distinguishes **agent orchestration** from **tool protocol / integration**.
