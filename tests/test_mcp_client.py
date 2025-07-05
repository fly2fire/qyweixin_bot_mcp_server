#!/usr/bin/env python3
"""
企业微信机器人 MCP 客户端测试
测试MCP服务器的各种功能
"""

import asyncio
import json
import os
import tempfile
import base64
from typing import Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClientTester:
    """MCP客户端测试类"""
    
    def __init__(self):
        self.results = []
        self.success_count = 0
        self.fail_count = 0
    
    def log_result(self, test_name: str, success: bool, message: str = "", result: Any = None):
        """记录测试结果"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.results.append({
            "test": test_name,
            "status": status,
            "message": message,
            "result": result
        })
        
        if success:
            self.success_count += 1
        else:
            self.fail_count += 1
            
        print(f"{status} {test_name}: {message}")
        if result and not success:
            print(f"   详情: {result}")
    
    async def test_server_connection(self, session: ClientSession):
        """测试服务器连接"""
        print("\n🔗 测试服务器连接...")
        
        try:
            # 初始化会话
            await session.initialize()
            self.log_result("服务器连接", True, "MCP服务器连接成功")
            return True
        except Exception as e:
            self.log_result("服务器连接", False, f"连接失败: {str(e)}")
            return False
    
    async def test_list_tools(self, session: ClientSession):
        """测试工具列表"""
        print("\n🛠️ 测试工具列表...")
        
        try:
            tools = await session.list_tools()
            expected_tools = [
                "qyweixin_text", "qyweixin_markdown", "qyweixin_markdown_v2",
                "qyweixin_image", "qyweixin_news", "qyweixin_file", "qyweixin_voice",
                "qyweixin_template_card", "qyweixin_upload_media", 
                "qyweixin_list_message_types", "qyweixin_get_message_format"
            ]
            
            tool_names = [tool.name for tool in tools.tools]
            missing_tools = [tool for tool in expected_tools if tool not in tool_names]
            
            if not missing_tools:
                self.log_result("工具列表", True, f"发现 {len(tool_names)} 个工具")
                print(f"   工具列表: {', '.join(tool_names)}")
                return True
            else:
                self.log_result("工具列表", False, f"缺少工具: {missing_tools}")
                return False
                
        except Exception as e:
            self.log_result("工具列表", False, f"获取工具列表失败: {str(e)}")
            return False
    
    async def test_list_message_types(self, session: ClientSession):
        """测试消息类型列表"""
        print("\n📋 测试消息类型列表...")
        
        try:
            result = await session.call_tool("qyweixin_list_message_types", {})
            
            if isinstance(result.content, list) and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    message_types = json.loads(content.text)
                    if len(message_types) == 8:
                        self.log_result("消息类型列表", True, f"获取到 {len(message_types)} 种消息类型")
                        return True
                    else:
                        self.log_result("消息类型列表", False, f"消息类型数量错误: {len(message_types)}")
                        return False
                else:
                    self.log_result("消息类型列表", False, "返回内容格式错误")
                    return False
            else:
                self.log_result("消息类型列表", False, "返回内容为空")
                return False
                
        except Exception as e:
            self.log_result("消息类型列表", False, f"调用失败: {str(e)}")
            return False
    
    async def test_get_message_format(self, session: ClientSession):
        """测试消息格式查询"""
        print("\n📄 测试消息格式查询...")
        
        try:
            result = await session.call_tool("qyweixin_get_message_format", {
                "message_type": "text"
            })
            
            if isinstance(result.content, list) and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    try:
                        format_info = json.loads(content.text)
                        # 检查是否包含必要的格式信息（使用type而不是message_type）
                        if isinstance(format_info, dict) and "type" in format_info:
                            self.log_result("消息格式查询", True, f"获取{format_info['type']}格式成功")
                            return True
                        else:
                            # 输出调试信息
                            print(f"   调试信息: {format_info}")
                            self.log_result("消息格式查询", False, "格式信息结构错误")
                            return False
                    except json.JSONDecodeError as e:
                        self.log_result("消息格式查询", False, f"JSON解析错误: {e}")
                        return False
                else:
                    self.log_result("消息格式查询", False, "返回内容格式错误")
                    return False
            else:
                self.log_result("消息格式查询", False, "返回内容为空")
                return False
                
        except Exception as e:
            self.log_result("消息格式查询", False, f"调用失败: {str(e)}")
            return False
    
    async def test_text_message(self, session: ClientSession):
        """测试文本消息"""
        print("\n💬 测试文本消息...")
        
        try:
            result = await session.call_tool("qyweixin_text", {
                "content": "🧪 MCP客户端测试 - 文本消息",
                "mentioned_list": ["@all"]
            })
            
            if isinstance(result.content, list) and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    response = json.loads(content.text)
                    if response.get('errcode') == 0:
                        self.log_result("文本消息发送", True, "发送成功")
                        return True
                    else:
                        self.log_result("文本消息发送", False, f"发送失败: {response}")
                        return False
                else:
                    self.log_result("文本消息发送", False, "返回内容格式错误")
                    return False
            else:
                self.log_result("文本消息发送", False, "返回内容为空")
                return False
                
        except Exception as e:
            self.log_result("文本消息发送", False, f"调用失败: {str(e)}")
            return False
    
    async def test_markdown_message(self, session: ClientSession):
        """测试Markdown消息"""
        print("\n📝 测试Markdown消息...")
        
        markdown_content = """# 🧪 MCP客户端测试报告

## 测试项目
- **连接测试**: ✅ 通过
- **工具列表**: ✅ 通过
- **消息发送**: 🔄 进行中

## 下一步
继续测试其他消息类型

> 📅 测试时间: 2024-01-01  
> 🔧 客户端版本: v1.0.0"""
        
        try:
            result = await session.call_tool("qyweixin_markdown", {
                "content": markdown_content
            })
            
            if isinstance(result.content, list) and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    response = json.loads(content.text)
                    if response.get('errcode') == 0:
                        self.log_result("Markdown消息发送", True, "发送成功")
                        return True
                    else:
                        self.log_result("Markdown消息发送", False, f"发送失败: {response}")
                        return False
                else:
                    self.log_result("Markdown消息发送", False, "返回内容格式错误")
                    return False
            else:
                self.log_result("Markdown消息发送", False, "返回内容为空")
                return False
                
        except Exception as e:
            self.log_result("Markdown消息发送", False, f"调用失败: {str(e)}")
            return False
    
    async def test_markdown_v2_message(self, session: ClientSession):
        """测试Markdown v2消息"""
        print("\n📄 测试Markdown v2消息...")
        
        markdown_v2_content = """# 🧪 MCP客户端测试 - Markdown v2

## 数据报表

### 价格对比表
| 产品 | 原价 | 现价 | 涨幅 |
|------|------|------|------|
| 苹果 | ¥5.0 | ¥6.5 | 30% |
| 香蕉 | ¥3.0 | ¥4.2 | 40% |
| 橘子 | ¥4.0 | ¥5.8 | 45% |

### 测试图片
![测试图片](https://mdn.alipayobjects.com/one_clip/afts/img/ARV_R4C8ygYAAAAATMAAAAgAoEACAQFr/original)

### 分割线测试
---

### 代码块测试
```json
{
  "status": "success",
  "data": {
    "count": 100,
    "message": "MCP测试数据"
  }
}
```

**结论：** Markdown v2 功能测试完成。"""
        
        try:
            result = await session.call_tool("qyweixin_markdown_v2", {
                "content": markdown_v2_content
            })
            
            if isinstance(result.content, list) and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    response = json.loads(content.text)
                    if response.get('errcode') == 0:
                        self.log_result("Markdown v2消息发送", True, "发送成功")
                        return True
                    else:
                        self.log_result("Markdown v2消息发送", False, f"发送失败: {response}")
                        return False
                else:
                    self.log_result("Markdown v2消息发送", False, "返回内容格式错误")
                    return False
            else:
                self.log_result("Markdown v2消息发送", False, "返回内容为空")
                return False
                
        except Exception as e:
            self.log_result("Markdown v2消息发送", False, f"调用失败: {str(e)}")
            return False
    
    async def test_file_message(self, session: ClientSession):
        """测试文件消息（只测试工具调用）"""
        print("\n📁 测试文件消息...")
        
        # 创建一个临时文本文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
            tmp_file.write("MCP客户端测试文件内容\n测试时间: 2024-01-01\n")
            file_path = tmp_file.name
        
        try:
            result = await session.call_tool("qyweixin_file", {
                "file_path": file_path
            })
            
            # 只要工具调用成功返回，就认为MCP调用成功
            if isinstance(result.content, list) and len(result.content) > 0:
                self.log_result("文件消息调用", True, "MCP工具调用成功")
                return True
            else:
                self.log_result("文件消息调用", False, "MCP工具调用失败")
                return False
                
        except Exception as e:
            self.log_result("文件消息调用", False, f"调用失败: {str(e)}")
            return False
        finally:
            # 清理临时文件
            try:
                os.unlink(file_path)
            except:
                pass
    
    async def test_voice_message(self, session: ClientSession):
        """测试语音消息（只测试工具调用）"""
        print("\n🎤 测试语音消息...")
        
        # 创建一个临时AMR文件（模拟）
        with tempfile.NamedTemporaryFile(suffix='.amr', delete=False) as tmp_file:
            # 写入AMR文件头（模拟语音文件）
            tmp_file.write(b"#!AMR\n")
            tmp_file.write(b"fake amr content for testing")
            voice_path = tmp_file.name
        
        try:
            result = await session.call_tool("qyweixin_voice", {
                "voice_path": voice_path
            })
            
            # 只要工具调用成功返回，就认为MCP调用成功
            if isinstance(result.content, list) and len(result.content) > 0:
                self.log_result("语音消息调用", True, "MCP工具调用成功")
                return True
            else:
                self.log_result("语音消息调用", False, "MCP工具调用失败")
                return False
                
        except Exception as e:
            self.log_result("语音消息调用", False, f"调用失败: {str(e)}")
            return False
        finally:
            # 清理临时文件
            try:
                os.unlink(voice_path)
            except:
                pass
    
    async def test_image_message(self, session: ClientSession):
        """测试图片消息"""
        print("\n🖼️ 测试图片消息...")
        
        try:
            # 使用有效图片URL测试实际发送
            result = await session.call_tool("qyweixin_image", {
                "image_url": "https://mdn.alipayobjects.com/one_clip/afts/img/ARV_R4C8ygYAAAAATMAAAAgAoEACAQFr/original"
            })
            
            if isinstance(result.content, list) and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    response = json.loads(content.text)
                    if response.get('errcode') == 0:
                        self.log_result("图片消息发送", True, "发送成功")
                        return True
                    else:
                        self.log_result("图片消息发送", False, f"发送失败: {response}")
                        return False
                else:
                    self.log_result("图片消息发送", False, "返回内容格式错误")
                    return False
            else:
                self.log_result("图片消息发送", False, "返回内容为空")
                return False
                
        except Exception as e:
            self.log_result("图片消息发送", False, f"调用失败: {str(e)}")
            return False
    
    async def test_news_message(self, session: ClientSession):
        """测试图文消息"""
        print("\n📰 测试图文消息...")
        
        try:
            result = await session.call_tool("qyweixin_news", {
                "articles": [
                    {
                        "title": "🧪 MCP客户端测试",
                        "description": "企业微信机器人MCP服务器客户端功能测试",
                        "url": "https://example.com/test",
                        "picurl": "https://mdn.alipayobjects.com/one_clip/afts/img/ARV_R4C8ygYAAAAATMAAAAgAoEACAQFr/original"
                    }
                ]
            })
            
            if isinstance(result.content, list) and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    response = json.loads(content.text)
                    if response.get('errcode') == 0:
                        self.log_result("图文消息发送", True, "发送成功")
                        return True
                    else:
                        self.log_result("图文消息发送", False, f"发送失败: {response}")
                        return False
                else:
                    self.log_result("图文消息发送", False, "返回内容格式错误")
                    return False
            else:
                self.log_result("图文消息发送", False, "返回内容为空")
                return False
                
        except Exception as e:
            self.log_result("图文消息发送", False, f"调用失败: {str(e)}")
            return False
    
    async def test_template_card_message(self, session: ClientSession):
        """测试模板卡片消息（只测试工具调用，不测试实际发送）"""
        print("\n🎴 测试模板卡片消息...")
        
        try:
            result = await session.call_tool("qyweixin_template_card", {
                "card_type": "text_notice",
                "source": {
                    "icon_url": "https://mdn.alipayobjects.com/one_clip/afts/img/ARV_R4C8ygYAAAAATMAAAAgAoEACAQFr/original",
                    "desc": "MCP测试客户端"
                },
                "main_title": {
                    "title": "🧪 客户端测试完成",
                    "desc": "MCP服务器功能测试"
                },
                "emphasis_content": {
                    "title": "测试状态",
                    "desc": "进行中"
                },
                "sub_title_text": "测试时间：2024-01-01",
                "horizontal_content_list": [
                    {
                        "keyname": "连接测试",
                        "value": "✅ 通过"
                    },
                    {
                        "keyname": "消息发送",
                        "value": "🔄 测试中"
                    }
                ]
            })
            
            # 只要工具调用成功返回，就认为MCP调用成功
            if isinstance(result.content, list) and len(result.content) > 0:
                self.log_result("模板卡片消息调用", True, "MCP工具调用成功")
                return True
            else:
                self.log_result("模板卡片消息调用", False, "MCP工具调用失败")
                return False
                
        except Exception as e:
            self.log_result("模板卡片消息调用", False, f"调用失败: {str(e)}")
            return False
    
    def print_summary(self):
        """打印测试总结"""
        print("\n" + "="*60)
        print(f"📊 MCP客户端测试总结")
        print("="*60)
        print(f"✅ 成功: {self.success_count}")
        print(f"❌ 失败: {self.fail_count}")
        print(f"📈 成功率: {(self.success_count/(self.success_count+self.fail_count)*100):.1f}%")
        print("\n📋 详细结果:")
        for result in self.results:
            print(f"  {result['status']} {result['test']}: {result['message']}")
        print("="*60)


async def main():
    """主测试函数"""
    print("🚀 启动企业微信机器人MCP客户端测试")
    print("="*60)
    
    # 检查环境变量
    webhook_key = os.environ.get("key")
    if not webhook_key:
        print("❌ 环境变量 'key' 未设置")
        print("请设置: export key=your_webhook_key")
        return
    
    print(f"🔑 使用Webhook Key: {webhook_key[:8]}...")
    
    # MCP服务器参数
    server_params = StdioServerParameters(
        command="python",
        args=["../server.py"],
        env={"key": webhook_key}
    )
    
    tester = MCPClientTester()
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 测试连接
                if not await tester.test_server_connection(session):
                    print("❌ 服务器连接失败，停止测试")
                    return
                
                # 测试工具列表
                if not await tester.test_list_tools(session):
                    print("❌ 工具列表获取失败，停止测试")
                    return
                
                # 测试辅助函数
                await tester.test_list_message_types(session)
                await tester.test_get_message_format(session)
                
                # 测试各种消息类型
                await tester.test_text_message(session)
                await tester.test_markdown_message(session)
                await tester.test_markdown_v2_message(session)
                await tester.test_file_message(session)
                await tester.test_voice_message(session)
                await tester.test_image_message(session)
                await tester.test_news_message(session)
                await tester.test_template_card_message(session)
                
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")
        tester.log_result("总体测试", False, f"测试异常: {str(e)}")
    
    finally:
        tester.print_summary()


if __name__ == "__main__":
    asyncio.run(main()) 