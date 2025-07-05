import os
import requests
import hashlib
import base64
from typing import Dict, Any, Optional, List
from config import WEBHOOK_URL, REQUEST_TIMEOUT, MAX_TEXT_LENGTH, MAX_MARKDOWN_LENGTH, MAX_IMAGE_SIZE
from utils import qyweixin_upload_media


def _send_message(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    发送消息到企业微信的通用函数
    
    Args:
        data: 消息数据字典
    
    Returns:
        Dict: 响应结果
    """
    response = requests.post(
        WEBHOOK_URL,
        json=data,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def qyweixin_text(content: str, mentioned_list: Optional[List[str]] = None, 
                  mentioned_mobile_list: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    发送文本消息
    
    Args:
        content: 文本内容
        mentioned_list: 用户ID列表，用于@指定用户
        mentioned_mobile_list: 手机号列表，用于@指定用户
    
    Returns:
        Dict: 发送结果
    """
    if len(content.encode('utf-8')) > MAX_TEXT_LENGTH:
        raise ValueError(f"文本内容过长，最大支持{MAX_TEXT_LENGTH}字节")
    
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    
    if mentioned_list:
        data["text"]["mentioned_list"] = mentioned_list
    if mentioned_mobile_list:
        data["text"]["mentioned_mobile_list"] = mentioned_mobile_list
    
    return _send_message(data)


def qyweixin_markdown(content: str) -> Dict[str, Any]:
    """
    发送Markdown消息
    
    Args:
        content: Markdown内容
    
    Returns:
        Dict: 发送结果
    """
    if len(content.encode('utf-8')) > MAX_MARKDOWN_LENGTH:
        raise ValueError(f"Markdown内容过长，最大支持{MAX_MARKDOWN_LENGTH}字节")
    
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    
    return _send_message(data)


def qyweixin_markdown_v2(content: str) -> Dict[str, Any]:
    """
    发送Markdown增强消息（注意：企业微信实际上并不支持markdown_v2类型，这里发送的是普通markdown）
    
    Args:
        content: Markdown v2内容（支持表格、图片、分割线、代码块等增强功能）
    
    Returns:
        Dict: 发送结果
    """
    if len(content.encode('utf-8')) > MAX_MARKDOWN_LENGTH:
        raise ValueError(f"Markdown v2内容过长，最大支持{MAX_MARKDOWN_LENGTH}字节")
    
    # 实际发送的是普通markdown类型，因为企业微信不支持markdown_v2
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    
    return _send_message(data)


def qyweixin_image(image_url: Optional[str] = None, image_path: Optional[str] = None, 
                   image_base64: Optional[str] = None, image_md5: Optional[str] = None) -> Dict[str, Any]:
    """
    发送图片消息
    
    Args:
        image_url: 图片URL地址
        image_path: 本地图片文件路径
        image_base64: 图片base64编码
        image_md5: 图片MD5值
    
    Returns:
        Dict: 发送结果
    """
    if not any([image_url, image_path, image_base64]):
        raise ValueError("必须提供image_url、image_path或image_base64中的一个")
    
    data = {
        "msgtype": "image",
        "image": {}
    }
    
    if image_url:
        data["image"]["base64"] = _get_image_base64_from_url(image_url)
        data["image"]["md5"] = _get_image_md5_from_url(image_url)
    elif image_path:
        data["image"]["base64"] = _get_image_base64_from_file(image_path)
        data["image"]["md5"] = _get_image_md5_from_file(image_path)
    else:
        data["image"]["base64"] = image_base64
        if image_md5:
            data["image"]["md5"] = image_md5
        else:
            data["image"]["md5"] = _get_md5_from_base64(image_base64)
    
    return _send_message(data)


def qyweixin_news(articles: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    发送图文消息
    
    Args:
        articles: 图文列表，每个元素包含title、url、description、picurl
    
    Returns:
        Dict: 发送结果
    """
    if not articles:
        raise ValueError("图文列表不能为空")
    
    if len(articles) > 8:
        raise ValueError("图文消息最多支持8篇文章")
    
    for article in articles:
        if not article.get("title") or not article.get("url"):
            raise ValueError("每篇图文消息必须包含title和url")
    
    data = {
        "msgtype": "news",
        "news": {
            "articles": articles
        }
    }
    
    return _send_message(data)


def qyweixin_file(file_path: Optional[str] = None, media_id: Optional[str] = None) -> Dict[str, Any]:
    """
    发送文件消息
    
    Args:
        file_path: 本地文件路径
        media_id: 已上传文件的media_id
    
    Returns:
        Dict: 发送结果
    """
    if not file_path and not media_id:
        raise ValueError("必须提供file_path或media_id")
    
    if file_path and not media_id:
        media_id = qyweixin_upload_media(file_path, "file")
    
    data = {
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }
    
    return _send_message(data)


def qyweixin_voice(voice_path: Optional[str] = None, media_id: Optional[str] = None) -> Dict[str, Any]:
    """
    发送语音消息
    
    Args:
        voice_path: 本地语音文件路径（AMR格式）
        media_id: 已上传语音的media_id
    
    Returns:
        Dict: 发送结果
    """
    if not voice_path and not media_id:
        raise ValueError("必须提供voice_path或media_id")
    
    if voice_path and not media_id:
        media_id = qyweixin_upload_media(voice_path, "voice")
    
    data = {
        "msgtype": "voice",
        "voice": {
            "media_id": media_id
        }
    }
    
    return _send_message(data)


def qyweixin_template_card(card_type: str, **kwargs) -> Dict[str, Any]:
    """
    发送模板卡片消息
    
    Args:
        card_type: 卡片类型，"text_notice"或"news_notice"
        **kwargs: 其他卡片参数
    
    Returns:
        Dict: 发送结果
    """
    if card_type not in ["text_notice", "news_notice"]:
        raise ValueError("card_type必须是'text_notice'或'news_notice'")
    
    template_card = {
        "card_type": card_type,
        **kwargs
    }
    
    data = {
        "msgtype": "template_card",
        "template_card": template_card
    }
    
    return _send_message(data)


# 图片处理辅助函数
def _get_image_base64_from_url(url: str) -> str:
    """从URL获取图片base64编码"""
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    
    if len(response.content) > MAX_IMAGE_SIZE:
        raise ValueError(f"图片大小超出限制: {len(response.content)} > {MAX_IMAGE_SIZE}")
    
    return base64.b64encode(response.content).decode('utf-8')


def _get_image_md5_from_url(url: str) -> str:
    """从URL获取图片MD5值"""
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return hashlib.md5(response.content).hexdigest()


def _get_image_base64_from_file(file_path: str) -> str:
    """从本地文件获取图片base64编码"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    file_size = os.path.getsize(file_path)
    if file_size > MAX_IMAGE_SIZE:
        raise ValueError(f"图片大小超出限制: {file_size} > {MAX_IMAGE_SIZE}")
    
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def _get_image_md5_from_file(file_path: str) -> str:
    """从本地文件获取图片MD5值"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def _get_md5_from_base64(base64_str: str) -> str:
    """从base64字符串获取MD5值"""
    image_data = base64.b64decode(base64_str)
    return hashlib.md5(image_data).hexdigest() 