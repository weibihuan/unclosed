"""
continued_fraction.py
连分数分析工具：计算、统计、指纹识别
"""

import mpmath as mp
from typing import List, Tuple, Dict, Any
import json
import os
import numpy as np

def continued_fraction(x: mp.mpf, max_terms: int = 100) -> List[int]:
    """
    计算实数x的连分数展开
    
    参数:
        x: 目标实数
        max_terms: 最大项数
        
    返回:
        连分数系数列表 [a0; a1, a2, ...]
    """
    cf = []
    for _ in range(max_terms):
        a = int(mp.floor(x))
        cf.append(a)
        x = x - a
        if x == 0:
            break
        x = 1 / x
    return cf

def find_large_partial_quotients(cf: List[int], threshold: int = 100) -> List[Tuple[int, int]]:
    """
    寻找连分数中的巨大偏商
    
    参数:
        cf: 连分数系数列表
        threshold: 巨大偏商阈值
        
    返回:
        [(索引, 偏商), ...] 列表，索引从0开始
    """
    return [(i, a) for i, a in enumerate(cf) if a > threshold]

def compute_convergents(cf: List[int], max_convergents: int = 20) -> List[Dict[str, Any]]:
    """
    计算连分数的渐近分数（最佳有理逼近）
    
    参数:
        cf: 连分数系数列表
        max_convergents: 最大收敛子数量
        
    返回:
        收敛子信息列表
    """
    h0, h1 = 0, 1
    k0, k1 = 1, 0
    convergents = []
    
    for i, a in enumerate(cf[:max_convergents]):
        h = a * h1 + h0
        k = a * k1 + k0
        
        if k == 0:
            continue
            
        value = mp.mpf(h) / mp.mpf(k)
        convergents.append({
            'index': i + 1,
            'numerator': h,
            'denominator': k,
            'value': value,
            'coefficient': a,
            'h_k': f"{h}/{k}"
        })
        
        h0, h1 = h1, h
        k0, k1 = k1, k
    
    return convergents

def analyze_cf_statistics(cf: List[int]) -> Dict[str, Any]:
    """
    分析连分数的统计特征
    
    参数:
        cf: 连分数系数列表
        
    返回:
        统计信息字典
    """
    if not cf:
        return {}
    
    cf_array = np.array(cf, dtype=float)
    
    # 基本统计
    stats = {
        'length': len(cf),
        'mean': float(np.mean(cf_array)),
        'std': float(np.std(cf_array)),
        'min': int(np.min(cf_array)),
        'max': int(np.max(cf_array)),
        'median': float(np.median(cf_array)),
        'q1': float(np.percentile(cf_array, 25)),
        'q3': float(np.percentile(cf_array, 75)),
        'sum': int(np.sum(cf_array))
    }
    
    # Khinchin相关统计
    positive_terms = cf_array[cf_array > 0]
    if len(positive_terms) > 0:
        stats['geometric_mean'] = float(np.exp(np.mean(np.log(positive_terms))))
        stats['harmonic_mean'] = float(len(positive_terms) / np.sum(1.0 / positive_terms))
    
    # 大偏商统计
    large_terms = cf_array[cf_array > 100]
    stats['large_terms_count'] = len(large_terms)
    stats['large_terms_indices'] = [int(i) for i in np.where(cf_array > 100)[0]]
    stats['large_terms_values'] = [int(val) for val in large_terms]
    
    return stats

def save_cf_analysis(cf: List[int], 
                    large_terms: List[Tuple[int, int]], 
                    convergents: List[Dict[str, Any]], 
                    stats: Dict[str, Any],
                    filename_prefix: str = "cf_analysis",
                    target_name: str = "D") -> None:
    """
    保存连分数分析结果到文件
    
    参数:
        cf: 连分数系数列表
        large_terms: 巨大偏商列表
        convergents: 渐近分数列表
        stats: 统计信息
        filename_prefix: 文件名前缀
        target_name: 目标常数名称
    """
    # 确定输出目录
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. 保存原始连分数
    cf_filename = os.path.join(data_dir, f"{filename_prefix}_terms.txt")
    with open(cf_filename, 'w', encoding='utf-8') as f:
        f.write(f"# {target_name} 的连分数系数\n")
        f.write(f"# 总项数: {len(cf)}\n")
        f.write("#" * 50 + "\n")
        for i, a in enumerate(cf):
            f.write(f"{i:4d}: {a}\n")
    
    # 2. 保存统计信息
    stats_filename = os.path.join(results_dir, f"{filename_prefix}_statistics.json")
    with open(stats_filename, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    # 3. 保存收敛子
    conv_filename = os.path.join(results_dir, f"{filename_prefix}_convergents.txt")
    with open(conv_filename, 'w', encoding='utf-8') as f:
        f.write(f"# {target_name} 的最佳有理逼近（前{len(convergents)}个）\n")
        f.write("序号 | 分数 h/k | 近似值 | 误差 | 系数\n")
        f.write("-" * 60 + "\n")
        
        for conv in convergents:
            # 计算误差（相对于目标值的误差）
            error_str = "N/A"
            f.write(f"{conv['index']:4d} | {conv['h_k']:>10} | {mp.nstr(conv['value'], 12):<15} | {error_str:>10} | {conv['coefficient']}\n")
    
    # 4. 保存巨大偏商
    if large_terms:
        large_filename = os.path.join(results_dir, f"{filename_prefix}_large_terms.txt")
        with open(large_filename, 'w', encoding='utf-8') as f:
            f.write(f"# {target_name} 的巨大偏商（>100）\n")
            f.write("#" * 40 + "\n")
            for idx, val in large_terms:
                f.write(f"第 {idx:3d} 项: {val}\n")
    
    print(f"✅ 连分数分析结果已保存:")
    print(f"   原始数据: {cf_filename}")
    print(f"   统计信息: {stats_filename}")
    print(f"   收敛子: {conv_filename}")
    if large_terms:
        print(f"   巨大偏商: {large_filename}")

def analyze_dimension_cf(dps: int = 50, max_terms: int = 100) -> Dict[str, Any]:
    """
    分析维数D的连分数特征（主函数）
    """
    from .constants import compute_sierpinski_constants
    
    # 计算常数
    constants = compute_sierpinski_constants(dps)
    D = constants['D']
    
    print(f"分析维数 D = log₃8 的连分数指纹...")
    print(f"计算精度: {dps} 位")
    print(f"最大项数: {max_terms}")
    print("-" * 50)
    
    # 计算连分数
    cf_D = continued_fraction(D, max_terms)
    
    # 寻找巨大偏商
    large_terms = find_large_partial_quotients(cf_D, 100)
    
    # 计算渐近分数
    convergents = compute_convergents(cf_D, 12)
    
    # 统计特征
    stats = analyze_cf_statistics(cf_D)
    
    # 显示结果
    print(f"前20项: {cf_D[:20]}")
    print(f"总项数: {len(cf_D)}")
    print(f"最大值: {stats['max']}")
    
    if large_terms:
        print(f"\n🎯 发现巨大偏商（>100）:")
        for idx, val in large_terms:
            print(f"  第{idx}项: {val}")
    else:
        print(f"\n❌ 未发现巨大偏商（>100）")
    
    print(f"\n📊 统计特征:")
    print(f"  平均值: {stats['mean']:.4f}")
    print(f"  标准差: {stats['std']:.4f}")
    print(f"  中位数: {stats['median']:.4f}")
    
    # 保存结果
    save_cf_analysis(cf_D, large_terms, convergents, stats, "cf_dimension", "D")
    
    return {
        'cf': cf_D,
        'large_terms': large_terms,
        'convergents': convergents,
        'stats': stats,
        'D': D
    }

# 测试代码
if __name__ == "__main__":
    print("测试 continued_fraction.py 模块...")
    print("=" * 60)
    
    # 测试维数D的分析
    result = analyze_dimension_cf(dps=30, max_terms=50)
    
    print("\n" + "=" * 60)
    print("✅ continued_fraction.py 模块测试完成！")
            f.write(f"{conv['index']:4d} | {conv['numerator']:6d}/{conv['denominator']:6d} | "
                   f"{mp.nstr(conv['value'], 12)} | {conv['coefficient']}\n")
    
    print(f"连分数分析结果已保存，前缀: {filename_prefix}")