"""
utils.py
通用工具函数
"""

import os
import json
import yaml
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime
import mpmath as mp

def ensure_directories(directories: List[str] = None) -> None:
    """
    确保必要的目录存在
    
    参数:
        directories: 目录列表，如果为None则使用默认列表
    """
    if directories is None:
        directories = [
            'data',
            'results',
            'figures',
            'logs'
        ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print(f"✅ 目录结构已创建: {directories}")

def load_config(config_file: str = "config.yaml") -> Dict[str, Any]:
    """
    加载YAML配置文件
    
    参数:
        config_file: 配置文件路径
        
    返回:
        配置字典
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"✅ 配置文件已加载: {config_file}")
        return config
    except FileNotFoundError:
        print(f"⚠️  配置文件不存在: {config_file}，使用默认配置")
        return get_default_config()
    except yaml.YAMLError as e:
        print(f"❌ 配置文件解析错误: {e}")
        return get_default_config()

def get_default_config() -> Dict[str, Any]:
    """获取默认配置"""
    return {
        'precision': {
            'dps': 50,
            'max_cf_terms': 100,
            'pslq_maxcoeff': 1000,
            'series_terms': 10
        },
        'analysis': {
            'large_quotient_threshold': 100,
            'convergence_tolerance': 1e-15,
            'save_raw_data': True
        },
        'visualization': {
            'dpi': 150,
            'figsize': [12, 8],
            'style': 'seaborn-v0_8-whitegrid',
            'save_format': 'png'
        }
    }

def save_results(data: Dict[str, Any], 
                filename: str, 
                indent: int = 2,
                ensure_ascii: bool = False) -> str:
    """
    保存结果到JSON文件
    
    参数:
        data: 要保存的数据
        filename: 文件名
        indent: JSON缩进
        ensure_ascii: 是否确保ASCII编码
        
    返回:
        保存的文件路径
    """
    # 确保results目录存在
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    
    # 如果文件名不包含路径，则添加到results目录
    if not os.path.dirname(filename):
        filename = os.path.join(results_dir, filename)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii, default=str)
    
    print(f"✅ 结果已保存到: {filename}")
    return filename

def load_results(filename: str) -> Optional[Dict[str, Any]]:
    """
    从JSON文件加载结果
    
    参数:
        filename: 文件名
        
    返回:
        加载的数据，如果失败则返回None
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 结果已加载: {filename}")
        return data
    except FileNotFoundError:
        print(f"❌ 文件不存在: {filename}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        return None

def format_number(x: Any, precision: int = 15) -> str:
    """
    格式化数字为字符串
    
    参数:
        x: 要格式化的数字
        precision: 精度
        
    返回:
        格式化后的字符串
    """
    if isinstance(x, (int, float)):
        return f"{x:.{precision}f}"
    elif isinstance(x, mp.mpf):
        return mp.nstr(x, precision)
    elif isinstance(x, str):
        try:
            # 尝试转换为数字
            num = mp.mpf(x)
            return mp.nstr(num, precision)
        except:
            return x
    else:
        return str(x)

def create_experiment_summary(results: Dict[str, Any]) -> str:
    """
    创建实验摘要字符串
    
    参数:
        results: 实验结果字典
        
    返回:
        摘要字符串
    """
    summary_lines = []
    summary_lines.append("=" * 60)
    summary_lines.append("谢尔宾斯基地毯编译指纹分析实验摘要")
    summary_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary_lines.append("=" * 60)
    
    if 'constants' in results:
        consts = results['constants']
        summary_lines.append("\n=== 核心常数 ===")
        if 'D' in consts:
            summary_lines.append(f"豪斯多夫维数 D = {format_number(consts['D'], 20)}")
        if 'S' in consts:
            summary_lines.append(f"面积 S = {format_number(consts['S'], 20)}")
    
    if 'continued_fraction' in results:
        cf = results['continued_fraction']
        if 'large_partial_quotients' in cf and cf['large_partial_quotients']:
            summary_lines.append("\n=== 巨大偏商发现 ===")
            for idx, val in cf['large_partial_quotients']:
                summary_lines.append(f"  第{idx}项: {val}")
    
    if 'algebraic_relations' in results:
        rels = results['algebraic_relations']
        summary_lines.append("\n=== 代数关系验证 ===")
        for key, rel in rels.items():
            if 'error' in rel:
                summary_lines.append(f"  {rel.get('formula', key)}: 误差 = {format_number(rel['error'], 10)}")
    
    summary_lines.append("\n=== 分析状态 ===")
    
    # 检查已完成的分析
    completed_analyses = []
    if 'constants' in results:
        completed_analyses.append("常数计算")
    if 'continued_fraction' in results:
        completed_analyses.append("连分数分析")
    if 'algebraic_relations' in results:
        completed_analyses.append("代数关系")
    if 'series_analysis' in results:
        completed_analyses.append("级数表示")
    
    for analysis in completed_analyses:
        summary_lines.append(f"✅ {analysis}")
    
    summary_lines.append("=" * 60)
    
    return "\n".join(summary_lines)

def save_experiment_summary(results: Dict[str, Any], 
                          filename: str = "experiment_summary.txt") -> str:
    """
    保存实验摘要到文件
    
    参数:
        results: 实验结果
        filename: 输出文件名
        
    返回:
        保存的文件路径
    """
    summary = create_experiment_summary(results)
    
    # 确保results目录存在
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    
    filepath = os.path.join(results_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ 实验摘要已保存到: {filepath}")
    return filepath

def get_project_root() -> str:
    """
    获取项目根目录
    
    返回:
        项目根目录路径
    """
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 向上两级到项目根目录
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    return project_root

def setup_project_environment() -> Dict[str, Any]:
    """
    设置项目环境
    
    返回:
        环境信息字典
    """
    env_info = {
        'project_root': get_project_root(),
        'current_time': datetime.now().isoformat(),
        'python_version': sys.version,
        'platform': sys.platform
    }
    
    # 创建必要的目录
    ensure_directories()
    
    # 加载配置
    config = load_config()
    env_info['config'] = config
    
    # 设置mpmath精度
    if 'precision' in config and 'dps' in config['precision']:
        mp.mp.dps = config['precision']['dps']
        env_info['mpmath_dps'] = mp.mp.dps
    
    print("=" * 60)
    print("项目环境设置完成")
    print(f"项目根目录: {env_info['project_root']}")
    print(f"Python版本: {env_info['python_version'].split()[0]}")
    print(f"计算精度: {env_info.get('mpmath_dps', 'N/A')} 位")
    print("=" * 60)
    
    return env_info

def print_table(headers: List[str], rows: List[List[Any]], 
               title: str = "", col_widths: List[int] = None) -> None:
    """
    打印表格
    
    参数:
        headers: 表头列表
        rows: 行数据列表
        title: 表格标题
        col_widths: 列宽列表
    """
    if not rows:
        return
    
    if col_widths is None:
        # 自动计算列宽
        col_widths = []
        for i, header in enumerate(headers):
            max_len = len(str(header))
            for row in rows:
                if i < len(row):
                    max_len = max(max_len, len(str(row[i])))
            col_widths.append(max_len + 2)  # 加2作为边距
    
    if title:
        print(f"\n{title}")
        print("-" * sum(col_widths))
    
    # 打印表头
    header_row = ""
    for i, header in enumerate(headers):
        width = col_widths[i] if i < len(col_widths) else 15
        header_row += f"{str(header):<{width}}"
    print(header_row)
    print("-" * sum(col_widths))
    
    # 打印数据行
    for row in rows:
        row_str = ""
        for i, cell in enumerate(row):
            width = col_widths[i] if i < len(col_widths) else 15
            row_str += f"{str(cell):<{width}}"
        print(row_str)

# 测试代码
if __name__ == "__main__":
    print("测试 utils.py 模块...")
    print("=" * 60)
    
    # 测试环境设置
    env = setup_project_environment()
    print(f"环境信息: {json.dumps(env, indent=2, default=str)}")
    
    # 测试数字格式化
    test_number = mp.mpf('1.23456789')
    print(f"\n数字格式化测试:")
    print(f"原始: {test_number}")
    print(f"格式化(10位): {format_number(test_number, 10)}")
    
    # 测试表格打印
    print("\n表格打印测试:")
    headers = ['名称', '值', '描述']
    rows = [
        ['D', '1.892789', '维数'],