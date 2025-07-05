# 企业微信机器人MCP服务器测试集

本目录包含了企业微信机器人MCP服务器的完整测试集，用于测试所有支持的消息类型和功能。

## 📁 测试文件结构

```
tests/
├── test_utils.py          # 测试工具和辅助函数
├── test_text.py           # 文本消息测试
├── test_markdown.py       # Markdown消息测试
├── test_markdown_v2.py    # Markdown_v2消息测试
├── test_image.py          # 图片消息测试
├── test_news.py           # 图文消息测试
├── test_template_card.py  # 模板卡片消息测试
├── test_all.py            # 主测试集（运行所有测试）
└── README.md              # 本文档
```

## 🚀 快速开始

### 1. 设置环境变量

在运行测试之前，请确保设置了企业微信机器人的webhook密钥：

```bash
export QYWEIXIN_KEY="your_webhook_key_here"
```

### 2. 运行所有测试

```bash
cd tests
python test_all.py
```

或者直接运行：

```bash
./test_all.py
```

### 3. 运行单个测试

```bash
python test_text.py           # 测试文本消息
python test_markdown.py       # 测试Markdown消息
python test_markdown_v2.py    # 测试Markdown_v2消息
python test_image.py          # 测试图片消息
python test_news.py           # 测试图文消息
python test_template_card.py  # 测试模板卡片消息
python test_utils.py          # 测试工具函数
```

## 📋 测试覆盖范围

### 文本消息测试
- 简单文本消息
- 带表情符号的文本
- 长文本消息
- 包含特殊字符的文本

### Markdown消息测试
- 简单Markdown格式
- 包含代码块的Markdown
- 带颜色的Markdown
- 通知类型的Markdown消息

### Markdown_v2消息测试
- 表格格式
- 图片链接
- 代码块
- 复杂格式组合

### 图片消息测试
- 从URL获取图片
- 小尺寸图片
- Base64编码图片

### 图文消息测试
- 单篇图文消息
- 多篇图文消息
- 无图片的图文消息
- 最大数量图文消息（8篇）

### 模板卡片消息测试
- 简单文本通知卡片
- 完整文本通知卡片
- 图文展示卡片
- 带操作菜单的卡片

### 工具函数测试
- 消息类型列表查询
- 消息格式查询
- 上传功能测试（如果支持）

## 🔧 配置要求

### 环境变量
- `QYWEIXIN_KEY`: 企业微信机器人的webhook密钥

### Python依赖
- `requests`: HTTP请求库
- `base64`: Base64编码库
- `hashlib`: 哈希计算库
- `json`: JSON处理库

## 📊 测试结果示例

```
🚀 企业微信机器人MCP服务器测试集
============================================================
📋 测试计划:
   1. 文本消息测试 (test_text.py)
   2. Markdown消息测试 (test_markdown.py)
   3. Markdown_v2消息测试 (test_markdown_v2.py)
   4. 图片消息测试 (test_image.py)
   5. 图文消息测试 (test_news.py)
   6. 模板卡片消息测试 (test_template_card.py)
   7. 工具函数测试 (test_utils.py)

============================================================
📊 测试总结
============================================================
⏱️  总用时: 45.32秒
📈 通过率: 7/7 (100.0%)

📋 详细结果:
   ✅ 文本消息测试
   ✅ Markdown消息测试
   ✅ Markdown_v2消息测试
   ✅ 图片消息测试
   ✅ 图文消息测试
   ✅ 模板卡片消息测试
   ✅ 工具函数测试

🎉 所有测试通过！
```

## 🐛 故障排除

### 1. 环境变量未设置
```
❌ 错误: 未设置QYWEIXIN_KEY环境变量
💡 解决: export QYWEIXIN_KEY="your_webhook_key_here"
```

### 2. 网络连接问题
```
❌ 错误: requests.exceptions.ConnectionError
💡 解决: 检查网络连接和防火墙设置
```

### 3. 图片下载失败
```
❌ 错误: 图片处理失败
💡 解决: 检查图片URL是否可访问
```

### 4. 消息发送失败
```
❌ 错误: 发送消息失败
💡 解决: 检查webhook密钥是否正确
```

## 📝 注意事项

1. **测试频率**: 避免过于频繁的测试，以免触发企业微信的频率限制
2. **数据隐私**: 测试数据不包含敏感信息
3. **网络依赖**: 图片测试需要网络连接
4. **环境隔离**: 建议在测试环境中运行，避免影响生产环境

## 🤝 贡献指南

如果您想添加新的测试用例：

1. 在相应的测试文件中添加新的测试函数
2. 遵循现有的命名规范：`test_功能描述()`
3. 添加详细的文档字符串
4. 确保测试函数返回布尔值表示成功或失败
5. 更新相关的README文档

## 📄 许可证

本测试集遵循与主项目相同的许可证。 