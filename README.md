# qyweixin_bot_mcp_server

企业微信群通知机器人 MCP 服务器

## 项目介绍

这是一个基于 MCP (Model Context Protocol) 的企业微信群通知机器人服务器，支持通过 AI 助手向企业微信群发送各种类型的消息。

## 功能特性

- 🤖 **MCP 协议支持**：基于 FastMCP 框架，与 Claude 等 AI 助手无缝集成
- 📱 **完整消息类型支持**：支持企业微信群机器人的所有 8 种消息类型
- 🔧 **智能文件处理**：自动处理图片、文件上传和格式转换
- 🔐 **安全认证**：支持 webhook 密钥验证
- 📊 **丰富内容格式**：支持 Markdown、模板卡片、图文消息等

## 支持的消息类型

| 消息类型 | 说明 | 特性 |
|---------|------|------|
| `text` | 文本消息 | 支持 @用户、换行、超链接 |
| `markdown` | Markdown 消息 | 基础 Markdown 语法支持 |
| `markdown_v2` | 增强 Markdown | 支持表格、代码块、图片等 |
| `image` | 图片消息 | 支持 URL、本地文件、base64 |
| `news` | 图文消息 | 支持多图文，可跳转链接 |
| `file` | 文件消息 | 自动上传文件获取 media_id |
| `voice` | 语音消息 | 支持 AMR 格式语音文件 |
| `template_card` | 模板卡片 | 支持文本通知卡片和图文展示卡片 |

## 安装和配置

### 1. 克隆项目
```bash
git clone https://github.com/fly2fire/qyweixin_bot_mcp_server.git
cd qyweixin_bot_mcp_server
```

### 2. 安装依赖
```bash
pip install fastmcp requests pillow
```

### 3. 获取企业微信群机器人 Webhook 密钥
1. 在企业微信群中添加机器人
2. 获取 Webhook URL 中的 `key` 参数
3. 配置到 Claude Desktop 中

### 4. 配置 Claude Desktop

在 Claude Desktop 的配置文件中添加：

```json
{
  "mcpServers": {
    "qyweixin_bot": {
      "disabled": false,
      "timeout": 60,
      "command": "python",
      "args": [
        "/path/to/your/qyweixin_bot_mcp_server/server.py"
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

> **注意**：将 `key` 替换为你的实际企业微信群机器人 Webhook 密钥

## 使用方法

### 工具函数

#### 1. qyweixin_notice
发送各种类型的消息到企业微信群

**参数说明：**
- `message_type`: 消息类型（text, markdown, markdown_v2, image, news, file, voice, template_card）
- `content`: 消息内容（根据消息类型不同而不同）

#### 2. qyweixin_upload_media
上传文件到企业微信，获取 media_id

**参数说明：**
- `file_path`: 文件路径
- `media_type`: 媒体类型（file 或 voice）

### 使用示例

#### 发送文本消息
```
请向企业微信群发送文本消息：今天的工作会议将在下午2点开始。
```

#### 发送图片消息
```
请向企业微信群发送这张图片：/path/to/image.jpg
```

#### 发送 Markdown 消息
```
请向企业微信群发送 Markdown 格式的周报：
# 本周工作总结
- 完成了项目 A 的开发
- 修复了 3 个 bug
- 准备下周的产品发布
```

#### 发送模板卡片
```
请向企业微信群发送一个通知卡片，标题是"重要通知"，内容是"请大家及时查看邮件"。
```

## 技术规范

### 消息限制
- 文本消息：最长 2048 字节
- Markdown 消息：最长 4096 字节
- 图片文件：最大 2MB
- 语音文件：最大 2MB，仅支持 AMR 格式
- 普通文件：最大 20MB

### 图片处理
- 支持 URL 链接、本地文件路径、base64 编码
- 自动进行 MD5 校验
- 支持 JPG、PNG、GIF 等常见格式

### 错误处理
- 网络超时：30 秒
- 文件大小检查
- 格式验证
- 详细错误信息返回

## 注意事项

1. **环境变量**：确保正确设置企业微信群机器人的 `key`
2. **文件路径**：使用绝对路径避免文件找不到的问题
3. **网络环境**：确保服务器能够访问企业微信 API
4. **频率限制**：注意企业微信的 API 调用频率限制
5. **权限验证**：确保机器人有发送消息的权限

## 常见问题

### Q: 消息发送失败怎么办？
A: 检查网络连接、验证 key 是否正确、确认文件大小是否超限

### Q: 图片显示不出来？
A: 确认图片格式是否支持、文件大小是否超过 2MB、网络是否可访问

### Q: 如何发送@某人的消息？
A: 在 text 类型消息中使用 `<@userid>` 格式，需要知道用户的 userid

## 贡献

欢迎提交 Issue 和 Pull Request 来完善这个项目。

## 许可证

MIT License

## 联系方式

如有问题请通过 GitHub Issues 联系。