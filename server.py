from fastmcp import FastMCP, Context
import logging
from pydantic import Field
from typing import Annotated, Optional, List, Dict, Any

# 导入消息发送函数
from message_tools import (
    qyweixin_text, qyweixin_markdown, qyweixin_markdown_v2, qyweixin_image,
    qyweixin_news, qyweixin_file, qyweixin_voice, qyweixin_template_card
)

# 导入辅助工具函数
from utils import qyweixin_upload_media, qyweixin_list_message_types, qyweixin_get_message_format

# 导入配置
from config import KEY

logger = logging.getLogger("mcp")

mcp = FastMCP("qyweixin bot MCP Server", log_level='ERROR')

# 检查环境变量
if not KEY:
    raise ValueError("环境变量 'key' 未设置，请设置企业微信群机器人的Webhook Key")


@mcp.tool(name="qyweixin_text", description="Send text message to Enterprise WeChat group.")
def tool_qyweixin_text(
    content: Annotated[str, Field(description="Text message content")],
    mentioned_list: Annotated[Optional[List[str]], Field(description="List of users to mention (@someone), @all means mention everyone")] = None,
    mentioned_mobile_list: Annotated[Optional[List[str]], Field(description="List of mobile numbers to mention (@someone), @all means mention everyone")] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Send text message to Enterprise WeChat group."""
    return qyweixin_text(content, mentioned_list, mentioned_mobile_list)


@mcp.tool(name="qyweixin_markdown", description="Send markdown message to Enterprise WeChat group.")
def tool_qyweixin_markdown(
    content: Annotated[str, Field(description="Markdown format message content")],
    ctx: Context = None
) -> Dict[str, Any]:
    """Send markdown message to Enterprise WeChat group."""
    return qyweixin_markdown(content)


@mcp.tool(name="qyweixin_markdown_v2", description="Send enhanced markdown message to Enterprise WeChat group (Note: Actually sends regular markdown type, as WeChat Work doesn't support standalone markdown_v2 type).")
def tool_qyweixin_markdown_v2(
    content: Annotated[str, Field(description="Enhanced markdown format message content, supports tables, code blocks, images, etc. (Note: Actually sends as regular markdown)")],
    ctx: Context = None
) -> Dict[str, Any]:
    """Send enhanced markdown message to Enterprise WeChat group."""
    return qyweixin_markdown_v2(content)


@mcp.tool(name="qyweixin_image", description="Send image message to Enterprise WeChat group.")
def tool_qyweixin_image(
    image_url: Annotated[Optional[str], Field(description="Image URL")] = None,
    image_path: Annotated[Optional[str], Field(description="Local image file path")] = None,
    image_base64: Annotated[Optional[str], Field(description="Base64 encoded image data")] = None,
    image_md5: Annotated[Optional[str], Field(description="MD5 hash of image data, optional")] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Send image message to Enterprise WeChat group."""
    return qyweixin_image(image_url, image_path, image_base64, image_md5)


@mcp.tool(name="qyweixin_news", description="Send news message to Enterprise WeChat group.")
def tool_qyweixin_news(
    articles: Annotated[List[Dict[str, str]], Field(description="List of articles, each containing title, url, description, picurl")],
    ctx: Context = None
) -> Dict[str, Any]:
    """Send news message to Enterprise WeChat group."""
    return qyweixin_news(articles)


@mcp.tool(name="qyweixin_file", description="Send file message to Enterprise WeChat group.")
def tool_qyweixin_file(
    file_path: Annotated[Optional[str], Field(description="Local file path")] = None,
    media_id: Annotated[Optional[str], Field(description="Already uploaded file media_id")] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Send file message to Enterprise WeChat group."""
    return qyweixin_file(file_path, media_id)


@mcp.tool(name="qyweixin_voice", description="Send voice message to Enterprise WeChat group.")
def tool_qyweixin_voice(
    voice_path: Annotated[Optional[str], Field(description="Local voice file path (AMR format)")] = None,
    media_id: Annotated[Optional[str], Field(description="Already uploaded voice media_id")] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Send voice message to Enterprise WeChat group."""
    return qyweixin_voice(voice_path, media_id)


@mcp.tool(name="qyweixin_template_card", description="Send template card message to Enterprise WeChat group.")
def tool_qyweixin_template_card(
    card_type: Annotated[str, Field(description="Template card type: text_notice or news_notice")],
    main_title: Annotated[Optional[str], Field(description="Main title for template card")] = None,
    card_action_type: Annotated[Optional[int], Field(description="Card action type: 1=jump to URL, 2=jump to mini program")] = None,
    card_action_url: Annotated[Optional[str], Field(description="Card action URL, required when card_action_type=1")] = None,
    main_title_desc: Annotated[Optional[str], Field(description="Main title description for template card")] = None,
    source_desc: Annotated[Optional[str], Field(description="Card source description")] = None,
    source_icon_url: Annotated[Optional[str], Field(description="Card source icon URL")] = None,
    card_image_url: Annotated[Optional[str], Field(description="Card image URL, required for news_notice type")] = None,
    card_image_aspect_ratio: Annotated[Optional[float], Field(description="Card image aspect ratio, optional for news_notice type")] = None,
    sub_title_text: Annotated[Optional[str], Field(description="Sub title text, optional for text_notice type")] = None,
    emphasis_title: Annotated[Optional[str], Field(description="Emphasis content title, optional for text_notice type")] = None,
    emphasis_desc: Annotated[Optional[str], Field(description="Emphasis content description, optional for text_notice type")] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Send template card message to Enterprise WeChat group."""
    
    # 构建卡片参数
    card_params = {}
    
    if main_title:
        card_params["main_title"] = {"title": main_title}
        if main_title_desc:
            card_params["main_title"]["desc"] = main_title_desc
    
    if card_action_type:
        card_params["card_action"] = {"type": card_action_type}
        if card_action_url:
            card_params["card_action"]["url"] = card_action_url
    
    if source_desc or source_icon_url:
        card_params["source"] = {}
        if source_desc:
            card_params["source"]["desc"] = source_desc
        if source_icon_url:
            card_params["source"]["icon_url"] = source_icon_url
    
    if card_type == "news_notice" and card_image_url:
        card_params["card_image_url"] = card_image_url
        if card_image_aspect_ratio:
            card_params["aspect_ratio"] = card_image_aspect_ratio
    
    if card_type == "text_notice":
        if sub_title_text:
            card_params["sub_title_text"] = sub_title_text
        if emphasis_title or emphasis_desc:
            card_params["emphasis_content"] = {}
            if emphasis_title:
                card_params["emphasis_content"]["title"] = emphasis_title
            if emphasis_desc:
                card_params["emphasis_content"]["desc"] = emphasis_desc
    
    return qyweixin_template_card(card_type, **card_params)


@mcp.tool(name="qyweixin_upload_media", description="Upload file or voice to Enterprise WeChat robot and get media_id.")
def tool_qyweixin_upload_media(
    file_path: Annotated[str, Field(description="Local file path to upload")],
    media_type: Annotated[str, Field(description="Media type: file or voice")] = "file",
    ctx: Context = None
) -> str:
    """Upload file or voice to Enterprise WeChat robot and get media_id."""
    try:
        return qyweixin_upload_media(file_path, media_type)
    except Exception as e:
        raise Exception(f"上传媒体文件失败: {str(e)}")


@mcp.tool(name="qyweixin_list_message_types", description="List all supported message types for Enterprise WeChat robot.")
def tool_qyweixin_list_message_types(ctx: Context = None) -> List[Dict[str, Any]]:
    """List all supported message types for Enterprise WeChat robot."""
    return qyweixin_list_message_types()


@mcp.tool(name="qyweixin_get_message_format", description="Get detailed format requirements for a specific message type.")
def tool_qyweixin_get_message_format(
    message_type: Annotated[str, Field(description="Message type to query: text, markdown, markdown_v2, image, news, file, voice, template_card")],
    ctx: Context = None
) -> Dict[str, Any]:
    """Get detailed format requirements for a specific message type."""
    return qyweixin_get_message_format(message_type)


def run_server():
    """启动MCP服务器"""
    logger.info("🚀 启动企业微信机器人MCP服务器...")
    logger.info(f"📡 Webhook Key: {KEY[:8]}..." if KEY else "❌ 未设置Webhook Key")
    mcp.run()


if __name__ == "__main__":
    run_server()