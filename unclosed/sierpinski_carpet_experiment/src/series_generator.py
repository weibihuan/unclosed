"""
series_generator.py
级数表示生成与分析工具
"""

import mpmath as mp
from typing import List, Dict, Any, Callable, Optional
import json
import os
import numpy as np
from math import factorial

def geometric_series_for_S(terms: int = 10) -> List[Dict[str, Any]]:
    """
    为面积S=8/9生成几何级数表示
    
    参数:
        terms: 级数项数
        
    返回:
        级数表示列表
    """
    S = mp.mpf(8) / mp.mpf(9)  # 目标值
    representations = []
    
    # 表示1: 十进制展开
    decimal_sum = mp.mpf('0')
    decimal_terms = []
    errors_decimal = []
    
    for n in range(1, terms + 1):
        term = mp.mpf(8) / (10**n)
        decimal_sum += term
        decimal_terms.append(float(term))
        error = abs(decimal_sum - S)
        errors_decimal.append(float(error))
    
    representations.append({
        'name': '十进制展开',
        'formula': r'$S = \sum_{n=1}^{\infty} \frac{8}{10^n}$',
        'partial_sum': float(decimal_sum),
        'target_value': float(S),
        'error': float(abs(decimal_sum - S)),
        'terms': decimal_terms,
        'errors': errors_decimal,
        'base': 10,
        'convergence_rate': '几何收敛 (1/10)'
    })
    
    # 表示2: 基于9的几何级数
    geometric_sum = mp.mpf('0')
    geometric_terms = []
    errors_geometric = []
    
    for n in range(1, terms + 1):
        term = mp.mpf(8) / (9**n)
        geometric_sum += term
        geometric_terms.append(float(term))
        error = abs(geometric_sum - S)
        errors_geometric.append(float(error))
    
    representations.append({
        'name': '9的幂级数',
        'formula': r'$S = \sum_{n=1}^{\infty} \frac{8}{9^n}$',
        'partial_sum': float(geometric_sum),
        'target_value': float(S),
        'error': float(abs(geometric_sum - S)),
        'terms': geometric_terms,
        'errors': errors_geometric,
        'base': 9,
        'convergence_rate': '几何收敛 (1/9)'
    })
    
    # 表示3: 交错级数表示
    alternating_sum = mp.mpf('0')
    alternating_terms = []
    errors_alternating = []
    
    for n in range(terms):
        term = mp.mpf(8) * ((-1)**n) / (9**(n+1))
        alternating_sum += term
        alternating_terms.append(float(term))
        error = abs(alternating_sum - S)
        errors_alternating.append(float(error))
    
    representations.append({
        'name': '交错级数',
        'formula': r'$S = \sum_{n=0}^{\infty} \frac{8(-1)^n}{9^{n+1}}$',
        'partial_sum': float(alternating_sum),
        'target_value': float(S),
        'error': float(abs(alternating_sum - S)),
        'terms': alternating_terms,
        'errors': errors_alternating,
        'base': 9,
        'convergence_rate': '交错几何收敛 (1/9)'
    })
    
    # 表示4: 二项式展开
    binomial_sum = mp.mpf('0')
    binomial_terms = []
    errors_binomial = []
    
    for n in range(terms):
        # 广义二项式系数 C(1, n) = 1*(1-1)*...*(1-n+1)/n!
        coeff = mp.mpf(1)
        for k in range(n):
            coeff *= (1 - k)
        coeff /= factorial(n)
        term = coeff * ((-1/9)**n)
        binomial_sum += term
        binomial_terms.append(float(term))
        error = abs(binomial_sum - S)
        errors_binomial.append(float(error))
    
    representations.append({
        'name': '二项式展开',
        'formula': r'$S = (1 - \frac{1}{9}) = \sum_{n=0}^{\infty} \binom{1}{n} (-\frac{1}{9})^n$',
        'partial_sum': float(binomial_sum),
        'target_value': float(S),
        'error': float(abs(binomial_sum - S)),
        'terms': binomial_terms,
        'errors': errors_binomial,
        'base': 9,
        'convergence_rate': '泰勒展开'
    })
    
    return representations

def factorial_series_for_D(base: int = 166, terms: int = 5) -> Dict[str, Any]:
    """
    尝试为维数D构造阶乘比级数（拉马努金式）
    
    参数:
        base: 级数底数
        terms: 级数项数
        
    返回:
        级数表示字典
    """
    D = mp.log(8) / mp.log(3)  # 目标值
    
    # 尝试形式: Σ (an+b) * (阶乘比) / base^n
    sum_val = mp.mpf('0')
    series_terms = []
    errors = []
    
    for n in range(terms):
        # 使用中心二项式系数 (2n)!/(n!)^2
        binom = factorial(2*n) // (factorial(n)**2)
        term = mp.mpf(binom) / (mp.mpf(base)**n)
        sum_val += term
        series_terms.append(float(term))
        error = abs(sum_val - D)
        errors.append(float(error))
    
    return {
        'name': f'阶乘比级数 (底数{base})',
        'formula': r'$D \approx \sum_{n=0}^{\infty} \frac{(2n)!}{(n!)^2} \cdot \frac{1}{' + str(base) + r'^n}$',
        'partial_sum': float(sum_val),
        'target_value': float(D),
        'error': float(abs(sum_val - D)),
        'terms': series_terms,
        'errors': errors,
        'base': base,
        'convergence_rate': '尝试性构造'
    }

def ramanujan_style_series(constant: mp.mpf, 
                          base_candidates: List[int] = None,
                          max_terms: int = 5) -> List[Dict[str, Any]]:
    """
    尝试构造拉马努金式快速收敛级数
    
    参数:
        constant: 目标常数
        base_candidates: 候选底数列表
        max_terms: 最大项数
        
    返回:
        级数表示列表
    """
    if base_candidates is None:
        base_candidates = [166, 260, 396, 9801]  # 常见拉马努金底数
    
    representations = []
    target_value = float(constant)
    
    for base in base_candidates:
        # 尝试不同的阶乘组合
        for factorial_type in ['double', 'quadruple']:
            sum_val = mp.mpf('0')
            terms = []
            errors = []
            
            for n in range(max_terms):
                if factorial_type == 'double':
                    # 使用 (4n)!/(n!)^4
                    num = factorial(4*n) if 4*n <= 170 else 1e100  # 避免大数溢出
                    den = factorial(n)**4
                    coeff = mp.mpf(num) / mp.mpf(den) if den != 0 else mp.mpf(0)
                else:  # 'quadruple'
                    # 使用 (2n)!/(n!)^2
                    num = factorial(2*n) if 2*n <= 170 else 1e100
                    den = factorial(n)**2
                    coeff = mp.mpf(num) / mp.mpf(den) if den != 0 else mp.mpf(0)
                
                # 线性系数尝试
                linear_coeff = mp.mpf(1103 + 26390*n)  # 拉马努金经典系数
                
                term = linear_coeff * coeff / (mp.mpf(base)**n)
                sum_val += term
                terms.append(float(term))
                error = abs(sum_val - constant)
                errors.append(float(error))
            
            factorial_name = '(4n)!/(n!)^4' if factorial_type == 'double' else '(2n)!/(n!)^2'
            
            representations.append({
                'name': f'拉马努金式 (底数{base}, {factorial_name})',
                'formula': f'$ \\approx \\sum \\frac{{(an+b) \\cdot {factorial_name}}}{{{base}^n}}$',
                'partial_sum': float(sum_val),
                'target_value': target_value,
                'error': float(abs(sum_val - constant)),
                'terms': terms,
                'errors': errors,
                'base': base,
                'factorial_type': factorial_type
            })
    
    return representations

def analyze_series_efficiency(series_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析级数表示的收敛效率
    
    参数:
        series_list: 级数表示列表
        
    返回:
        效率分析结果
    """
    if not series_list:
        return {}
    
    analysis = {
        'series_count': len(series_list),
        'efficiency_ranking': [],
        'best_series': None,
        'convergence_stats': {}
    }
    
    # 对每个级数计算收敛效率指标
    for series in series_list:
        if 'errors' in series and series['errors']:
            errors = series['errors']
            final_error = errors[-1] if errors else float('inf')
            
            # 计算收敛速率
            if len(errors) > 1:
                convergence_ratio = errors[-1] / errors[-2] if errors[-2] > 0 else 0
            else:
                convergence_ratio = 0
            
            # 计算达到特定精度所需的项数估计
            terms_to_precision = {}
            for precision in [1e-5, 1e-10, 1e-15]:
                terms_needed = next((i+1 for i, err in enumerate(errors) if err < precision), None)
                terms_to_precision[f'terms_to_{precision}'] = terms_needed
            
            efficiency_score = {
                'name': series.get('name', '未知'),
                'final_error': final_error,
                'convergence_ratio': convergence_ratio,
                'base': series.get('base', 0),
                'terms_to_precision': terms_to_precision,
                'formula': series.get('formula', '')
            }
            
            analysis['efficiency_ranking'].append(efficiency_score)
    
    # 按最终误差排序
    analysis['efficiency_ranking'].sort(key=lambda x: x['final_error'])
    
    # 选择最佳级数
    if analysis['efficiency_ranking']:
        analysis['best_series'] = analysis['efficiency_ranking'][0]
    
    # 计算收敛统计
    if analysis['efficiency_ranking']:
        errors = [s['final_error'] for s in analysis['efficiency_ranking'] if s['final_error'] > 0]
        if errors:
            analysis['convergence_stats'] = {
                'min_error': min(errors),
                'max_error': max(errors),
                'mean_error': np.mean(errors),
                'median_error': np.median(errors)
            }
    
    return analysis

def save_series_analysis(series_data: Dict[str, Any], 
                        filename: str = "series_analysis.json") -> str:
    """
    保存级数分析结果
    
    参数:
        series_data: 级数分析数据
        filename: 输出文件名
        
    返回:
        保存的文件路径
    """
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    filepath = os.path.join(results_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(series_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✅ 级数分析结果已保存到: {filepath}")
    return filepath

# 测试代码
if __name__ == "__main__":
    print("测试 series_generator.py 模块...")
    print("=" * 60)
    
    # 测试面积S的级数表示
    print("1. 面积S的级数表示:")
    s_series = geometric_series_for_S(terms=5)
    for series in s_series:
        print(f"  {series['name']}: 部分和={series['partial_sum']:.10f}, 误差={series['error']:.2e}")
    
    # 测试维数D的级数表示
    print("\n2. 维数D的尝试级数:")
    D = mp.log(8) / mp.log(3)
    d_series = ramanujan_style_series(D, [166, 260], 3)
    for series in d_series:
        print(f"  {series['name']}: 部分和={series['partial_sum']:.10f}, 误差={series['error']:.2e}")
    
    # 分析效率
    print("\n3. 级数效率分析:")
    all_series = s_series + d_series
    efficiency = analyze_series_efficiency(all_series)
    
    if efficiency.get('best_series'):
        best = efficiency['best_series']
        print(f"  最佳级数: {best['name']}")
        print(f"  最终误差: {best['final_error']:.2e}")
        print(f"  收敛比: {best['convergence_ratio']:.3f}")
    
    print("\n" + "=" * 60)
    print("✅ series_generator.py 模块测试完成！")