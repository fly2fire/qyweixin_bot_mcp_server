#!/usr/bin/env python3
"""
测试工具类
"""

import json
import requests
import os
import sys
from typing import Dict, Any, Optional

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import KEY, WEBHOOK_URL


class TestUtils:
    """企业微信机器人测试工具类"""
    
    def __init__(self):
        self.webhook_url = WEBHOOK_URL
        self.headers = {'Content-Type': 'application/json'}
        self.timeout = 30
    
    def send_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送消息到企业微信"""
        try:
            print(f"📤 发送消息: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            response = requests.post(
                self.webhook_url,
                json=data,
                headers=self.headers,
                timeout=self.timeout
            )
            
            print(f"🔍 响应状态码: {response.status_code}")
            print(f"🔍 响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('errcode') == 0:
                    print("✅ 消息发送成功")
                    return {"success": True, "data": result}
                else:
                    print(f"❌ 消息发送失败: {result}")
                    return {"success": False, "error": result}
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def print_test_header(self, test_name: str):
        """打印测试头部信息"""
        print(f"\n{'='*50}")
        print(f"🧪 {test_name}")
        print(f"{'='*50}")
    
    def print_test_result(self, test_name: str, success: bool, error: Optional[str] = None):
        """打印测试结果"""
        if success:
            print(f"✅ {test_name} - 测试通过")
        else:
            print(f"❌ {test_name} - 测试失败")
            if error:
                print(f"   错误信息: {error}")
    
    def check_config(self) -> bool:
        """检查配置是否正确"""
        if not KEY:
            print("❌ 环境变量 'key' 未设置")
            return False
        
        print(f"✅ 配置检查通过")
        print(f"   Webhook URL: {self.webhook_url}")
        return True
    
    def test_simple_text(self) -> bool:
        """测试简单文本消息"""
        data = {
            "msgtype": "text",
            "text": {
                "content": "🧪 这是一条测试消息"
            }
        }
        
        result = self.send_message(data)
        return result["success"] 