"""
测试“不存在”基元与维度跃迁
严格遵循：维度跃迁必须由NOT_EXIST连续自乘生成
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.unclosed_number import UnclosedNumber

def test_not_exist():
    print("=== 测试“不存在”基元与维度跃迁 ===\n")
    
    # 1. 创建“不存在”基元
    not_exist = UnclosedNumber.not_exist()
    print(f"不存在基元: {not_exist}")
    assert not_exist.anchor == 0
    assert not_exist.known_terms == []
    assert not_exist.gap_depth == 0
    print("✅ 不存在基元创建成功\n")
    
    # 2. 第一次自乘：一维存在（1）
    one_dim = not_exist.self_mul()
    print(f"一维存在: {one_dim}")
    assert one_dim.anchor == 1
    assert one_dim.known_terms == [1], f"一维应为 [1]，实际为 {one_dim.known_terms}"
    assert one_dim.gap_depth == 1
    print("✅ 一维跃迁成功\n")
    
    # 3. 第二次自乘：二维存在（30）
    two_dim = not_exist.self_mul().self_mul()  # 从不存在开始，连续两次
    print(f"二维存在: {two_dim}")
    assert two_dim.anchor == 1
    assert two_dim.known_terms == [30], f"二维应为 [30]，实际为 {two_dim.known_terms}"
    assert two_dim.gap_depth == 1
    print("✅ 二维跃迁成功\n")
    
    # 4. 第三次自乘：三维存在（396）
    three_dim = not_exist.self_mul().self_mul().self_mul()  # 连续三次
    print(f"三维存在: {three_dim}")
    assert three_dim.anchor == 1
    assert three_dim.known_terms == [396], f"三维应为 [396]，实际为 {three_dim.known_terms}"
    assert three_dim.gap_depth == 1
    print("✅ 三维跃迁成功\n")
    
    print("="*50)
    print("🎉 所有测试通过！维度谱生成逻辑正确：")
    print("   不存在 → 自乘1次 → 一维 (1)")
    print("   不存在 → 自乘2次 → 二维 (30)")
    print("   不存在 → 自乘3次 → 三维 (396)")
    print("="*50)
    
    return one_dim, two_dim, three_dim

if __name__ == "__main__":
    test_not_exist()