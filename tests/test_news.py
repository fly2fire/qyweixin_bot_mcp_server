#!/usr/bin/env python3
"""
测试 News 消息类型
"""

from test_utils import TestUtils


def test_single_news():
    """测试单篇图文消息"""
    utils = TestUtils()
    
    data = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": "🧪 单篇图文测试",
                    "description": "这是一个测试单篇图文消息的示例",
                    "url": "https://github.com/fly2fire/qyweixin_bot_mcp_server",
                    "picurl": "https://github.com/github.png"
                }
            ]
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_multiple_news():
    """测试多篇图文消息"""
    utils = TestUtils()
    
    data = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": "📈 辣椒价格分析报告",
                    "description": "2025年6月6日-6月20日辣椒价格走势详细分析，包含小米椒、精品尖椒、红彩椒、黄彩椒等品类价格数据",
                    "url": "https://example.com/pepper-analysis",
                    "picurl": "https://mdn.alipayobjects.com/one_clip/afts/img/ARV_R4C8ygYAAAAATMAAAAgAoEACAQFr/original"
                },
                {
                    "title": "🔍 市场趋势解读",
                    "description": "深度分析当前农产品市场走势，预测未来价格变化趋势",
                    "url": "https://example.com/market-trend",
                    "picurl": "https://github.com/github.png"
                },
                {
                    "title": "💡 投资建议",
                    "description": "基于市场分析给出的专业投资建议和风险提示",
                    "url": "https://example.com/investment-advice"
                }
            ]
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_news_without_image():
    """测试没有图片的图文消息"""
    utils = TestUtils()
    
    data = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": "📝 纯文本图文消息",
                    "description": "这是一个没有配图的图文消息测试",
                    "url": "https://example.com/text-only"
                }
            ]
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_news_minimal():
    """测试最简图文消息（仅包含必需字段）"""
    utils = TestUtils()
    
    data = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": "🎯 最简图文消息",
                    "url": "https://example.com/minimal"
                }
            ]
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_max_news():
    """测试最大数量图文消息（8篇）"""
    utils = TestUtils()
    
    articles = []
    for i in range(8):
        articles.append({
            "title": f"📊 图文消息 {i+1}",
            "description": f"这是第{i+1}篇图文消息的描述内容",
            "url": f"https://example.com/article-{i+1}",
            "picurl": "https://github.com/github.png" if i % 2 == 0 else None
        })
    
    # 移除None值
    for article in articles:
        if article.get("picurl") is None:
            del article["picurl"]
    
    data = {
        "msgtype": "news",
        "news": {
            "articles": articles
        }
    }
    
    print(f"📰 文章数量: {len(articles)}")
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
        ("单篇图文消息", test_single_news),
        ("多篇图文消息", test_multiple_news),
        ("无图片图文消息", test_news_without_image),
        ("最简图文消息", test_news_minimal),
        ("最大数量图文消息", test_max_news),
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