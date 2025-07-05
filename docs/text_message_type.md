# 文本消息类型文档

## 概述

文本消息类型是企业微信机器人最基础和常用的消息类型，用于发送纯文本内容。支持 @用户功能，可以提醒群中的指定成员或所有成员。

## 消息格式

### JSON 结构

```json
{
    "msgtype": "text",
    "text": {
        "content": "广州今日天气：29度，大部分多云，降雨概率：60%",
        "mentioned_list": ["wangqing", "@all"],
        "mentioned_mobile_list": ["13800001111", "@all"]
    }
}
```

### 参数说明

| 参数 | 是否必填 | 类型 | 说明 |
|------|----------|------|------|
| `msgtype` | 是 | string | 消息类型，此时固定为 `text` |
| `text` | 是 | object | 文本对象 |
| `text.content` | 是 | string | 文本内容，最长不超过2048个字节，必须是utf8编码 |
| `text.mentioned_list` | 否 | array | userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人 |
| `text.mentioned_mobile_list` | 否 | array | 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人 |

## 使用示例

### 1. 基础文本消息

```json
{
    "msgtype": "text",
    "text": {
        "content": "🌤️ 今日天气报告：\n\n📍 广州\n🌡️ 温度：29°C\n☁️ 天气：大部分多云\n🌧️ 降雨概率：60%\n\n请大家出门记得带伞哦！"
    }
}
```

### 2. @指定用户的消息

```json
{
    "msgtype": "text",
    "text": {
        "content": "@wangqing 你好，请查看今日的工作安排",
        "mentioned_list": ["wangqing"]
    }
}
```

### 3. @所有人的消息

```json
{
    "msgtype": "text",
    "text": {
        "content": "@all 紧急通知：今日下午3点开会，请准时参加！",
        "mentioned_list": ["@all"]
    }
}
```

### 4. 使用手机号@用户

```json
{
    "msgtype": "text",
    "text": {
        "content": "会议提醒：@13800001111 请准备会议材料",
        "mentioned_mobile_list": ["13800001111"]
    }
}
```

### 5. 同时@多个用户

```json
{
    "msgtype": "text",
    "text": {
        "content": "项目进度更新：@张三 @李四 请提供最新进展",
        "mentioned_list": ["zhangsan", "lisi"],
        "mentioned_mobile_list": ["13800001111", "13800002222"]
    }
}
```

## 编程示例

### Python 发送文本消息

```python
import requests
import json

def send_text_message(content, webhook_key, mentioned_list=None, mentioned_mobile_list=None):
    """
    发送文本消息到企业微信群
    
    Args:
        content: 消息内容
        webhook_key: 机器人webhook密钥
        mentioned_list: 要@的用户ID列表
        mentioned_mobile_list: 要@的手机号列表
    
    Returns:
        dict: 发送结果
    """
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    
    # 添加@用户列表
    if mentioned_list:
        data["text"]["mentioned_list"] = mentioned_list
    
    if mentioned_mobile_list:
        data["text"]["mentioned_mobile_list"] = mentioned_mobile_list
    
    try:
        response = requests.post(url, json=data, timeout=30)
        result = response.json()
        
        if result.get('errcode') == 0:
            return {"success": True, "data": result}
        else:
            return {"success": False, "error": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# 使用示例
webhook_key = "YOUR_WEBHOOK_KEY"

# 发送普通文本消息
result = send_text_message("今日天气不错，适合出行！", webhook_key)
print(result)

# 发送@所有人的消息
result = send_text_message(
    "⚠️ 系统维护通知：今晚10点-12点进行系统维护，请提前保存工作！",
    webhook_key,
    mentioned_list=["@all"]
)
print(result)

# 发送@指定用户的消息
result = send_text_message(
    "会议提醒：明天上午10点开会，请准时参加",
    webhook_key,
    mentioned_list=["zhangsan", "lisi"],
    mentioned_mobile_list=["13800001111"]
)
print(result)
```

### 使用 MCP 服务器工具

```python
# 使用 qyweixin_text 工具函数
result = qyweixin_text(
    content="今日工作提醒：请大家按时提交周报",
    mentioned_list=["@all"]
)
```

## 限制条件

### 内容限制
- **最大长度**: 2048个字节（UTF-8编码）
- **字符编码**: 必须是UTF-8编码
- **换行符**: 支持 `\n` 换行符
- **特殊字符**: 支持 emoji 表情符号

### @功能限制
- **mentioned_list**: 支持 userid 和 "@all"
- **mentioned_mobile_list**: 支持手机号和 "@all"
- **@all**: 提醒群内所有成员
- **优先级**: 如果获取不到 userid，可以使用 mentioned_mobile_list

## 最佳实践

### 1. 内容格式化

```python
def format_weather_message(city, temperature, weather, rain_probability):
    """格式化天气消息"""
    return f"""🌤️ {city}天气报告

🌡️ 温度：{temperature}°C
☁️ 天气：{weather}
🌧️ 降雨概率：{rain_probability}%

{'☔ 建议带伞' if rain_probability > 50 else '☀️ 天气不错'}"""

# 使用
content = format_weather_message("广州", 29, "大部分多云", 60)
```

### 2. @用户管理

```python
class MentionManager:
    """@用户管理器"""
    
    def __init__(self):
        self.user_mapping = {
            "张三": "zhangsan",
            "李四": "lisi",
            "王五": "wangwu"
        }
    
    def get_userid_by_name(self, name):
        """根据姓名获取userid"""
        return self.user_mapping.get(name)
    
    def mention_users(self, content, users):
        """在消息中@指定用户"""
        mentioned_list = []
        
        for user in users:
            if user == "所有人":
                mentioned_list.append("@all")
                content += " @all"
            else:
                userid = self.get_userid_by_name(user)
                if userid:
                    mentioned_list.append(userid)
                    content += f" @{user}"
        
        return content, mentioned_list

# 使用示例
manager = MentionManager()
content, mentioned_list = manager.mention_users(
    "会议提醒：明天上午10点开会",
    ["张三", "李四"]
)
```

### 3. 消息模板

```python
class MessageTemplate:
    """消息模板类"""
    
    @staticmethod
    def notice(title, content, urgent=False):
        """通知消息模板"""
        prefix = "🚨 紧急通知" if urgent else "📢 通知"
        return f"{prefix}：{title}\n\n{content}"
    
    @staticmethod
    def reminder(event, time, participants=None):
        """提醒消息模板"""
        msg = f"⏰ 提醒：{event}\n📅 时间：{time}"
        if participants:
            msg += f"\n👥 参与人员：{', '.join(participants)}"
        return msg
    
    @staticmethod
    def report(title, data):
        """报告消息模板"""
        msg = f"📊 {title}\n\n"
        for key, value in data.items():
            msg += f"• {key}：{value}\n"
        return msg

# 使用示例
template = MessageTemplate()

# 紧急通知
urgent_notice = template.notice(
    "系统维护", 
    "今晚10点-12点进行系统维护，请提前保存工作！", 
    urgent=True
)

# 会议提醒
meeting_reminder = template.reminder(
    "周例会", 
    "明天上午10:00", 
    ["张三", "李四", "王五"]
)

# 数据报告
daily_report = template.report("今日数据统计", {
    "访问量": "1,234",
    "新增用户": "56",
    "转化率": "3.2%"
})
```

### 4. 字节长度检查

```python
def check_content_length(content, max_bytes=2048):
    """检查内容字节长度"""
    content_bytes = content.encode('utf-8')
    if len(content_bytes) > max_bytes:
        raise ValueError(f"内容过长：{len(content_bytes)} 字节 > {max_bytes} 字节")
    return True

def truncate_content(content, max_bytes=2048):
    """截断内容到指定字节长度"""
    content_bytes = content.encode('utf-8')
    if len(content_bytes) <= max_bytes:
        return content
    
    # 截断到最大字节数
    truncated = content_bytes[:max_bytes-3]  # 预留3字节给"..."
    
    # 确保不在UTF-8字符中间截断
    while len(truncated) > 0:
        try:
            decoded = truncated.decode('utf-8')
            return decoded + "..."
        except UnicodeDecodeError:
            truncated = truncated[:-1]
    
    return ""

# 使用示例
try:
    check_content_length(content)
    send_text_message(content, webhook_key)
except ValueError as e:
    print(f"内容过长，自动截断: {e}")
    truncated_content = truncate_content(content)
    send_text_message(truncated_content, webhook_key)
```

## 常见错误码

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 40001 | invalid key | webhook key 无效 | 检查 key 参数是否正确 |
| 40013 | invalid appid | 应用ID无效 | 检查机器人配置 |
| 93000 | invalid json | JSON格式错误 | 检查JSON格式是否正确 |
| 93001 | text content too long | 文本内容过长 | 确保内容不超过2048字节 |
| 93004 | invalid mentioned_list | @用户列表无效 | 检查用户ID是否正确 |

## 注意事项

1. **字符编码**: 所有文本内容必须是UTF-8编码
2. **内容长度**: 最大2048字节，中文字符占3字节
3. **@功能**: userid优先级高于手机号
4. **换行符**: 使用 `\n` 进行换行
5. **特殊字符**: 支持emoji表情，但注意字节长度计算
6. **@all限制**: 避免频繁使用@all，可能会被群成员屏蔽

## 内容格式建议

### 1. 使用 Emoji 增强可读性
```
✅ 任务完成
❌ 任务失败
⚠️ 重要提醒
📅 时间安排
👥 人员信息
📊 数据统计
```

### 2. 合理使用换行和分段
```
📢 会议通知

📅 时间：2024年1月15日 10:00
📍 地点：会议室A
👥 参与人员：@张三 @李四

📝 议程：
1. 项目进展汇报
2. 下周工作安排
3. 其他事项

请准时参加！
```

### 3. 结构化信息展示
```
📊 每日数据报告

• 访问量：1,234 (+5.2%)
• 新增用户：56 (+12.3%)
• 转化率：3.2% (-0.8%)
• 收入：¥12,345 (+8.9%)

🔍 详细分析：
- 移动端访问增长显著
- 新用户主要来自推广渠道
- 转化率略有下降，需要优化
```

## 相关链接

- [企业微信机器人配置说明](https://developer.work.weixin.qq.com/document/path/91770)
- [群机器人配置说明](https://developer.work.weixin.qq.com/document/path/91770#%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F)
- [UTF-8编码说明](https://zh.wikipedia.org/wiki/UTF-8) 