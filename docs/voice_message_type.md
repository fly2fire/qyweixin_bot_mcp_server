# 语音消息类型文档

## 概述

语音消息类型用于向企业微信群发送语音文件，支持 AMR 格式的音频文件。发送语音消息需要先通过文件上传接口获取 `media_id`，然后使用该 `media_id` 发送消息。

## 消息格式

### JSON 结构

```json
{
    "msgtype": "voice",
    "voice": {
        "media_id": "MEDIA_ID"
    }
}
```

### 参数说明

| 参数 | 是否必填 | 类型 | 说明 |
|------|----------|------|------|
| `msgtype` | 是 | string | 消息类型，此时固定为 `voice` |
| `voice` | 是 | object | 语音对象 |
| `voice.media_id` | 是 | string | 语音文件id，通过文件上传接口获取 |

## 语音文件上传接口

### 接口地址

```
POST https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=voice
```

### 请求方式

- **方法**: POST
- **Content-Type**: multipart/form-data

### 请求参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| `key` | 是 | 企业微信机器人的 webhook 密钥 |
| `type` | 是 | 媒体文件类型，固定为 `voice` |
| `media` | 是 | 语音文件内容，form-data 格式 |

### 响应格式

**成功响应：**
```json
{
    "errcode": 0,
    "errmsg": "ok",
    "type": "voice",
    "media_id": "MEDIA_ID",
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

### 语音文件限制
- **最大文件大小**: 2MB
- **音频格式**: 仅支持 AMR 格式
- **推荐时长**: 不超过 60 秒
- **采样率**: 8kHz
- **比特率**: 12.2kbps

### Media ID 限制
- **有效期**: 3天
- **使用次数**: 不限制

## 使用示例

### 1. 使用 curl 上传语音文件

```bash
curl -X POST \
  "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=YOUR_KEY&type=voice" \
  -H "Content-Type: multipart/form-data" \
  -F "media=@/path/to/your/audio.amr"
```

### 2. 使用 Python 上传语音文件

```python
import requests

def upload_voice(file_path, webhook_key):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webhook_key}&type=voice"
    
    with open(file_path, 'rb') as f:
        files = {'media': (file_path, f, 'audio/amr')}
        response = requests.post(url, files=files)
    
    result = response.json()
    if result.get('errcode') == 0:
        return result['media_id']
    else:
        raise Exception(f"上传失败: {result.get('errmsg')}")
```

### 3. 发送语音消息

```python
import requests
import json

def send_voice_message(media_id, webhook_key):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    
    data = {
        "msgtype": "voice",
        "voice": {
            "media_id": media_id
        }
    }
    
    response = requests.post(url, json=data)
    return response.json()

# 完整流程
webhook_key = "YOUR_WEBHOOK_KEY"
voice_file_path = "/path/to/audio.amr"

# 1. 上传语音文件获取 media_id
media_id = upload_voice(voice_file_path, webhook_key)

# 2. 发送语音消息
result = send_voice_message(media_id, webhook_key)
print(result)
```

### 4. 使用 MCP 服务器工具

```python
# 使用 qyweixin_voice 工具函数
result = qyweixin_voice(file_path="/path/to/audio.amr")
```

### 5. 音频格式转换

如果你有其他格式的音频文件，需要先转换为 AMR 格式：

```python
# 使用 ffmpeg 转换音频格式
import subprocess

def convert_to_amr(input_file, output_file):
    """将音频文件转换为 AMR 格式"""
    cmd = [
        'ffmpeg', '-i', input_file,
        '-ar', '8000',  # 采样率 8kHz
        '-ab', '12.2k', # 比特率 12.2kbps
        '-ac', '1',     # 单声道
        output_file
    ]
    subprocess.run(cmd, check=True)

# 示例使用
convert_to_amr("input.mp3", "output.amr")
```

## 常见错误码

| 错误码 | 错误信息 | 说明 |
|--------|----------|------|
| 40001 | invalid key | webhook key 无效 |
| 40003 | invalid media_id | media_id 无效或已过期 |
| 40004 | invalid media size | 文件大小超出限制（>2MB） |
| 40005 | invalid file type | 不支持的文件格式（非AMR格式） |
| 93000 | invalid file | 文件内容无效或损坏 |

## 最佳实践

### 1. 音频质量控制
- 使用 8kHz 采样率，12.2kbps 比特率
- 控制语音时长在 60 秒以内
- 确保语音清晰度，避免噪音

### 2. 格式转换
- 使用 ffmpeg 等工具转换音频格式
- 转换时保持适当的音质参数
- 检查转换后的文件大小

### 3. 错误处理
- 上传前检查文件格式和大小
- 处理网络异常和 API 错误
- 实现重试机制

### 4. 性能优化
- 压缩音频文件减少上传时间
- 缓存 media_id 避免重复上传
- 异步处理音频上传

## 注意事项

1. **音频格式限制**: 仅支持 AMR 格式，其他格式需要转换
2. **文件大小限制**: 单个语音文件不能超过 2MB
3. **时长建议**: 语音时长建议控制在 60 秒以内
4. **Media ID 有效期**: 上传后的 media_id 有效期为3天
5. **播放兼容性**: 确保 AMR 文件在各种设备上都能正常播放
6. **隐私保护**: 注意语音内容的隐私性，避免敏感信息泄露

## 音频格式转换工具

### 使用 ffmpeg 转换

```bash
# 将 MP3 转换为 AMR
ffmpeg -i input.mp3 -ar 8000 -ab 12.2k -ac 1 output.amr

# 将 WAV 转换为 AMR
ffmpeg -i input.wav -ar 8000 -ab 12.2k -ac 1 output.amr

# 将 M4A 转换为 AMR
ffmpeg -i input.m4a -ar 8000 -ab 12.2k -ac 1 output.amr
```

### 在线转换工具

- [CloudConvert](https://cloudconvert.com/)
- [Online Audio Converter](https://online-audio-converter.com/)
- [Convertio](https://convertio.co/)

## 相关链接

- [企业微信机器人配置说明](https://developer.work.weixin.qq.com/document/path/91770)
- [群机器人配置说明](https://developer.work.weixin.qq.com/document/path/91770#%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F)
- [AMR 音频格式说明](https://en.wikipedia.org/wiki/Adaptive_Multi-Rate_audio_codec) 