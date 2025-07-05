# 文件消息类型文档

## 概述

文件消息类型用于向企业微信群发送文件，支持各种文件格式。发送文件消息需要先通过文件上传接口获取 `media_id`，然后使用该 `media_id` 发送消息。

## 消息格式

### JSON 结构

```json
{
    "msgtype": "file",
    "file": {
        "media_id": "3a8asd892asd8asd"
    }
}
```

### 参数说明

| 参数 | 是否必填 | 类型 | 说明 |
|------|----------|------|------|
| `msgtype` | 是 | string | 消息类型，此时固定为 `file` |
| `file` | 是 | object | 文件对象 |
| `file.media_id` | 是 | string | 文件id，通过文件上传接口获取 |

## 文件上传接口

### 接口地址

```
POST https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file
```

### 请求方式

- **方法**: POST
- **Content-Type**: multipart/form-data

### 请求参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| `key` | 是 | 企业微信机器人的 webhook 密钥 |
| `type` | 是 | 媒体文件类型，固定为 `file` |
| `media` | 是 | 文件内容，form-data 格式 |

### 响应格式

**成功响应：**
```json
{
    "errcode": 0,
    "errmsg": "ok",
    "type": "file",
    "media_id": "3a8asd892asd8asd",
    "created_at": "1380000000"
}
```

**错误响应：**
```json
{
    "errcode": 40004,
    "errmsg": "invalid media size"
}
```

## 限制条件

### 文件大小限制
- **最大文件大小**: 20MB
- **文件格式**: 支持各种文件格式（如 PDF、DOC、XLS、PPT、ZIP、RAR 等）

### Media ID 限制
- **有效期**: 3天
- **使用次数**: 不限制

## 使用示例

### 1. 使用 curl 上传文件

```bash
curl -X POST \
  "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=YOUR_KEY&type=file" \
  -H "Content-Type: multipart/form-data" \
  -F "media=@/path/to/your/file.pdf"
```

### 2. 使用 Python 上传文件

```python
import requests

def upload_file(file_path, webhook_key):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webhook_key}&type=file"
    
    with open(file_path, 'rb') as f:
        files = {'media': (file_path, f, 'application/octet-stream')}
        response = requests.post(url, files=files)
    
    result = response.json()
    if result.get('errcode') == 0:
        return result['media_id']
    else:
        raise Exception(f"上传失败: {result.get('errmsg')}")
```

### 3. 发送文件消息

```python
import requests
import json

def send_file_message(media_id, webhook_key):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    
    data = {
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }
    
    response = requests.post(url, json=data)
    return response.json()

# 完整流程
webhook_key = "YOUR_WEBHOOK_KEY"
file_path = "/path/to/document.pdf"

# 1. 上传文件获取 media_id
media_id = upload_file(file_path, webhook_key)

# 2. 发送文件消息
result = send_file_message(media_id, webhook_key)
print(result)
```

### 4. 使用 MCP 服务器工具

```python
# 使用 qyweixin_file 工具函数
result = qyweixin_file(file_path="/path/to/document.pdf")
```

## 常见错误码

| 错误码 | 错误信息 | 说明 |
|--------|----------|------|
| 40001 | invalid key | webhook key 无效 |
| 40003 | invalid media_id | media_id 无效或已过期 |
| 40004 | invalid media size | 文件大小超出限制 |
| 40005 | invalid file type | 不支持的文件类型 |
| 93000 | invalid file | 文件内容无效 |

## 最佳实践

### 1. 文件大小控制
- 发送前检查文件大小，确保不超过 20MB
- 对于大文件，建议压缩后发送

### 2. 错误处理
- 上传失败时进行重试
- 检查 media_id 的有效期

### 3. 文件命名
- 使用有意义的文件名
- 避免使用特殊字符

### 4. 安全考虑
- 不要发送敏感信息
- 确保文件来源可信

## 注意事项

1. **Media ID 有效期**: 上传后的 media_id 有效期为3天，超过有效期需要重新上传
2. **文件格式**: 理论上支持所有文件格式，但建议使用常见的办公文档格式
3. **文件大小**: 单个文件不能超过 20MB
4. **上传频率**: 避免频繁上传大文件，可能会被限制
5. **文件安全**: 企业微信会对上传的文件进行安全检查

## 相关链接

- [企业微信机器人配置说明](https://developer.work.weixin.qq.com/document/path/91770)
- [群机器人配置说明](https://developer.work.weixin.qq.com/document/path/91770#%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F) 