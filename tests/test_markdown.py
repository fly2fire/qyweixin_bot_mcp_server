#!/usr/bin/env python3
"""
测试 Markdown 消息类型
"""

from test_utils import TestUtils


def test_simple_markdown():
    """测试简单的markdown消息"""
    utils = TestUtils()
    
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": "# 测试标题\n\n这是一个简单的**markdown**测试消息\n\n- 列表项1\n- 列表项2"
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_markdown_with_code():
    """测试包含代码的markdown消息"""
    utils = TestUtils()
    
    content = """# 代码测试

## 行内代码
这是一个 `inline code` 示例

## 代码块
```python
def hello_world():
    print("Hello, World!")
    return "success"
```

## 其他格式
- **粗体文本**
- *斜体文本*
- [链接](https://example.com)

> 这是一个引用

测试完成 ✅"""
    
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_markdown_with_color():
    """测试包含颜色的markdown消息"""
    utils = TestUtils()
    
    content = """# 颜色测试

## 支持的颜色
<font color="info">蓝色信息文本</font>
<font color="comment">灰色注释文本</font>
<font color="warning">橙色警告文本</font>

## 普通格式
**重要信息**
*提示内容*

测试完成 ✅"""
    
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_markdown_notification():
    """测试通知类型的markdown消息"""
    utils = TestUtils()
    
    content = """# 📢 系统通知

## 🔔 重要更新
系统将于今晚 **22:00-24:00** 进行维护

## 📝 影响范围
- 用户登录功能暂时不可用
- 数据同步将延迟
- 部分接口可能响应缓慢

## 🚀 新功能预览
> 维护完成后，我们将上线以下新功能：
> - 更快的数据处理速度
> - 优化的用户界面
> - 增强的安全性

## 📞 联系方式
如有紧急问题，请联系：
- 技术支持：`tech@example.com`
- 客服热线：`400-123-4567`

感谢您的理解与支持！"""
    
    data = {
        "msgtype": "markdown",
        "markdown": {
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
        ("简单Markdown消息", test_simple_markdown),
        ("包含代码的Markdown消息", test_markdown_with_code),
        ("包含颜色的Markdown消息", test_markdown_with_color),
        ("通知类型Markdown消息", test_markdown_notification),
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