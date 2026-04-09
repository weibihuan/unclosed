#!/usr/bin/env python3
"""
run_full_analysis.py
完整分析脚本：执行所有分析模块
"""

import sys
import os
import json
import yaml
import mpmath as mp
from datetime import datetime

def setup_environment():
    """设置运行环境"""
    print("=" * 60)
    print("谢尔宾斯基地毯完整分析脚本")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 检查是否在项目根目录
    if not os.path.exists('src'):
        print("❌ 错误：请在项目根目录（Sierpinski_Experiment/）中运行")
        print(f"当前目录: {os.getcwd()}")
        print("请运行: cd /path/to/Sierpinski_Experiment")
        return False
    
    # 添加项目根目录到Python路径
    sys.path.insert(0, os.getcwd())
    
    # 创建必要的目录
    os.makedirs('results', exist_ok=True)
    os.makedirs('figures', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    return True

def load_config():
    """加载配置文件"""
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"❌ 加载配置文件失败: {e}")
        print("使用默认配置...")
        return {
            'precision': {'dps': 50, 'max_cf_terms': 100},
            'analysis': {'large_quotient_threshold': 100}
        }

def run_step(step_name, step_func, *args, **kwargs):
    """运行分析步骤并计时"""
    from time import time
    start_time = time()
    print(f"\n▶ 开始步骤: {step_name}")
    print("-" * 40)
    
    try:
        result = step_func(*args, **kwargs)
        elapsed = time() - start_time
        print(f"✅ 步骤完成: {step_name} ({elapsed:.2f}秒)")
        return result
    except Exception as e:
        elapsed = time() - start_time
        print(f"❌ 步骤失败: {step_name} ({elapsed:.2f}秒)")
        print(f"错误信息: {e}")
        return None

def step1_compute_constants(config):
    """步骤1：计算常数"""
    dps = config['precision']['dps']
    
    # 设置精度
    mp.mp.dps = dps
    
    # 计算常数
    D = mp.log(8) / mp.log(3)  # 维数
    S = mp.mpf(8) / mp.mpf(9)  # 面积
    
    ln2 = mp.log(2)
    ln3 = mp.log(3)
    ln8 = mp.log(8)
    
    print(f"计算精度: {dps} 位")
    print(f"维数 D = {mp.nstr(D, 20)}")
    print(f"面积 S = {mp.nstr(S, 20)}")
    print(f"ln2 = {mp.nstr(ln2, 20)}")
    print(f"ln3 = {mp.nstr(ln3, 20)}")
    print(f"ln8 = {mp.nstr(ln8, 20)}")
    
    # 保存常数到文件
    constants_data = {
        'D': mp.nstr(D, dps),
        'S': mp.nstr(S, dps),
        'ln2': mp.nstr(ln2, dps),
        'ln3': mp.nstr(ln3, dps),
        'ln8': mp.nstr(ln8, dps),
        'precision': dps,
        'calculation_time': datetime.now().isoformat()
    }
    
    with open('data/constants.json', 'w', encoding='utf-8') as f:
        json.dump(constants_data, f, indent=2, ensure_ascii=False)
    
    with open('data/constants.txt', 'w', encoding='utf-8') as f:
        f.write("# 谢尔宾斯基地毯常数\n")
        f.write("=" * 50 + "\n\n")
        for key, value in constants_data.items():
            if key not in ['precision', 'calculation_time']:
                f.write(f"{key}: {value}\n")
    
    return constants_data

def step2_continued_fraction_analysis(config, constants):
    """步骤2：连分数分析"""
    max_terms = config['precision']['max_cf_terms']
    threshold = config['analysis']['large_quotient_threshold']
    
    D = mp.mpf(constants['D'])
    
    print(f"计算连分数 (最大{max_terms}项)")
    print(f"巨大偏商阈值: {threshold}")
    
    # 计算连分数
    cf = []
    x = D
    for _ in range(max_terms):
        a = int(mp.floor(x))
        cf.append(a)
        x = x - a
        if x == 0:
            break
        x = 1 / x
    
    # 寻找巨大偏商
    large_terms = []
    for i, val in enumerate(cf):
        if val > threshold:
            large_terms.append((i, val))
    
    print(f"连分数长度: {len(cf)} 项")
    print(f"前20项: {cf[:20]}")
    
    if large_terms:
        print(f"发现巨大偏商(>{threshold}):")
        for idx, val in large_terms:
            print(f"  第{idx}项: {val}")
    else:
        print(f"未发现巨大偏商(>{threshold})")
    
    # 计算渐近分数
    convergents = []
    h0, h1 = 0, 1
    k0, k1 = 1, 0
    for i, a in enumerate(cf[:20]):  # 只计算前20个渐近分数
        h = a * h1 + h0
        k = a * k1 + k0
        if k != 0:
            value = mp.mpf(h) / mp.mpf(k)
            convergents.append({
                'index': i + 1,
                'fraction': f"{h}/{k}",
                'value': mp.nstr(value, 15),
                'error': mp.nstr(abs(value - D), 10)
            })
        h0, h1 = h1, h
        k0, k1 = k1, k
    
    # 保存结果
    cf_data = {
        'continued_fraction': cf,
        'large_partial_quotients': large_terms,
        'convergents': convergents,
        'statistics': {
            'length': len(cf),
            'max': max(cf) if cf else 0,
            'min': min(cf) if cf else 0,
            'sum': sum(cf)
        }
    }
    
    with open('results/continued_fraction_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(cf_data, f, indent=2, ensure_ascii=False, default=str)
    
    # 保存原始连分数
    with open('data/cf_dimension_100_terms.txt', 'w', encoding='utf-8') as f:
        f.write("# 维数D的连分数前100项\n")
        f.write("# 格式: 索引,值\n")
        for i, val in enumerate(cf[:100]):
            f.write(f"{i},{val}\n")
    
    return cf_data

def step3_algebraic_relations(constants):
    """步骤3：代数关系分析"""
    D = mp.mpf(constants['D'])
    ln2 = mp.mpf(constants['ln2'])
    ln3 = mp.mpf(constants['ln3'])
    ln8 = mp.mpf(constants['ln8'])
    
    print("验证代数关系:")
    print("-" * 30)
    
    # 理论关系
    relation1 = D * ln3 - ln8  # 应为0
    relation2 = 3 * ln2 - ln8  # 应为0
    
    relations = {
        'D_eq_ln8_over_ln3': {
            'formula': 'D = ln8 / ln3',
            'computed': mp.nstr(D, 20),
            'expected': mp.nstr(ln8/ln3, 20),
            'error': mp.nstr(abs(relation1), 20)
        },
        'ln8_eq_3ln2': {
            'formula': 'ln8 = 3 * ln2',
            'computed': mp.nstr(ln8, 20),
            'expected': mp.nstr(3*ln2, 20),
            'error': mp.nstr(abs(relation2), 20)
        }
    }
    
    for key, rel in relations.items():
        print(f"{rel['formula']}:")
        print(f"  计算值: {rel['computed']}")
        print(f"  理论值: {rel['expected']}")
        print(f"  误差: {rel['error']}")
    
    with open('results/algebraic_relations.json', 'w', encoding='utf-8') as f:
        json.dump(relations, f, indent=2, ensure_ascii=False)
    
    return relations

def step4_generate_summary(config, constants, cf_data, relations):
    """步骤4：生成分析摘要"""
    summary = {
        'analysis_time': datetime.now().isoformat(),
        'config': config,
        'constants': constants,
        'continued_fraction': {
            'length': cf_data.get('statistics', {}).get('length', 0),
            'large_partials_count': len(cf_data.get('large_partial_quotients', [])),
            'large_partials': cf_data.get('large_partial_quotients', [])
        },
        'algebraic_relations': relations
    }
    
    # 保存JSON摘要
    with open('results/full_analysis_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    
    # 保存文本摘要
    with open('results/full_analysis_summary.txt', 'w', encoding='utf-8') as f:
        f.write("谢尔宾斯基地毯完整分析摘要\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("1. 核心常数\n")
        f.write("-" * 40 + "\n")
        f.write(f"维数 D = {constants['D']}\n")
        f.write(f"面积 S = {constants['S']}\n\n")
        
        f.write("2. 连分数分析\n")
        f.write("-" * 40 + "\n")
        f.write(f"总项数: {summary['continued_fraction']['length']}\n")
        
        large_parts = summary['continued_fraction']['large_partials']
        if large_parts:
            f.write(f"巨大偏商(>100): {len(large_parts)} 个\n")
            for idx, val in large_parts:
                f.write(f"  第{idx}项: {val}\n")
        else:
            f.write("未发现巨大偏商(>100)\n")
        f.write("\n")
        
        f.write("3. 代数关系验证\n")
        f.write("-" * 40 + "\n")
        for key, rel in relations.items():
            f.write(f"{rel['formula']}: 误差 = {rel['error']}\n")
        
        f.write("\n4. 分析配置\n")
        f.write("-" * 40 + "\n")
        f.write(f"计算精度: {config['precision']['dps']} 位\n")
        f.write(f"连分数最大项数: {config['precision']['max_cf_terms']}\n")
    
    return summary

def main():
    """主函数"""
    # 设置环境
    if not setup_environment():
        return
    
    # 加载配置
    config = load_config()
    
    # 执行所有分析步骤
    constants = run_step("计算常数", step1_compute_constants, config)
    cf_data = run_step("连分数分析", step2_continued_fraction_analysis, config, constants)
    relations = run_step("代数关系分析", step3_algebraic_relations, constants)
    summary = run_step("生成摘要", step4_generate_summary, config, constants, cf_data, relations)
    
    # 最终输出
    print("\n" + "=" * 60)
    print("✅ 完整分析完成！")
    print("=" * 60)
    
    print("\n📁 生成的文件:")
    print("  data/constants.json - 常数数据")
    print("  data/constants.txt - 常数文本")
    print("  data/cf_dimension_100_terms.txt - 连分数原始数据")
    print("  results/continued_fraction_analysis.json - 连分数分析")
    print("  results/algebraic_relations.json - 代数关系")
    print("  results/full_analysis_summary.json - JSON摘要")
    print("  results/full_analysis_summary.txt - 文本摘要")
    
    if cf_data and 'large_partial_quotients' in cf_data:
        large_terms = cf_data['large_partial_quotients']
        if large_terms:
            print(f"\n🎯 关键发现: 发现 {len(large_terms)} 个巨大偏商")
            for idx, val in large_terms:
                print(f"  第{idx}项: {val}")
    
    print(f"\n⏱️ 总耗时: 请查看各步骤计时")
    print("=" * 60)

if __name__ == "__main__":
    main()