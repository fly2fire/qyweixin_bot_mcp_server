from fastmcp import FastMCP, Context
import json
import os
import requests
import logging
from pydantic import Field
from typing import Annotated, Optional, List, Dict, Any
import base64
import hashlib
from urllib.parse import urlparse

logger = logging.getLogger("mcp")

mcp = FastMCP("qyweixin bot MCP Server", log_level='ERROR')

key = os.environ.get("key")
webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"


@mcp.tool(name="qyweixin_notice", description="Enterprise WeChat robot notification, send messages to group chats through the enterprise WeChat robot.")
def qyweixin_notice(
    msg: Annotated[str, Field(description="Message content text. For image type, this can be an image URL address or the local full path of the image. For file/voice type, this can be a file path (will auto-upload) or media_id. For template_card type, this will be used as main_title if main_title is not provided")],
    msgtype: Annotated[str, Field(description="Message type, options: text, markdown, markdown_v2, image, file, voice, news, template_card, default is text. For image type, msg can be URL or local file path. For file/voice type, msg can be file path or media_id")] = "text",
    mentioned_list: Annotated[Optional[List[str]], Field(description="Notify specific members in group (@someone), @all means notify everyone, only valid for text messages")] = None,
    mentioned_mobile_list: Annotated[Optional[List[str]], Field(description="Notify specific members in group by mobile number (@someone), @all means notify everyone, only valid for text messages")] = None,
    # News message parameters
    title: Annotated[Optional[str], Field(description="Article title, required for news type")] = None,
    description: Annotated[Optional[str], Field(description="Article description, optional for news type")] = None,
    url: Annotated[Optional[str], Field(description="Article URL, required for news type")] = None,
    picurl: Annotated[Optional[str], Field(description="Article picture URL, optional for news type")] = None,
    # Template card parameters
    card_type: Annotated[Optional[str], Field(description="Template card type: text_notice, news_notice, required for template_card type")] = None,
    main_title: Annotated[Optional[str], Field(description="Main title for template card, required for template_card type")] = None,
    main_title_desc: Annotated[Optional[str], Field(description="Main title description for template card, optional")] = None,
    source_desc: Annotated[Optional[str], Field(description="Card source description, optional for template_card type")] = None,
    source_icon_url: Annotated[Optional[str], Field(description="Card source icon URL, optional for template_card type")] = None,
    card_action_type: Annotated[Optional[int], Field(description="Card action type: 1=jump to URL, 2=jump to mini program, required for template_card type")] = None,
    card_action_url: Annotated[Optional[str], Field(description="Card action URL, required when card_action_type=1")] = None,
    # For news_notice type
    card_image_url: Annotated[Optional[str], Field(description="Card image URL, required for news_notice type")] = None,
    card_image_aspect_ratio: Annotated[Optional[float], Field(description="Card image aspect ratio, optional for news_notice type")] = None,
    # For text_notice type
    sub_title_text: Annotated[Optional[str], Field(description="Sub title text, optional for text_notice type")] = None,
    emphasis_title: Annotated[Optional[str], Field(description="Emphasis content title, optional for text_notice type")] = None,
    emphasis_desc: Annotated[Optional[str], Field(description="Emphasis content description, optional for text_notice type")] = None,
    ctx: Context = None):
    """
    Enterprise WeChat robot notification, send messages to group chats through the enterprise WeChat robot.

    Args:
        msg (str): Message content text. For image type, this can be an image URL address or the local full path of the image. For file type, this should be the file path. For voice type, this should be the file path.
        msgtype (str): Message type, options: text, markdown, markdown_v2, image, file, voice, news, template_card, default is text. When the message type is an image, it can be an image URL address or the local full path of the image. When the message type is file or voice, msg should be the file path
        mentioned_list (List[str], optional): Notify specific members in group (@someone), @all means notify everyone, only valid for text messages
        mentioned_mobile_list (List[str], optional): Notify specific members in group by mobile number (@someone), @all means notify everyone, only valid for text messages
        title (str, optional): Article title, required for news type
        description (str, optional): Article description, optional for news type
        url (str, optional): Article URL, required for news type
        picurl (str, optional): Article picture URL, optional for news type
        card_type (str, optional): Template card type: text_notice, news_notice, required for template_card type
        main_title (str, optional): Main title for template card, required for template_card type
        main_title_desc (str, optional): Main title description for template card, optional
        source_desc (str, optional): Card source description, optional for template_card type
        source_icon_url (str, optional): Card source icon URL, optional for template_card type
        card_action_type (int, optional): Card action type: 1=jump to URL, 2=jump to mini program, required for template_card type
        card_action_url (str, optional): Card action URL, required when card_action_type=1
        card_image_url (str, optional): Card image URL, required for news_notice type
        card_image_aspect_ratio (float, optional): Card image aspect ratio, optional for news_notice type
        sub_title_text (str, optional): Sub title text, optional for text_notice type
        emphasis_title (str, optional): Emphasis content title, optional for text_notice type
        emphasis_desc (str, optional): Emphasis content description, optional for text_notice type
        ctx (Context): Context
    
    Returns:
        Dict[str, Any]: Return result
    """

    payload = {"msgtype": msgtype}
    
    if msgtype == "text":
        payload["text"] = {
            "content": msg
        }
        if mentioned_list:
            payload["text"]["mentioned_list"] = mentioned_list
        if mentioned_mobile_list:
            payload["text"]["mentioned_mobile_list"] = mentioned_mobile_list
    
    elif msgtype == "markdown":
        payload["markdown"] = {
            "content": msg
        }
    
    elif msgtype == "markdown_v2":
        payload["markdown_v2"] = {
            "content": msg
        }
    
    elif msgtype == "image":
        try:
            # 处理URL图片
            if urlparse(msg).scheme in ('http', 'https'):
                response = requests.get(msg, timeout=10)
                response.raise_for_status()
                image_data = response.content
            # 处理本地图片
            else:
                if not os.path.exists(msg):
                    return {"errcode": -1, "errmsg": f"Image file not found: {msg}"}
                with open(msg, "rb") as f:
                    image_data = f.read()
            
            # 统一处理图片数据
            base64_content = base64.b64encode(image_data).decode('utf-8')
            md5_content = hashlib.md5(image_data).hexdigest()
            
            payload["image"] = {
                "base64": base64_content,
                "md5": md5_content
            }
        except requests.exceptions.RequestException as e:
            return {"errcode": -1, "errmsg": f"Failed to download image from URL: {str(e)}"}
        except Exception as e:
            return {"errcode": -1, "errmsg": f"Image processing failed: {str(e)}"}
    
    elif msgtype == "file":
        try:
            # 检查msg是否为文件路径，如果是则上传文件获取media_id
            if os.path.exists(msg):
                # 上传文件获取media_id
                upload_result = qyweixin_upload_media(msg, "file")
                if upload_result.get("errcode") != 0:
                    return upload_result
                media_id = upload_result.get("media_id")
                if not media_id:
                    return {"errcode": -1, "errmsg": "Failed to get media_id from upload response"}
            else:
                # 假设msg已经是media_id
                media_id = msg
            
            payload["file"] = {
                "media_id": media_id
            }
        except Exception as e:
            return {"errcode": -1, "errmsg": f"File processing failed: {str(e)}"}
    
    elif msgtype == "voice":
        try:
            # 检查msg是否为文件路径，如果是则上传文件获取media_id
            if os.path.exists(msg):
                # 上传文件获取media_id
                upload_result = qyweixin_upload_media(msg, "voice")
                if upload_result.get("errcode") != 0:
                    return upload_result
                media_id = upload_result.get("media_id")
                if not media_id:
                    return {"errcode": -1, "errmsg": "Failed to get media_id from upload response"}
            else:
                # 假设msg已经是media_id
                media_id = msg
            
            payload["voice"] = {
                "media_id": media_id
            }
        except Exception as e:
            return {"errcode": -1, "errmsg": f"Voice processing failed: {str(e)}"}
    
    elif msgtype == "news":
        if not title or not url:
            return {"errcode": -1, "errmsg": "News type requires both title and url parameters"}
        
        payload["news"] = {
            "articles": [
                {
                    "title": title,
                    "description": description or "",
                    "url": url,
                    "picurl": picurl or ""
                }
            ]
        }
    
    elif msgtype == "template_card":
        if not card_type:
            return {"errcode": -1, "errmsg": "Template card type requires card_type parameter (text_notice or news_notice)"}
        
        # 使用main_title或msg作为主标题
        title_text = main_title if main_title else msg
        if not title_text:
            return {"errcode": -1, "errmsg": "Template card requires main_title parameter or msg content"}
        
        if not card_action_type:
            return {"errcode": -1, "errmsg": "Template card requires card_action_type parameter (1=URL, 2=mini program)"}
        
        # 构建基础结构
        template_card = {
            "card_type": card_type,
            "main_title": {
                "title": title_text
            }
        }
        
        # 添加主标题描述
        if main_title_desc:
            template_card["main_title"]["desc"] = main_title_desc
        
        # 添加来源信息
        if source_desc or source_icon_url:
            template_card["source"] = {}
            if source_desc:
                template_card["source"]["desc"] = source_desc
            if source_icon_url:
                template_card["source"]["icon_url"] = source_icon_url
        
        # 添加卡片动作（必需）
        template_card["card_action"] = {
            "type": card_action_type
        }
        if card_action_url:
            template_card["card_action"]["url"] = card_action_url
        
        # 根据不同类型添加特定字段
        if card_type == "text_notice":
            # 文本通知型特有字段
            if sub_title_text:
                template_card["sub_title_text"] = sub_title_text
            
            if emphasis_title or emphasis_desc:
                template_card["emphasis_content"] = {}
                if emphasis_title:
                    template_card["emphasis_content"]["title"] = emphasis_title
                if emphasis_desc:
                    template_card["emphasis_content"]["desc"] = emphasis_desc
        
        elif card_type == "news_notice":
            # 图文展示型特有字段
            if not card_image_url:
                return {"errcode": -1, "errmsg": "news_notice type requires card_image_url parameter"}
            
            template_card["card_image"] = {
                "url": card_image_url
            }
            if card_image_aspect_ratio:
                template_card["card_image"]["aspect_ratio"] = card_image_aspect_ratio
        
        else:
            return {"errcode": -1, "errmsg": f"Invalid card_type: {card_type}. Must be 'text_notice' or 'news_notice'"}
        
        payload["template_card"] = template_card
    
    else:
        return {"errcode": -1, "errmsg": f"Unsupported message type: {msgtype}. Supported types: text, markdown, markdown_v2, image, file, voice, news, template_card"}
    
    # 发送消息
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json; charset=utf-8'},
            # headers={'Content-Type': 'application/json'},
            timeout=60
        )
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        return {"errcode": -1, "errmsg": f"Failed to send message: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"errcode": -1, "errmsg": f"Invalid response from server: {str(e)}"}

@mcp.tool(name="qyweixin_upload_media", description="Upload file or voice to Enterprise WeChat robot and get media_id.")
def qyweixin_upload_media(
    file_path: Annotated[str, Field(description="Local file path to upload")],
    media_type: Annotated[str, Field(description="Media type: file or voice")] = "file",
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Upload file or voice to Enterprise WeChat robot and get media_id.
    
    Args:
        file_path (str): Local file path to upload
        media_type (str): Media type: file or voice, default is file
        ctx (Context): Context
    
    Returns:
        dict: Response containing media_id if successful
    """
    try:
        if not key:
            return {"errcode": -1, "errmsg": "Environment variable 'key' is not set"}
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return {"errcode": -1, "errmsg": f"File not found: {file_path}"}
        
        # 检查媒体类型
        if media_type not in ["file", "voice"]:
            return {"errcode": -1, "errmsg": f"Invalid media type: {media_type}. Must be 'file' or 'voice'"}
        
        # 检查文件大小限制
        file_size = os.path.getsize(file_path)
        if media_type == "file" and file_size > 20 * 1024 * 1024:  # 20MB for files
            return {"errcode": -1, "errmsg": f"File too large: {file_size} bytes, maximum allowed: 20MB"}
        elif media_type == "voice" and file_size > 2 * 1024 * 1024:  # 2MB for voice
            return {"errcode": -1, "errmsg": f"Voice file too large: {file_size} bytes, maximum allowed: 2MB"}
        
        # 构建上传URL
        upload_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type={media_type}"
        
        # 准备文件上传
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            files = {
                'media': (filename, f, 'application/octet-stream')
            }
            
            # 发送上传请求
            response = requests.post(upload_url, files=files, timeout=30)
            
        # 处理响应
        if response.status_code == 200:
            result = response.json()
            logger.info(f"File upload response: {result}")
            return result
        else:
            return {"errcode": -1, "errmsg": f"HTTP error: {response.status_code}, {response.text}"}
            
    except requests.exceptions.Timeout:
        return {"errcode": -1, "errmsg": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"errcode": -1, "errmsg": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"errcode": -1, "errmsg": f"Unexpected error: {str(e)}"}

@mcp.tool(name="qyweixin_list_message_types", description="List all supported message types for Enterprise WeChat robot.")
def qyweixin_list_message_types(ctx: Context = None) -> Dict[str, Any]:
    """
    List all supported message types for Enterprise WeChat robot.
    
    Returns:
        dict: List of supported message types with brief descriptions
    """
    message_types = [
        {
            "type": "text",
            "name": "文本消息",
            "description": "支持 @用户、换行、超链接的纯文本消息"
        },
        {
            "type": "markdown",
            "name": "Markdown 消息",
            "description": "支持基础 Markdown 语法的格式化消息"
        },
        {
            "type": "markdown_v2",
            "name": "增强 Markdown 消息",
            "description": "支持表格、代码块、图片等增强功能的 Markdown 消息"
        },
        {
            "type": "image",
            "name": "图片消息",
            "description": "支持 URL 链接、本地文件路径、base64 编码的图片消息"
        },
        {
            "type": "news",
            "name": "图文消息",
            "description": "支持多图文，可跳转链接的图文消息"
        },
        {
            "type": "file",
            "name": "文件消息",
            "description": "支持自动上传文件获取 media_id 的文件消息"
        },
        {
            "type": "voice",
            "name": "语音消息",
            "description": "支持 AMR 格式的语音文件消息"
        },
        {
            "type": "template_card",
            "name": "模板卡片",
            "description": "支持文本通知卡片和图文展示卡片的模板消息"
        }
    ]
    
    return {
        "errcode": 0,
        "errmsg": "ok",
        "message_types": message_types,
        "total_count": len(message_types)
    }

@mcp.tool(name="qyweixin_get_message_format", description="Get detailed format requirements for a specific message type.")
def qyweixin_get_message_format(
    message_type: Annotated[str, Field(description="Message type to query: text, markdown, markdown_v2, image, news, file, voice, template_card")],
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get detailed format requirements for a specific message type.
    
    Args:
        message_type (str): Message type to query format requirements for
        ctx (Context): Context
    
    Returns:
        dict: Detailed format requirements for the specified message type
    """
    
    formats = {
        "text": {
            "type": "text",
            "name": "文本消息",
            "description": "纯文本消息，支持 @用户、换行、超链接",
            "required_params": ["msg"],
            "optional_params": ["mentioned_list", "mentioned_mobile_list"],
            "limits": {
                "content_length": "最长 2048 字节",
                "mentions": "支持 @用户和手机号"
            },
            "format": {
                "msg": "消息内容文本",
                "mentioned_list": "要@的用户列表，@all表示所有人",
                "mentioned_mobile_list": "要@的手机号列表"
            },
            "example": {
                "msg": "今天的会议将在下午2点开始",
                "mentioned_list": ["@all"]
            }
        },
        "markdown": {
            "type": "markdown",
            "name": "Markdown 消息",
            "description": "支持基础 Markdown 语法的格式化消息",
            "required_params": ["msg"],
            "optional_params": [],
            "limits": {
                "content_length": "最长 4096 字节",
                "syntax": "支持基础 Markdown 语法"
            },
            "format": {
                "msg": "Markdown 格式的消息内容"
            },
            "example": {
                "msg": "# 标题\n**加粗文本**\n- 列表项1\n- 列表项2"
            }
        },
        "markdown_v2": {
            "type": "markdown_v2",
            "name": "增强 Markdown 消息",
            "description": "支持表格、代码块、图片等增强功能的 Markdown 消息",
            "required_params": ["msg"],
            "optional_params": [],
            "limits": {
                "content_length": "最长 4096 字节",
                "syntax": "支持表格、代码块、图片、分割线等"
            },
            "format": {
                "msg": "增强 Markdown 格式的消息内容"
            },
            "example": {
                "msg": "| 列1 | 列2 |\n|-----|-----|\n| 值1 | 值2 |\n```python\nprint('Hello')\n```"
            }
        },
        "image": {
            "type": "image",
            "name": "图片消息",
            "description": "支持 URL 链接、本地文件路径、base64 编码的图片消息",
            "required_params": ["msg"],
            "optional_params": [],
            "limits": {
                "file_size": "最大 2MB",
                "formats": "支持 JPG、PNG、GIF 等常见格式"
            },
            "format": {
                "msg": "图片 URL 链接或本地文件路径"
            },
            "example": {
                "msg": "https://example.com/image.jpg"
            }
        },
        "news": {
            "type": "news",
            "name": "图文消息",
            "description": "支持多图文，可跳转链接的图文消息",
            "required_params": ["title", "url"],
            "optional_params": ["description", "picurl"],
            "limits": {
                "articles": "最多 8 篇图文",
                "title_length": "标题最长 128 字节",
                "description_length": "描述最长 512 字节"
            },
            "format": {
                "title": "图文标题",
                "url": "跳转链接",
                "description": "图文描述（可选）",
                "picurl": "图片链接（可选）"
            },
            "example": {
                "title": "重要通知",
                "url": "https://example.com",
                "description": "请查看详细内容",
                "picurl": "https://example.com/pic.jpg"
            }
        },
        "file": {
            "type": "file",
            "name": "文件消息",
            "description": "支持自动上传文件获取 media_id 的文件消息",
            "required_params": ["msg"],
            "optional_params": [],
            "limits": {
                "file_size": "最大 20MB",
                "formats": "支持各种文件格式"
            },
            "format": {
                "msg": "文件路径或 media_id"
            },
            "example": {
                "msg": "/path/to/document.pdf"
            }
        },
        "voice": {
            "type": "voice",
            "name": "语音消息",
            "description": "支持 AMR 格式的语音文件消息",
            "required_params": ["msg"],
            "optional_params": [],
            "limits": {
                "file_size": "最大 2MB",
                "formats": "仅支持 AMR 格式",
                "duration": "最长 60 秒"
            },
            "format": {
                "msg": "AMR 格式语音文件路径或 media_id"
            },
            "example": {
                "msg": "/path/to/voice.amr"
            }
        },
        "template_card": {
            "type": "template_card",
            "name": "模板卡片",
            "description": "支持文本通知卡片和图文展示卡片的模板消息",
            "required_params": ["card_type", "main_title", "card_action_type"],
            "optional_params": [
                "main_title_desc", "source_desc", "source_icon_url", "card_action_url",
                "card_image_url", "card_image_aspect_ratio", "sub_title_text",
                "emphasis_title", "emphasis_desc"
            ],
            "limits": {
                "card_types": "text_notice（文本通知）或 news_notice（图文展示）",
                "title_length": "标题最长 128 字节",
                "aspect_ratio": "图片比例 1.25~2.25"
            },
            "format": {
                "card_type": "卡片类型：text_notice 或 news_notice",
                "main_title": "主标题",
                "card_action_type": "动作类型：1=跳转URL，2=跳转小程序",
                "card_action_url": "跳转链接（当 card_action_type=1 时必需）",
                "card_image_url": "卡片图片（news_notice 类型必需）"
            },
            "example": {
                "card_type": "text_notice",
                "main_title": "重要通知",
                "card_action_type": 1,
                "card_action_url": "https://example.com",
                "sub_title_text": "请及时查看"
            }
        }
    }
    
    if message_type not in formats:
        return {
            "errcode": -1,
            "errmsg": f"Unsupported message type: {message_type}. Supported types: {', '.join(formats.keys())}"
        }
    
    return {
        "errcode": 0,
        "errmsg": "ok",
        "format_info": formats[message_type]
    }

def run_server():
    errors = []
    if key is None:
        errors.append("- Notice key environment variable not set")
    else:
        logger.info(f"Using WeChat webhook key: {key[:3]}...{key[-3:]}")

    if len(errors) > 0:
        errors = ["Failed to start qyweixin bot MCP Server:"] + errors
        logger.error("\n".join(errors))
        return "\n".join(errors)
    else:
        logger.info("Starting qyweixin bot MCP Server...")
        # test msg
        # qyweixin_notice(msg="你好，这是一条测试消息", msgtype="text")

        logger.info("MCP server started and ready")
        logger.info(f"Registered tools: qyweixin_notice, qyweixin_upload_media, qyweixin_list_message_types, qyweixin_get_message_format")
        mcp.run()


if __name__ == "__main__":
    run_server()