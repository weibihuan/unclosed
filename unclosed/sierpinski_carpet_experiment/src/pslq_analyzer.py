"""
pslq_analyzer.py
PSLQ整数关系分析工具
"""

import mpmath as mp
from mpmath import pslq
from typing import List, Dict, Any, Optional, Union
import json
import os
from .constants import compute_sierpinski_constants

def analyze_pslq_relations(values: List[mp.mpf], 
                          names: Optional[List[str]] = None,
                          maxcoeff: int = 1000,
                          tol: float = 1e-10) -> Dict[str, Any]:
    """
    使用PSLQ分析数值向量间的整数线性关系
    
    参数:
        values: 数值向量 [x1, x2, ..., xn]
        names: 对应名称，可选
        maxcoeff: 最大系数绝对值
        tol: 容差
        
    返回:
        分析结果字典
    """
    if len(values) < 2:
        return {
            'error': '向量长度至少为2',
            'found_relation': False
        }
    
    if names is None:
        names = [f'x{i}' for i in range(len(values))]
    
    if len(values) != len(names):
        return {
            'error': 'values和names长度不一致',
            'found_relation': False
        }
    
    result = {
        'input_values': [mp.nstr(v, 20) for v in values],
        'input_names': names,
        'maxcoeff': maxcoeff,
        'tolerance': tol,
        'found_relation': False
    }
    
    # 执行PSLQ
    try:
        coefficients = pslq(values, maxcoeff=maxcoeff, tol=tol)
    except Exception as e:
        result['error'] = f"PSLQ计算错误: {str(e)}"
        return result
    
    if coefficients is None:
        result['message'] = "未发现整数线性关系"
        return result
    
    # 计算残差
    residual = sum(c * v for c, v in zip(coefficients, values))
    residual_abs = abs(residual)
    
    # 转换为整数
    int_coefficients = [int(c) for c in coefficients]
    
    result.update({
        'found_relation': True,
        'coefficients': int_coefficients,
        'coefficients_float': [float(c) for c in coefficients],
        'residual': mp.nstr(residual, 20),
        'residual_abs': mp.nstr(residual_abs, 20),
        'residual_float': float(residual_abs)
    })
    
    # 构造可读的关系式
    terms = []
    for coef, name in zip(int_coefficients, names):
        if coef != 0:
            sign = '+' if coef > 0 else '-'
            abs_coef = abs(coef) if abs(coef) != 1 else ''
            term = f"{sign} {abs_coef}{name}".strip()
            terms.append(term)
    
    if terms:
        relation_str = ' '.join(terms)
        if relation_str.startswith('+ '):
            relation_str = relation_str[2:]
        relation_str += " = 0"
        result['relation_string'] = relation_str
    
    return result

def analyze_dimension_relations(dps: int = 50, maxcoeff: int = 1000) -> Dict[str, Any]:
    """
    分析维数D的特定关系
    
    参数:
        dps: 计算精度
        maxcoeff: 最大系数
        
    返回:
        分析结果字典
    """
    from .constants import compute_sierpinski_constants
    
    # 计算常数
    constants = compute_sierpinski_constants(dps)
    D = constants['D']
    ln2 = constants['ln2']
    ln3 = constants['ln3']
    ln8 = constants['ln8']
    
    print(f"分析维数 D 的整数线性关系...")
    print(f"计算精度: {dps} 位")
    print(f"最大系数: {maxcoeff}")
    print("-" * 50)
    
    all_results = {}
    
    # 1. 分析 D 与对数的关系
    print("\n1. 分析 D 与 ln2, ln3, ln8 的关系:")
    basis1 = [mp.mpf(1), D, ln2, ln3, ln8]
    names1 = ['1', 'D', 'ln2', 'ln3', 'ln8']
    result1 = analyze_pslq_relations(basis1, names1, maxcoeff)
    all_results['D_log_relation'] = result1
    
    if result1['found_relation']:
        print(f"   发现关系: {result1.get('relation_string', 'N/A')}")
        print(f"   系数: {result1['coefficients']}")
        print(f"   残差: {result1['residual_abs']}")
    else:
        print("   未发现简单整数关系")
    
    # 2. 分析纯对数关系
    print("\n2. 分析纯对数关系 (ln2, ln3, ln8):")
    basis2 = [mp.mpf(1), ln2, ln3, ln8]
    names2 = ['1', 'ln2', 'ln3', 'ln8']
    result2 = analyze_pslq_relations(basis2, names2, maxcoeff)
    all_results['log_relations'] = result2
    
    if result2['found_relation']:
        print(f"   发现关系: {result2.get('relation_string', 'N/A')}")
        print(f"   系数: {result2['coefficients']}")
        print(f"   残差: {result2['residual_abs']}")
    else:
        print("   未发现简单整数关系")
    
    # 3. 理论关系验证
    print("\n3. 理论关系验证:")
    print(f"   D = ln8/ln3 = {mp.nstr(D, 20)}")
    print(f"   D * ln3 - ln8 = {mp.nstr(D*ln3 - ln8, 20)} (理论上应为0)")
    print(f"   3*ln2 - ln8 = {mp.nstr(3*ln2 - ln8, 20)} (理论上应为0)")
    
    # 4. 保存结果
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    result_filename = os.path.join(results_dir, "pslq_analysis.json")
    with open(result_filename, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n✅ PSLQ分析结果已保存到: {result_filename}")
    
    return all_results

def save_pslq_results(results: Dict[str, Any], 
                     filename: str = "pslq_analysis.json") -> str:
    """
    保存PSLQ分析结果
    
    参数:
        results: 分析结果字典
        filename: 输出文件名
        
    返回:
        保存的文件路径
    """
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    filepath = os.path.join(results_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    return filepath

# 测试代码
if __name__ == "__main__":
    print("测试 pslq_analyzer.py 模块...")
    print("=" * 60)
    
    # 测试维数D的PSLQ分析
    results = analyze_dimension_relations(dps=30, maxcoeff=100)
    
    print("\n" + "=" * 60)
    print("✅ pslq_analyzer.py 模块测试完成！")
    保存PSLQ分析结果
    """
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"PSLQ分析结果已保存到: {filename}")