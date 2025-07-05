#!/usr/bin/env python3
"""
测试 Template Card 消息类型
"""

from test_utils import TestUtils


def test_text_notice_simple():
    """测试简单文本通知卡片"""
    utils = TestUtils()
    
    data = {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "text_notice",
            "source": {
                "icon_url": "https://github.com/github.png",
                "desc": "测试通知"
            },
            "main_title": {
                "title": "🧪 简单文本卡片测试",
                "desc": "这是一个简单的文本通知卡片测试"
            }
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_text_notice_full():
    """测试完整文本通知卡片"""
    utils = TestUtils()
    
    data = {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "text_notice",
            "source": {
                "icon_url": "https://github.com/github.png",
                "desc": "农连通数据分析",
                "desc_color": "#FF6B6B"
            },
            "main_title": {
                "title": "📊 辣椒价格预警",
                "desc": "价格波动较大，请关注市场变化"
            },
            "emphasis_content": {
                "title": "涨幅最大",
                "desc": "红彩椒涨幅达150%"
            },
            "sub_title_text": "数据更新时间：2025-06-20 14:30",
            "horizontal_content_list": [
                {
                    "keyname": "小米椒",
                    "value": "7.9元/斤"
                },
                {
                    "keyname": "红彩椒",
                    "value": "2.25元/斤"
                },
                {
                    "keyname": "黄彩椒",
                    "value": "2.2元/斤"
                }
            ],
            "jump_list": [
                {
                    "type": 1,
                    "title": "查看详细报告",
                    "url": "https://example.com/detail-report"
                },
                {
                    "type": 1,
                    "title": "历史数据",
                    "url": "https://example.com/history"
                }
            ],
            "card_action": {
                "type": 1,
                "url": "https://example.com/main"
            }
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_news_notice():
    """测试图文展示卡片"""
    utils = TestUtils()
    
    data = {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "news_notice",
            "source": {
                "icon_url": "https://github.com/github.png",
                "desc": "市场分析"
            },
            "main_title": {
                "title": "📈 农产品市场周报",
                "desc": "本周农产品价格走势分析"
            },
            "card_image": {
                "url": "https://mdn.alipayobjects.com/one_clip/afts/img/ARV_R4C8ygYAAAAATMAAAAgAoEACAQFr/original",
                "aspect_ratio": 1.6
            },
            "image_text_area": {
                "type": 1,
                "url": "https://example.com/weekly-report",
                "title": "点击查看完整报告",
                "desc": "包含详细的价格分析和市场预测"
            },
            "vertical_content_list": [
                {
                    "title": "重点关注",
                    "desc": "彩椒类价格大幅上涨"
                },
                {
                    "title": "趋势预测",
                    "desc": "预计下周价格将趋于稳定"
                }
            ]
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_card_with_action_menu():
    """测试带操作菜单的卡片"""
    utils = TestUtils()
    
    data = {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "text_notice",
            "source": {
                "icon_url": "https://github.com/github.png",
                "desc": "系统通知"
            },
            "action_menu": {
                "desc": "更多操作",
                "action_list": [
                    {
                        "text": "查看详情",
                        "type": "view",
                        "url": "https://example.com/detail"
                    },
                    {
                        "text": "分享报告",
                        "type": "view",
                        "url": "https://example.com/share"
                    }
                ]
            },
            "main_title": {
                "title": "🔧 系统维护通知",
                "desc": "系统将进行例行维护"
            },
            "emphasis_content": {
                "title": "维护时间",
                "desc": "今晚22:00-24:00"
            }
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_minimal_card():
    """测试最简卡片（仅包含必需字段）"""
    utils = TestUtils()
    
    data = {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "text_notice"
        }
    }
    
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
        ("简单文本通知卡片", test_text_notice_simple),
        ("完整文本通知卡片", test_text_notice_full),
        ("图文展示卡片", test_news_notice),
        ("带操作菜单的卡片", test_card_with_action_menu),
        ("最简卡片", test_minimal_card),
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