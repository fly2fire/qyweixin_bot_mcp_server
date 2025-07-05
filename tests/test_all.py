#!/usr/bin/env python3
"""
企业微信机器人MCP服务器测试集
运行所有消息类型的测试
"""

import os
import sys
import time
import importlib.util
from test_utils import TestUtils


def import_test_module(module_name, file_path):
    """动态导入测试模块"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_test_file(test_file, test_name):
    """运行单个测试文件"""
    print(f"\n{'='*60}")
    print(f"🧪 开始测试: {test_name}")
    print(f"📄 测试文件: {test_file}")
    print(f"{'='*60}")
    
    try:
        # 导入并运行测试模块
        module = import_test_module(test_file.replace('.py', ''), test_file)
        
        # 运行main函数
        if hasattr(module, 'main'):
            module.main()
            return True
        else:
            print(f"❌ 测试文件 {test_file} 没有main函数")
            return False
            
    except Exception as e:
        print(f"❌ 运行测试文件 {test_file} 时发生错误: {str(e)}")
        return False


def main():
    """主测试函数"""
    utils = TestUtils()
    
    # 检查配置
    if not utils.check_config():
        return
    
    # 获取测试文件列表
    test_files = [
        ("test_text.py", "文本消息测试"),
        ("test_markdown.py", "Markdown消息测试"),
        ("test_markdown_v2.py", "Markdown_v2消息测试"),
        ("test_image.py", "图片消息测试"),
        ("test_news.py", "图文消息测试"),
        ("test_template_card.py", "模板卡片消息测试"),
        ("test_utils.py", "工具函数测试"),
    ]
    
    print("🚀 企业微信机器人MCP服务器测试集")
    print("=" * 60)
    print("📋 测试计划:")
    for i, (file_name, test_name) in enumerate(test_files, 1):
        print(f"   {i}. {test_name} ({file_name})")
    
    # 检查测试文件是否存在
    missing_files = []
    for file_name, _ in test_files:
        if not os.path.exists(file_name):
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\n❌ 缺少测试文件: {', '.join(missing_files)}")
        return
    
    # 运行测试
    results = []
    start_time = time.time()
    
    for file_name, test_name in test_files:
        success = run_test_file(file_name, test_name)
        results.append((test_name, success))
        
        # 测试间隔
        if file_name != test_files[-1][0]:  # 不是最后一个测试
            print(f"\n⏳ 等待5秒后继续下一个测试...")
            time.sleep(5)
    
    # 总结
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print("📊 测试总结")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"⏱️  总用时: {duration:.2f}秒")
    print(f"📈 通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    # 详细结果
    print("\n📋 详细结果:")
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"   {status} {test_name}")
    
    if passed == total:
        print(f"\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败")
        print("💡 建议检查失败的测试和配置")


if __name__ == "__main__":
    main() 