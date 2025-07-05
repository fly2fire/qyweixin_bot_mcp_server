# 文件上传接口文档

## 概述

企业微信机器人文件上传接口用于上传媒体文件（文件和语音）到企业微信服务器，获取 `media_id` 用于后续消息发送。上传的文件会获得一个唯一的 `media_id`，该 `media_id` 仅在3天内有效，且只能由对应的机器人使用。

## 接口信息

### 接口地址
```
POST https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=KEY&type=TYPE
```

### 请求方式
- **方法**: POST (HTTPS)
- **Content-Type**: multipart/form-data

## 请求参数

### URL 参数

| 参数 | 必须 | 类型 | 说明 |
|------|------|------|------|
| `key` | 是 | string | 调用接口凭证，机器人 webhook URL 中的 key 参数 |
| `type` | 是 | string | 文件类型，支持：`voice`（语音）和 `file`（普通文件） |

### Form-Data 参数

| 参数 | 必须 | 说明 |
|------|------|------|
| `media` | 是 | 媒体文件内容，需要包含 filename、filelength、content-type 等信息 |

### Form-Data 详细说明

POST 请求包中，form-data 中媒体文件标识应包含：

- **filename**: 文件展示的名称，发消息时展示的文件名由该字段控制
- **filelength**: 文件长度（字节数）
- **content-type**: 文件的 MIME 类型

## 请求示例

### 原始 HTTP 请求
```http
POST https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=693a91f6-7xxx-4bc4-97a0-0ec2sifa5aaa&type=file HTTP/1.1
Content-Type: multipart/form-data; boundary=-------------------------acebdf13572468
Content-Length: 220

---------------------------acebdf13572468
Content-Disposition: form-data; name="media";filename="wework.txt"; filelength=6
Content-Type: application/octet-stream

mytext
---------------------------acebdf13572468--
```

### 使用 curl 上传文件
```bash
# 上传普通文件
curl -X POST \
  "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=YOUR_KEY&type=file" \
  -H "Content-Type: multipart/form-data" \
  -F "media=@/path/to/your/file.pdf"

# 上传语音文件
curl -X POST \
  "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=YOUR_KEY&type=voice" \
  -H "Content-Type: multipart/form-data" \
  -F "media=@/path/to/your/audio.amr"
```

### 使用 Python 上传文件
```python
import requests
import os

def upload_media(file_path, media_type, webhook_key):
    """
    上传媒体文件到企业微信
    
    Args:
        file_path: 文件路径
        media_type: 媒体类型 ('file' 或 'voice')
        webhook_key: 机器人webhook密钥
    
    Returns:
        media_id: 上传成功后的媒体ID
    """
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webhook_key}&type={media_type}"
    
    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    with open(file_path, 'rb') as f:
        files = {
            'media': (filename, f, 'application/octet-stream')
        }
        
        response = requests.post(url, files=files, timeout=30)
    
    result = response.json()
    if result.get('errcode') == 0:
        return result['media_id']
    else:
        raise Exception(f"上传失败: {result.get('errmsg', '未知错误')}")

# 使用示例
webhook_key = "YOUR_WEBHOOK_KEY"

# 上传文件
try:
    media_id = upload_media("/path/to/document.pdf", "file", webhook_key)
    print(f"文件上传成功，media_id: {media_id}")
except Exception as e:
    print(f"上传失败: {e}")

# 上传语音
try:
    media_id = upload_media("/path/to/audio.amr", "voice", webhook_key)
    print(f"语音上传成功，media_id: {media_id}")
except Exception as e:
    print(f"上传失败: {e}")
```

## 响应格式

### 成功响应
```json
{
   "errcode": 0,
   "errmsg": "ok",
   "type": "file",
   "media_id": "1G6nrLmr5EC3MMb_-zK1dDdzmd0p7cNliYu9V5w7o8K0",
   "created_at": "1380000000"
}
```

### 响应参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `errcode` | int | 错误码，0表示成功 |
| `errmsg` | string | 错误信息，成功时为"ok" |
| `type` | string | 文件类型，`voice`（语音）或 `file`（普通文件） |
| `media_id` | string | 媒体文件上传后获取的唯一标识，3天内有效 |
| `created_at` | string | 媒体文件上传时间戳 |

### 错误响应
```json
{
   "errcode": 40004,
   "errmsg": "invalid media size"
}
```

## 文件限制条件

### 通用限制
- **最小文件大小**: 所有类型的文件大小均要求**大于5个字节**
- **Media ID 有效期**: 3天
- **使用权限**: media_id 只能由对应上传文件的机器人使用

### 普通文件 (file)
- **最大文件大小**: 20MB
- **支持格式**: 支持各种文件格式（PDF、DOC、XLS、PPT、ZIP、RAR、TXT 等）

### 语音文件 (voice)
- **最大文件大小**: 2MB
- **最大播放时长**: 60秒
- **支持格式**: 仅支持 AMR 格式

## 常见错误码

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 40001 | invalid key | webhook key 无效 | 检查 key 参数是否正确 |
| 40002 | invalid type | 文件类型无效 | 确保 type 参数为 'file' 或 'voice' |
| 40004 | invalid media size | 文件大小无效 | 检查文件大小是否符合限制 |
| 40005 | invalid file type | 不支持的文件类型 | 检查文件格式是否支持 |
| 40006 | invalid file | 文件内容无效 | 检查文件是否损坏 |
| 93000 | invalid file | 文件无效 | 文件可能为空或格式错误 |

## 最佳实践

### 1. 文件检查
```python
def validate_file(file_path, media_type):
    """验证文件是否符合上传要求"""
    if not os.path.exists(file_path):
        raise ValueError(f"文件不存在: {file_path}")
    
    file_size = os.path.getsize(file_path)
    
    # 检查最小文件大小
    if file_size <= 5:
        raise ValueError("文件大小必须大于5个字节")
    
    # 检查文件大小限制
    if media_type == "file" and file_size > 20 * 1024 * 1024:  # 20MB
        raise ValueError("普通文件大小不能超过20MB")
    
    if media_type == "voice" and file_size > 2 * 1024 * 1024:  # 2MB
        raise ValueError("语音文件大小不能超过2MB")
    
    # 检查语音文件格式
    if media_type == "voice" and not file_path.lower().endswith('.amr'):
        raise ValueError("语音文件必须是AMR格式")
    
    return True
```

### 2. 错误处理和重试
```python
import time
import random

def upload_media_with_retry(file_path, media_type, webhook_key, max_retries=3):
    """带重试的文件上传"""
    for attempt in range(max_retries):
        try:
            return upload_media(file_path, media_type, webhook_key)
        except Exception as e:
            if attempt < max_retries - 1:
                # 指数退避重试
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"上传失败，{wait_time:.2f}秒后重试... (尝试 {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise e
```

### 3. Media ID 管理
```python
import json
import time
from datetime import datetime, timedelta

class MediaIdManager:
    """Media ID 管理器"""
    
    def __init__(self, cache_file="media_cache.json"):
        self.cache_file = cache_file
        self.cache = self.load_cache()
    
    def load_cache(self):
        """加载缓存"""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_cache(self):
        """保存缓存"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get_media_id(self, file_path, media_type, webhook_key):
        """获取 media_id，优先从缓存获取"""
        file_key = f"{file_path}_{media_type}"
        
        # 检查缓存
        if file_key in self.cache:
            cached_data = self.cache[file_key]
            created_at = datetime.fromtimestamp(cached_data['created_at'])
            
            # 检查是否过期（3天内有效）
            if datetime.now() - created_at < timedelta(days=3):
                return cached_data['media_id']
            else:
                # 过期，删除缓存
                del self.cache[file_key]
        
        # 上传新文件
        media_id = upload_media(file_path, media_type, webhook_key)
        
        # 缓存结果
        self.cache[file_key] = {
            'media_id': media_id,
            'created_at': time.time()
        }
        self.save_cache()
        
        return media_id
```

### 4. 完整的上传工具函数
```python
def qyweixin_upload_media(file_path, media_type, webhook_key=None):
    """企业微信文件上传工具函数"""
    import os
    import requests
    from config import KEY  # 假设从配置文件导入
    
    # 使用传入的key或配置文件中的key
    key = webhook_key or KEY
    if not key:
        raise ValueError("环境变量 'key' 未设置")
    
    # 验证媒体类型
    if media_type not in ['file', 'voice']:
        raise ValueError(f"不支持的媒体类型: {media_type}")
    
    # 验证文件
    validate_file(file_path, media_type)
    
    # 上传文件
    try:
        media_id = upload_media_with_retry(file_path, media_type, key)
        return media_id
    except Exception as e:
        raise Exception(f"文件上传失败: {str(e)}")
```

## 安全注意事项

1. **Key 保护**: 不要在代码中硬编码 webhook key，使用环境变量或配置文件
2. **文件验证**: 上传前验证文件类型和大小，避免上传恶意文件
3. **错误处理**: 妥善处理上传失败的情况，避免敏感信息泄露
4. **频率控制**: 避免频繁上传大文件，可能会被限流
5. **Media ID 安全**: 不要泄露 media_id，仅在必要时使用

## 相关链接

- [企业微信机器人配置说明](https://developer.work.weixin.qq.com/document/path/91770)
- [文件消息发送接口](./file_message_type.md)
- [语音消息发送接口](./voice_message_type.md) 