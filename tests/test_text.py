#!/usr/bin/env python3
"""
测试 Text 消息类型
"""

from test_utils import TestUtils


def test_simple_text():
    """测试简单文本消息"""
    utils = TestUtils()
    
    data = {
        "msgtype": "text",
        "text": {
            "content": "🧪 这是一条简单的文本测试消息"
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_text_with_mention():
    """测试@用户的文本消息"""
    utils = TestUtils()
    
    data = {
        "msgtype": "text",
        "text": {
            "content": "📢 重要通知：请大家关注 @all",
            "mentioned_list": ["@all"]
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_text_with_phone():
    """测试@手机号的文本消息"""
    utils = TestUtils()
    
    data = {
        "msgtype": "text",
        "text": {
            "content": "📱 测试@手机号功能",
            "mentioned_mobile_list": ["13800138000"]
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_long_text():
    """测试长文本消息"""
    utils = TestUtils()
    
    content = """📝 长文本测试消息

这是一条用于测试长文本消息的内容。包含多行文本和各种字符。

主要功能：
- 支持换行符
- 支持中文字符
- 支持英文字符
- 支持数字：123456789
- 支持符号：!@#$%^&*()

测试内容：
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

结束测试 ✅"""
    
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    
    print(f"📏 内容长度: {len(content.encode('utf-8'))} 字节")
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
        ("简单文本消息", test_simple_text),
        ("@用户文本消息", test_text_with_mention),
        ("@手机号文本消息", test_text_with_phone),
        ("长文本消息", test_long_text),
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