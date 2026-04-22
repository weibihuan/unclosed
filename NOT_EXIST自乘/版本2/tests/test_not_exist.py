"""
测试“不存在”基元与维度跃迁
严格遵循：连续对纯缺口自乘，生成维度谱
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.unclosed_number import UnclosedNumber

def test_not_exist():
    print("=== 测试“不存在”基元与维度跃迁 ===\n")
    
    not_exist = UnclosedNumber.not_exist()
    print(f"不存在基元: {not_exist}")
    
    # 连续自乘，每次都对纯缺口操作
    one_dim = not_exist.self_mul()          # 第一次自乘：一维
    print(f"一维存在: {one_dim}")
    assert one_dim.anchor == 0
    assert one_dim.metadata["dimension_level"] == 1
    assert one_dim.metadata["generated_value"] == 1
    
    two_dim = one_dim.self_mul()            # 第二次自乘：二维
    print(f"二维存在: {two_dim}")
    assert two_dim.anchor == 0
    assert two_dim.metadata["dimension_level"] == 2
    assert two_dim.metadata["generated_value"] == 30
    
    three_dim = two_dim.self_mul()          # 第三次自乘：三维
    print(f"三维存在: {three_dim}")
    assert three_dim.anchor == 0
    assert three_dim.metadata["dimension_level"] == 3
    assert three_dim.metadata["generated_value"] == 396
    
    print("\n✅ 所有测试通过！维度谱生成正确：1, 30, 396")
    return one_dim, two_dim, three_dim

if __name__ == "__main__":
    test_not_exist()