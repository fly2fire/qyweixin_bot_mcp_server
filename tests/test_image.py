#!/usr/bin/env python3
"""
测试 Image 消息类型
"""

import base64
import hashlib
import requests
from test_utils import TestUtils


def test_image_from_url():
    """测试从URL发送图片"""
    utils = TestUtils()
    
    # 使用一个测试图片URL
    image_url = "https://mdn.alipayobjects.com/one_clip/afts/img/ARV_R4C8ygYAAAAATMAAAAgAoEACAQFr/original"
    
    try:
        # 获取图片数据
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # 转换为base64和计算MD5
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        image_md5 = hashlib.md5(response.content).hexdigest()
        
        data = {
            "msgtype": "image",
            "image": {
                "base64": image_base64,
                "md5": image_md5
            }
        }
        
        print(f"📏 图片大小: {len(response.content)} 字节")
        print(f"🔑 MD5: {image_md5}")
        
        result = utils.send_message(data)
        return result["success"]
        
    except Exception as e:
        print(f"❌ 图片处理失败: {str(e)}")
        return False


def test_small_image():
    """测试小尺寸图片"""
    utils = TestUtils()
    
    # 使用GitHub头像作为小图片测试
    image_url = "https://github.com/github.png"
    
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        image_md5 = hashlib.md5(response.content).hexdigest()
        
        data = {
            "msgtype": "image",
            "image": {
                "base64": image_base64,
                "md5": image_md5
            }
        }
        
        print(f"📏 图片大小: {len(response.content)} 字节")
        print(f"🔑 MD5: {image_md5}")
        
        result = utils.send_message(data)
        return result["success"]
        
    except Exception as e:
        print(f"❌ 图片处理失败: {str(e)}")
        return False


def test_base64_image():
    """测试直接使用base64编码的图片"""
    utils = TestUtils()
    
    # 创建一个简单的1x1像素PNG图片的base64编码
    # 这是一个透明的1x1像素PNG图片
    small_png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77kQAAAABJRU5ErkJggg=="
    
    # 计算MD5
    image_data = base64.b64decode(small_png_base64)
    image_md5 = hashlib.md5(image_data).hexdigest()
    
    data = {
        "msgtype": "image",
        "image": {
            "base64": small_png_base64,
            "md5": image_md5
        }
    }
    
    print(f"📏 图片大小: {len(image_data)} 字节")
    print(f"🔑 MD5: {image_md5}")
    
    result = utils.send_message(data)
    return result["success"]


def main():
    """主测试函数"""
    utils = TestUtils()
    
    # 检查配置
    if not utils.check_config():
        return
    
    # 测试用例
    test_cases = [
        ("从URL发送图片", test_image_from_url),
        ("发送小尺寸图片", test_small_image),
        ("发送Base64编码图片", test_base64_image),
    ]
    
    results = []
    for test_name, test_func in test_cases:
        utils.print_test_header(test_name)
        try:
            success = test_func()
            utils.print_test_result(test_name, success)
            results.append((test_name, success))
        except Exception as e:
            utils.print_test_result(test_name, False, str(e))
            results.append((test_name, False))
    
    # 总结
    utils.print_test_header("测试总结")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"   {status} {test_name}")


if __name__ == "__main__":
    main() 