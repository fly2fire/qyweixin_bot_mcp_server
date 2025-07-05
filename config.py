import os

# 环境变量配置
KEY = os.environ.get("key")

# API URL 配置
WEBHOOK_URL = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={KEY}"
UPLOAD_URL_TEMPLATE = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type={media_type}"

# 文件大小限制（字节）
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
MAX_VOICE_SIZE = 2 * 1024 * 1024  # 2MB
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB

# 消息长度限制（字节）
MAX_TEXT_LENGTH = 2048
MAX_MARKDOWN_LENGTH = 4096

# 支持的消息类型
MESSAGE_TYPES = [
    "text", "markdown", "markdown_v2", "image", 
    "news", "file", "voice", "template_card"
]

# 支持的媒体类型
MEDIA_TYPES = ["file", "voice"]

# 卡片类型
CARD_TYPES = ["text_notice", "news_notice"]

# HTTP 配置
REQUEST_TIMEOUT = 60
UPLOAD_TIMEOUT = 30 