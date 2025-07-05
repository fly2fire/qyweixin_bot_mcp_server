import os
import requests
from typing import Dict, Any, List
from config import (
    KEY, UPLOAD_URL_TEMPLATE, MAX_FILE_SIZE, MAX_VOICE_SIZE, 
    MESSAGE_TYPES, MEDIA_TYPES, UPLOAD_TIMEOUT
)


def qyweixin_upload_media(file_path: str, media_type: str) -> str:
    """上传媒体文件到企业微信，返回media_id"""
    if not KEY:
        raise ValueError("环境变量 'key' 未设置")
    
    if media_type not in MEDIA_TYPES:
        raise ValueError(f"不支持的媒体类型: {media_type}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    file_size = os.path.getsize(file_path)
    max_size = MAX_VOICE_SIZE if media_type == "voice" else MAX_FILE_SIZE
    
    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        raise ValueError(f"文件大小超出限制: {file_size} 字节 > {max_mb}MB")
    
    upload_url = UPLOAD_URL_TEMPLATE.format(key=KEY, media_type=media_type)
    
    try:
        with open(file_path, 'rb') as f:
            files = {'media': (os.path.basename(file_path), f, 'application/octet-stream')}
            response = requests.post(upload_url, files=files, timeout=UPLOAD_TIMEOUT)
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('errcode') == 0:
            return result['media_id']
        else:
            raise Exception(f"上传失败: {result.get('errmsg', '未知错误')}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败: {str(e)}")


def qyweixin_list_message_types() -> List[Dict[str, Any]]:
    """列出所有支持的消息类型及其说明"""
    return [
        {"type": "text", "name": "文本消息", "description": "发送纯文本消息，支持@用户和@手机号"},
        {"type": "markdown", "name": "Markdown消息", "description": "发送Markdown格式消息，支持基本的Markdown语法"},
        {"type": "markdown_v2", "name": "Markdown增强消息", "description": "发送增强版Markdown消息（注意：实际发送的是普通markdown类型，企业微信不支持独立的markdown_v2类型）"},
        {"type": "image", "name": "图片消息", "description": "发送图片消息，支持URL、本地文件、base64编码"},
        {"type": "news", "name": "图文消息", "description": "发送图文消息，支持多篇文章"},
        {"type": "file", "name": "文件消息", "description": "发送文件消息，支持本地文件上传"},
        {"type": "voice", "name": "语音消息", "description": "发送语音消息，支持AMR格式"},
        {"type": "template_card", "name": "模板卡片", "description": "发送模板卡片消息，支持文本通知和图文展示"}
    ]


def qyweixin_get_message_format(message_type: str) -> Dict[str, Any]:
    """获取指定消息类型的格式要求和参数说明"""
    if message_type not in MESSAGE_TYPES:
        raise ValueError(f"不支持的消息类型: {message_type}")
    
    # 基础格式信息
    format_info = {
        "type": message_type,
        "webhook_url": f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={{YOUR_KEY}}",
        "http_method": "POST",
        "content_type": "application/json"
    }
    
    # 根据消息类型设置详细JSON格式
    if message_type == "text":
        format_info.update({
            "name": "文本消息",
            "description": "纯文本消息，支持@用户、换行、超链接",
            "json_format": {
                "msgtype": "text",
                "text": {
                    "content": "消息内容，支持换行\\n和@用户",
                    "mentioned_list": ["@all"] or ["userid1", "userid2"],  # 可选
                    "mentioned_mobile_list": ["13800001111", "13800002222"]  # 可选
                }
            },
            "required_fields": ["msgtype", "text.content"],
            "optional_fields": ["text.mentioned_list", "text.mentioned_mobile_list"],
            "limitations": {
                "max_length": "2048字节",
                "features": ["支持换行符", "支持@用户功能", "支持超链接"]
            }
        })
    
    elif message_type == "markdown":
        format_info.update({
            "name": "Markdown消息",
            "description": "支持基础markdown语法的格式化消息",
            "json_format": {
                "msgtype": "markdown",
                "markdown": {
                    "content": "# 标题\\n**加粗**\\n*斜体*\\n[链接](http://example.com)\\n- 列表项\\n> 引用\\n```代码```"
                }
            },
            "required_fields": ["msgtype", "markdown.content"],
            "optional_fields": [],
            "limitations": {
                "max_length": "4096字节",
                "supported_syntax": ["标题", "加粗", "斜体", "链接", "列表", "引用", "代码", "有限字体颜色"],
                "color_support": ["info", "comment", "warning"]
            }
        })
    
    elif message_type == "markdown_v2":
        format_info.update({
            "name": "Markdown增强消息",
            "description": "支持表格、图片、代码块等增强功能的markdown消息",
            "json_format": {
                "msgtype": "markdown",
                "markdown": {
                    "content": "# 标题\\n**加粗**\\n![图片](http://example.com/image.jpg)\\n| 列1 | 列2 |\\n|-----|-----|\\n| 值1 | 值2 |\\n```python\\nprint('code')\\n```\\n---\\n分割线"
                }
            },
            "required_fields": ["msgtype", "markdown.content"],
            "optional_fields": [],
            "limitations": {
                "max_length": "4096字节",
                "supported_syntax": ["标题", "字体样式", "列表", "引用", "链接", "图片", "分割线", "代码块", "表格"],
                "not_supported": ["字体颜色", "@功能", "HTML标签"],
                "image_control": "无法控制图片显示大小"
            }
        })
    
    elif message_type == "image":
        format_info.update({
            "name": "图片消息",
            "description": "支持URL、本地文件、base64编码的图片消息",
            "json_format": {
                "msgtype": "image",
                "image": {
                    "base64": "图片base64编码",
                    "md5": "图片md5值"
                }
            },
            "required_fields": ["msgtype", "image.base64", "image.md5"],
            "optional_fields": [],
            "limitations": {
                "max_size": "2MB",
                "supported_formats": ["JPG", "PNG", "GIF", "BMP", "WEBP"],
                "size_control": "无法控制显示大小",
                "encoding": "需要base64编码和md5校验"
            }
        })
    
    elif message_type == "news":
        format_info.update({
            "name": "图文消息",
            "description": "支持多篇图文，可跳转链接的图文消息",
            "json_format": {
                "msgtype": "news",
                "news": {
                    "articles": [
                        {
                            "title": "标题，必需字段",
                            "description": "描述，可选字段",
                            "url": "跳转链接，必需字段",
                            "picurl": "图片链接，可选字段"
                        }
                    ]
                }
            },
            "required_fields": ["msgtype", "news.articles", "articles[].title", "articles[].url"],
            "optional_fields": ["articles[].description", "articles[].picurl"],
            "limitations": {
                "max_articles": "8篇文章",
                "title_length": "建议不超过64字节",
                "description_length": "建议不超过512字节",
                "image_size": "大图建议1068×455，小图建议150×150"
            }
        })
    
    elif message_type == "file":
        format_info.update({
            "name": "文件消息",
            "description": "支持自动上传文件获取media_id的文件消息",
            "json_format": {
                "msgtype": "file",
                "file": {
                    "media_id": "通过上传接口获取的media_id"
                }
            },
            "required_fields": ["msgtype", "file.media_id"],
            "optional_fields": [],
            "upload_api": {
                "url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file",
                "method": "POST",
                "form_data": "multipart/form-data"
            },
            "limitations": {
                "max_size": "20MB",
                "media_id_ttl": "3天",
                "supported_formats": "各种文件格式"
            }
        })
    
    elif message_type == "voice":
        format_info.update({
            "name": "语音消息",
            "description": "支持AMR格式的语音文件消息",
            "json_format": {
                "msgtype": "voice",
                "voice": {
                    "media_id": "通过上传接口获取的media_id"
                }
            },
            "required_fields": ["msgtype", "voice.media_id"],
            "optional_fields": [],
            "upload_api": {
                "url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=voice",
                "method": "POST",
                "form_data": "multipart/form-data"
            },
            "limitations": {
                "max_size": "2MB",
                "supported_format": "AMR",
                "media_id_ttl": "3天",
                "duration": "建议不超过60秒"
            }
        })
    
    elif message_type == "template_card":
        format_info.update({
            "name": "模板卡片消息",
            "description": "支持文本通知卡片和图文展示卡片的模板消息",
            "json_format": {
                "msgtype": "template_card",
                "template_card": {
                    "card_type": "text_notice 或 news_notice",
                    "source": {
                        "icon_url": "图标链接，可选",
                        "desc": "来源描述，可选",
                        "desc_color": "描述颜色，可选"
                    },
                    "action_menu": {
                        "desc": "菜单描述，可选",
                        "action_list": [
                            {
                                "text": "菜单项文本",
                                "type": "菜单项类型"
                            }
                        ]
                    },
                    "task_id": "任务ID，可选",
                    "main_title": {
                        "title": "主标题，可选",
                        "desc": "主标题描述，可选"
                    },
                    "emphasis_content": {
                        "title": "强调内容标题，可选",
                        "desc": "强调内容描述，可选"
                    },
                    "sub_title_text": "副标题文本，可选",
                    "horizontal_content_list": [
                        {
                            "keyname": "属性名",
                            "value": "属性值"
                        }
                    ],
                    "jump_list": [
                        {
                            "type": "跳转类型",
                            "title": "跳转标题",
                            "url": "跳转链接"
                        }
                    ],
                    "card_action": {
                        "type": "卡片动作类型",
                        "url": "动作链接"
                    }
                }
            },
            "card_types": {
                "text_notice": "文本通知卡片",
                "news_notice": "图文展示卡片（需要card_image_url）"
            },
            "required_fields": ["msgtype", "template_card.card_type"],
            "optional_fields": [
                "template_card.source", "template_card.action_menu", "template_card.task_id",
                "template_card.main_title", "template_card.emphasis_content", "template_card.sub_title_text",
                "template_card.horizontal_content_list", "template_card.jump_list", "template_card.card_action"
            ],
            "limitations": {
                "title_length": "建议不超过36字节",
                "aspect_ratio": "图片宽高比范围1.3-2.25",
                "card_types": "支持text_notice和news_notice两种类型"
            }
        })
    
    return format_info
