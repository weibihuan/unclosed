#!/usr/bin/env python3
"""
run_simple_analysis.py
简化版分析脚本 - 可以直接运行
"""

import sys
import os
import json
from datetime import datetime

print("=" * 60)
print("谢尔宾斯基地毯简化分析脚本")
print("=" * 60)

# 第一步：检查是否在正确目录
if not os.path.exists('src'):
    print("❌ 错误：请在项目根目录（Sierpinski_Experiment/）中运行此脚本")
    print(f"当前目录：{os.getcwd()}")
    print("请运行：cd /path/to/Sierpinski_Experiment")
    sys.exit(1)

# 添加项目根目录到Python路径
sys.path.append('.')

# 第二步：导入模块
try:
    import mpmath as mp
    print(f"✅ mpmath 导入成功")
except ImportError:
    print("❌ 错误：未安装 mpmath")
    print("请运行：pip install mpmath")
    sys.exit(1)

# 第三步：定义简单函数（避免复杂导入）
def compute_constants_simple(dps=30):
    """简化版常数计算"""
    mp.dps = dps
    
    D = mp.log(8) / mp.log(3)  # 维数 D = log₃8
    S = mp.mpf(8) / mp.mpf(9)  # 面积 S = 8/9
    ln2 = mp.log(2)
    ln3 = mp.log(3)
    ln8 = mp.log(8)
    
    return {
        'D': D,
        'S': S,
        'ln2': ln2,
        'ln3': ln3,
        'ln8': ln8
    }

def continued_fraction_simple(x, max_terms=100):
    """简化版连分数计算"""
    cf = []
    for _ in range(max_terms):
        a = int(mp.floor(x))
        cf.append(a)
        x = x - a
        if x == 0:
            break
        x = 1 / x
    return cf

# 第四步：执行分析
print("\n📊 开始分析...")
print("-" * 40)

# 计算常数
constants = compute_constants_simple(30)
D = constants['D']
S = constants['S']
ln2 = constants['ln2']
ln3 = constants['ln3']
ln8 = constants['ln8']

print(f"维数 D = {mp.nstr(D, 20)}")
print(f"面积 S = {mp.nstr(S, 20)}")

# 计算连分数
cf_D = continued_fraction_simple(D, 100)
print(f"\n连分数长度：{len(cf_D)} 项")
print(f"前20项：{cf_D[:20]}")

# 寻找巨大偏商
large_terms = []
for i, val in enumerate(cf_D):
    if val > 100:
        large_terms.append((i, val))

if large_terms:
    print(f"\n🎯 发现巨大偏商（>100）：")
    for idx, val in large_terms:
        print(f"  第{idx}项: {val}")
else:
    print(f"\n❌ 未发现巨大偏商（>100）")
    
    # 查看最大值
    max_val = max(cf_D)
    max_idx = cf_D.index(max_val)
    print(f"最大偏商：第{max_idx}项的{max_val}")

# 验证代数关系
print(f"\n🔍 代数关系验证：")
relation1 = D * ln3 - ln8
relation2 = 3 * ln2 - ln8
print(f"D * ln3 - ln8 = {mp.nstr(relation1, 20)} (应为0)")
print(f"3*ln2 - ln8 = {mp.nstr(relation2, 20)} (应为0)")

# 第五步：保存结果
print(f"\n💾 保存结果...")

# 创建results目录
os.makedirs('results', exist_ok=True)

# 保存简单结果
result_file = 'results/simple_analysis.txt'
with open(result_file, 'w', encoding='utf-8') as f:
    f.write("谢尔宾斯基地毯简化分析结果\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("核心常数：\n")
    f.write(f"  维数 D = {mp.nstr(D, 30)}\n")
    f.write(f"  面积 S = {mp.nstr(S, 30)}\n\n")
    
    f.write("连分数分析：\n")
    f.write(f"  总项数：{len(cf_D)}\n")
    f.write(f"  前20项：{cf_D[:20]}\n")
    
    if large_terms:
        f.write(f"  巨大偏商（>100）：\n")
        for idx, val in large_terms:
            f.write(f"    第{idx}项: {val}\n")
    else:
        f.write(f"  未发现巨大偏商（>100）\n")
        f.write(f"  最大偏商：第{cf_D.index(max(cf_D))}项的{max(cf_D)}\n")
    
    f.write("\n代数关系验证：\n")
    f.write(f"  D = ln8/ln3 误差：{mp.nstr(abs(relation1), 20)}\n")
    f.write(f"  ln8 = 3*ln2 误差：{mp.nstr(abs(relation2), 20)}\n")

print(f"✅ 分析完成！结果已保存到：{result_file}")
print("=" * 60)