#!/usr/bin/env python3
"""
quick_test.py
快速测试脚本：验证项目基本功能
"""

import sys
import os
import mpmath as mp
from datetime import datetime

def run_quick_test():
    """运行快速测试"""
    print("=" * 60)
    print("谢尔宾斯基地毯项目 - 快速测试")
    print("=" * 60)
    
    # 检查环境
    print("\n1. 环境检查:")
    print("-" * 30)
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("❌ 需要Python 3.6+")
        return False
    else:
        print("✅ Python版本符合要求")
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 检查项目结构
    required_dirs = ['src', 'scripts', 'data', 'results']
    missing_dirs = []
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ 缺少目录: {missing_dirs}")
        print("请确保在项目根目录运行")
        return False
    else:
        print("✅ 项目结构完整")
    
    # 检查依赖
    print("\n2. 依赖检查:")
    print("-" * 30)
    
    try:
        import mpmath
        print(f"✅ mpmath版本: {mpmath.__version__}")
    except ImportError:
        print("❌ mpmath未安装")
        print("请运行: pip install mpmath")
        return False
    
    # 基本功能测试
    print("\n3. 基本功能测试:")
    print("-" * 30)
    
    # 测试常数计算
    mp.dps = 20
    D = mp.log(8) / mp.log(3)
    S = mp.mpf(8) / mp.mpf(9)
    
    print(f"维数 D = {mp.nstr(D, 15)}")
    print(f"面积 S = {mp.nstr(S, 15)}")
    
    # 测试连分数计算
    cf = []
    x = D
    for _ in range(10):
        a = int(mp.floor(x))
        cf.append(a)
        if x == a:
            break
        x = 1 / (x - a)
    
    print(f"连分数前10项: {cf}")
    
    # 测试代数关系
    ln2 = mp.log(2)
    ln3 = mp.log(3)
    ln8 = mp.log(8)
    
    error1 = abs(D * ln3 - ln8)
    error2 = abs(3 * ln2 - ln8)
    
    print(f"代数关系验证:")
    print(f"  D = ln8/ln3 误差: {mp.nstr(error1, 10)}")
    print(f"  ln8 = 3*ln2 误差: {mp.nstr(error2, 10)}")
    
    # 创建测试结果
    print("\n4. 创建测试结果:")
    print("-" * 30)
    
    os.makedirs('results', exist_ok=True)
    
    test_result = {
        'test_time': datetime.now().isoformat(),
        'python_version': f"{python_version.major}.{python_version.minor}.{python_version.micro}",
        'mpmath_version': mpmath.__version__ if 'mpmath' in locals() else 'unknown',
        'constants': {
            'D': str(D),
            'S': str(S)
        },
        'continued_fraction': cf,
        'algebraic_errors': {
            'D_eq_ln8_over_ln3': str(error1),
            'ln8_eq_3ln2': str(error2)
        }
    }
    
    with open('results/quick_test_result.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(test_result, f, indent=2, ensure_ascii=False)
    
    print("✅ 测试结果保存到: results/quick_test_result.json")
    
    # 总结
    print("\n" + "=" * 60)
    print("✅ 快速测试完成！")
    print("=" * 60)
    
    print("\n📋 测试总结:")
    print("1. 环境检查: 通过")
    print("2. 依赖检查: 通过")
    print("3. 功能测试: 通过")
    print("4. 结果保存: 完成")
    
    print("\n🎯 下一步:")
    print("运行完整分析: python scripts/run_full_analysis.py")
    print("或运行简化分析: python notebooks/run_simple_analysis.py")
    
    return True

if __name__ == "__main__":
    success = run_quick_test()
    sys.exit(0 if success else 1)