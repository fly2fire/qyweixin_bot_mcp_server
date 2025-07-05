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
        {"type": "text", "name": "文本消息", "description": "发送纯文本消息"},
        {"type": "markdown", "name": "Markdown消息", "description": "发送markdown格式消息"},
        {"type": "markdown_v2", "name": "Markdown增强消息", "description": "发送增强markdown消息"},
        {"type": "image", "name": "图片消息", "description": "发送图片消息"},
        {"type": "news", "name": "图文消息", "description": "发送图文消息"},
        {"type": "file", "name": "文件消息", "description": "发送文件消息"},
        {"type": "voice", "name": "语音消息", "description": "发送语音消息"},
        {"type": "template_card", "name": "模板卡片消息", "description": "发送模板卡片消息"}
    ]


def qyweixin_get_message_format(message_type: str) -> Dict[str, Any]:
    """获取指定消息类型的格式要求和参数说明"""
    if message_type not in MESSAGE_TYPES:
        raise ValueError(f"不支持的消息类型: {message_type}")
    
    # 基础格式信息
    format_info = {
        "type": message_type,
        "name": f"{message_type}消息",
        "description": f"发送{message_type}格式消息",
        "required_params": [],
        "optional_params": [],
        "limitations": []
    }
    
    # 根据消息类型设置详细信息
    if message_type == "text":
        format_info.update({
            "name": "文本消息",
            "description": "纯文本消息，支持@用户、换行、超链接",
            "required_params": ["content"],
            "optional_params": ["mentioned_list", "mentioned_mobile_list"],
            "limitations": ["最长2048字节", "支持换行符", "支持@用户功能"]
        })
    elif message_type == "markdown":
        format_info.update({
            "name": "Markdown消息",
            "description": "支持基础markdown语法的格式化消息",
            "required_params": ["content"],
            "optional_params": [],
            "limitations": ["最长4096字节", "支持基础markdown语法", "支持有限的字体颜色"]
        })
    elif message_type == "markdown_v2":
        format_info.update({
            "name": "Markdown增强消息",
            "description": "支持表格、图片、代码块等增强功能的markdown消息",
            "required_params": ["content"],
            "optional_params": [],
            "limitations": ["最长4096字节", "不支持字体颜色", "不支持@功能", "图片无法控制大小"]
        })
    elif message_type == "image":
        format_info.update({
            "name": "图片消息",
            "description": "支持URL、本地文件、base64编码的图片消息",
            "required_params": [],
            "optional_params": ["image_url", "image_path", "image_base64", "image_md5"],
            "limitations": ["图片大小不超过2MB", "支持JPG、PNG、GIF等常见格式", "无法控制显示大小"]
        })
    elif message_type == "news":
        format_info.update({
            "name": "图文消息",
            "description": "支持多篇图文，可跳转链接的图文消息",
            "required_params": ["articles"],
            "optional_params": [],
            "limitations": ["最多8篇文章", "title和url为必需字段", "建议图片尺寸大图1068×455，小图150×150"]
        })
    elif message_type == "file":
        format_info.update({
            "name": "文件消息",
            "description": "支持自动上传文件获取media_id的文件消息",
            "required_params": [],
            "optional_params": ["file_path", "media_id"],
            "limitations": ["文件大小不超过20MB", "支持各种文件格式", "上传后media_id有效期3天"]
        })
    elif message_type == "voice":
        format_info.update({
            "name": "语音消息",
            "description": "支持AMR格式的语音文件消息",
            "required_params": [],
            "optional_params": ["voice_path", "media_id"],
            "limitations": ["文件大小不超过2MB", "仅支持AMR格式", "上传后media_id有效期3天", "语音时长建议不超过60秒"]
        })
    elif message_type == "template_card":
        format_info.update({
            "name": "模板卡片消息",
            "description": "支持文本通知卡片和图文展示卡片的模板消息",
            "required_params": ["card_type"],
            "optional_params": [
                "source", "action_menu", "task_id", "main_title", "emphasis_content", 
                "sub_title_text", "horizontal_content_list", "jump_list", "card_action",
                "card_image_url", "aspect_ratio", "image_text_area", "vertical_content_list", "action_list"
            ],
            "limitations": ["card_type为必需参数", "不同卡片类型有不同的必需字段", "图片宽高比范围1.3-2.25", "标题建议不超过36个字节"]
        })
    
    return format_info
