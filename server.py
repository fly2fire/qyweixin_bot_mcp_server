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
        logger.info(f"Registered tool: qyweixin_notice")
        mcp.run()


if __name__ == "__main__":
    run_server()