"""
constants.py
定义谢尔宾斯基地毯及相关常数
"""

import mpmath as mp
from typing import Dict, Any

def compute_sierpinski_constants(dps: int = 50) -> Dict[str, Any]:
    """
    计算谢尔宾斯基地毯的主要常数
    
    参数:
        dps: 十进制计算精度
        
    返回:
        包含所有常数的字典
    """
    mp.mp.dps = dps
    
    # 核心常数
    D = mp.log(8) / mp.log(3)  # 豪斯多夫维数 D = log₃8
    S = mp.mpf(8) / mp.mpf(9)  # 面积 S = 8/9
    
    # 相关对数
    ln2 = mp.log(2)
    ln3 = mp.log(3)
    ln8 = mp.log(8)
    
    # 精确关系
    exact_relation_D = D * ln3 - ln8  # 应为0
    exact_relation_logs = 3 * ln2 - ln8  # 应为0
    
    return {
        'D': D,
        'S': S,
        'ln2': ln2,
        'ln3': ln3,
        'ln8': ln8,
        'exact_relation_D': exact_relation_D,
        'exact_relation_logs': exact_relation_logs,
 """
constants.py
定义谢尔宾斯基地毯的核心常数及相关数学常数
"""

import mpmath as mp
from typing import Dict, Any
import yaml
import os

def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

def compute_sierpinski_constants(dps: int = None) -> Dict[str, Any]:
    """
    计算谢尔宾斯基地毯的主要常数
    
    参数:
        dps: 十进制计算精度，如果为None则从配置文件读取
        
    返回:
        包含所有常数的字典
    """
    # 加载配置
    config = load_config()
    if dps is None:
        dps = config['precision']['dps']
    
    # 设置计算精度
    mp.mp.dps = dps
    
    # 1. 核心常数
    D = mp.log(8) / mp.log(3)  # 豪斯多夫维数 D = log₃8
    S = mp.mpf(8) / mp.mpf(9)  # 面积 S = 8/9
    
    # 2. 相关对数常数
    ln2 = mp.log(2)
    ln3 = mp.log(3)
    ln8 = mp.log(8)  # = 3*ln2
    
    # 3. 验证精确关系
    exact_relation_D = D * ln3 - ln8  # 理论上应为0
    exact_relation_logs = 3 * ln2 - ln8  # 理论上应为0
    
    # 4. 其他可能相关的常数
    constants_dict = {
        'D': D,
        'S': S,
        'ln2': ln2,
        'ln3': ln3,
        'ln8': ln8,
        'exact_relation_D': exact_relation_D,
        'exact_relation_logs': exact_relation_logs,
        'precision': dps
    }
    
    return constants_dict

def get_comparison_constants(dps: int = 50) -> Dict[str, Any]:
    """
    获取用于对比研究的其他数学常数
    """
    mp.mp.dps = dps
    
    return {
        'pi': mp.pi,
        'e': mp.e,
        'sqrt2': mp.sqrt(2),
        'sqrt3': mp.sqrt(3),
        'phi': (1 + mp.sqrt(5)) / 2,  # 黄金分割率
        'catalan_G': mp.mpf('0.915965594177219015054603514932'),  # 卡塔兰常数
        'precision': dps
    }

def save_constants_to_file(constants_dict: Dict[str, Any], filename: str = None):
    """
    将常数保存到文本文件
    
    参数:
        constants_dict: 常数字典
        filename: 输出文件名，如果为None则使用默认路径
    """
    if filename is None:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, "constants.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# 谢尔宾斯基地毯及相关常数\n")
        f.write(f"# 计算精度: {constants_dict.get('precision', 50)} 位十进制数字\n")
        f.write("=" * 60 + "\n\n")
        
        for name, value in constants_dict.items():
            if name != 'precision':
                f.write(f"{name:<15} = {mp.nstr(value, 30)}\n")
    
    print(f"✅ 常数已保存到: {filename}")

# 测试代码
if __name__ == "__main__":
    print("测试 constants.py 模块...")
    
    # 计算常数
    constants = compute_sierpinski_constants(30)
    
    print("\n谢尔宾斯基地毯常数:")
    print(f"维数 D = {constants['D']}")
    print(f"面积 S = {constants['S']}")
    print(f"ln2 = {constants['ln2']}")
    print(f"ln3 = {constants['ln3']}")
    print(f"ln8 = {constants['ln8']}")
    
    # 验证关系
    print(f"\n验证代数关系:")
    print(f"D * ln3 - ln8 = {constants['exact_relation_D']} (理论上应为0)")
    print(f"3*ln2 - ln8 = {constants['exact_relation_logs']} (理论上应为0)")
    
    # 保存到文件
    save_constants_to_file(constants)
    
    print("\n✅ constants.py 模块测试完成！")
    for key, value in constants.items():
        if key not in ['precision']:
            print(f"{key}: {value}")