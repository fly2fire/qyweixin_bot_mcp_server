#!/usr/bin/env python3
"""
测试 Markdown_v2 消息类型
"""

from test_utils import TestUtils


def test_simple_markdown_v2():
    """测试简单的markdown_v2消息"""
    utils = TestUtils()
    
    data = {
        "msgtype": "markdown_v2",
        "markdown_v2": {
            "content": "# 测试标题\n\n这是一个简单的**markdown_v2**测试消息\n\n- 列表项1\n- 列表项2"
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_table_markdown_v2():
    """测试包含表格的markdown_v2消息"""
    utils = TestUtils()
    
    content = """# 价格测试表格

| 品类 | 起始价 | 最新价 | 涨跌幅 |
|------|-------|-------|-------|
| 苹果 | 5.0 | 5.5 | +10% |
| 香蕉 | 3.0 | 2.8 | -7% |
| 橙子 | 4.0 | 4.2 | +5% |

测试完成 ✅"""
    
    data = {
        "msgtype": "markdown_v2",
        "markdown_v2": {
            "content": content
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_complex_markdown_v2():
    """测试复杂的markdown_v2消息（包含图片、代码块、分割线等）"""
    utils = TestUtils()
    
    content = """# 复杂Markdown_v2测试

## 基本格式
**粗体文本** 和 *斜体文本*

## 代码块
```python
def hello():
    print("Hello, World!")
```

## 分割线
---

## 图片
![测试图片](https://mdn.alipayobjects.com/one_clip/afts/img/ARV_R4C8ygYAAAAATMAAAAgAoEACAQFr/original)

## 表格
| 功能 | 状态 |
|------|------|
| 表格 | ✅ |
| 图片 | ✅ |
| 代码块 | ✅ |

## 引用
> 这是一个引用文本

## 链接
[访问GitHub](https://github.com)

测试完成！"""
    
    data = {
        "msgtype": "markdown_v2",
        "markdown_v2": {
            "content": content
        }
    }
    
    result = utils.send_message(data)
    return result["success"]


def test_pepper_report():
    """测试辣椒价格报告（用户原始数据）"""
    utils = TestUtils()
    
    content = """辣椒价格走势分析报告
2025年6月6日-6月20日

价格总览
| 品类 | 起始价 | 最高价 | 最新价 | 涨跌幅 |
|---|---|---|---|---|
| 小米椒 | 8.5 | 8.5 | 7.9 | -7.1% |
| 精品尖椒 | 1.55 | 2.0 | 2.0 | +29.0% |
| 红彩椒 | 0.9 | 2.25 | 2.25 | +150.0% |
| 黄彩椒 | 1.0 | 2.2 | 2.2 | +120.0% |

价格走势图
![辣椒价格走势图](https://mdn.alipayobjects.com/one_clip/afts/img/ARV_R4C8ygYAAAAATMAAAAgAoEACAQFr/original)

关键时间点价格(元/斤)
| 日期 | 小米椒 | 精品尖椒 | 红彩椒 | 黄彩椒 |
|---|---|---|---|---|
| 6月6日 | 8.5 | 1.55 | 0.9 | 1.0 |
| 6月13日 | 8.5 | 1.8 | 1.75 | 1.8 |
| 6月17日 | 7.5 | 1.9 | 2.05 | 2.0 |
| 6月20日 | 7.9 | 2.0 | 2.25 | 2.2 |

市场趋势分析
1. 除小米椒外，其他品类均明显上涨
2. 彩椒价格涨幅最大，均超100%
3. 小米椒价格较高但近期回落
4. 精品尖椒涨幅温和，走势稳定

数据来源：农连通（上海）数字科技有限公司
分析报告：bot@农连通（上海）数字科技有限公司"""
    
    data = {
        "msgtype": "markdown_v2",
        "markdown_v2": {
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
        ("简单Markdown_v2消息", test_simple_markdown_v2),
        ("表格Markdown_v2消息", test_table_markdown_v2),
        ("复杂Markdown_v2消息", test_complex_markdown_v2),
        ("辣椒价格报告", test_pepper_report),
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