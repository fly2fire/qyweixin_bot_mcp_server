# qyweixin_bot_mcp_server
企业微信群通知机器人

```json
{
  "mcpServers": {
    "qyweixin_bot": {
      "disabled": false,
      "timeout": 60,
      "command": "python",
      "args": [
        "D:\\code\\qyweixin_bot_mcp_server\\server.py"
      ],
      "env": {
        "key": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "PYTHONIOENCODING": "utf-8"
      },
      "transportType": "stdio",
      "alwaysAllow": []
    }
  }
}
```