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
    msg: Annotated[str, Field(description="Message content text")],
    msgtype: Annotated[str, Field(description="Message type, options: text, markdown, image, default is text. When the message type is an image, it can be an image URL address or the local full path of the image")] = "text",
    mentioned_list: Annotated[Optional[List[str]], Field(description="Notify specific members in group (@someone), @all means notify everyone, only valid for text messages")] = None,
    mentioned_mobile_list: Annotated[Optional[List[str]], Field(description="Notify members by mobile number, @all means notify everyone, only valid for text messages")] = None,
    ctx: Context = None):
    """
    Enterprise WeChat robot notification, send messages to group chats through the enterprise WeChat robot.

    Args:
        msg (str): Message content text
        msgtype (str): Message type, options: text, markdown, image, default is text. When the message type is an image, it can be an image URL address or the local full path of the image
        mentioned_list (List[str], optional): Notify specific members in group (@someone), @all means notify everyone, only valid for text messages
        mentioned_mobile_list (List[str], optional): Notify members by mobile number, @all means notify everyone, only valid for text messages
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
    
    else:
        return {"errcode": -1, "errmsg": f"Unsupported message type: {msgtype}"}
    
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