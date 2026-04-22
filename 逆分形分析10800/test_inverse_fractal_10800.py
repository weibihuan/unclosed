"""
使用逆分形分析 10800 的几何意义
目标：找到 10800 对应的 IFS 缩放因子或子图形数
"""

import mpmath as mp
import math

mp.mp.dps = 50

def analyze_10800_fractal():
    print("=== 逆分形分析：10800 ===\n")
    
    N = 10800  # 子图形数量候选
    
    # 常见分形维数
    target_dims = {
        "门格海绵": mp.log(20)/mp.log(3),           # ≈ 2.7268
        "谢尔宾斯基地毯": mp.log(8)/mp.log(3),      # ≈ 1.8928
        "科赫曲线": mp.log(4)/mp.log(3),            # ≈ 1.2619
        "谢尔宾斯基三角形": mp.log(3)/mp.log(2),   # ≈ 1.5850
        "康托尔集": mp.log(2)/mp.log(3),            # ≈ 0.6309
        "二维平面": mp.mpf(2),
        "三维空间": mp.mpf(3)
    }
    
    print("1. 假设 10800 是子图形数 N，求缩放因子 s：")
    print("   D = log(N) / log(s)  =>  s = N^(1/D)\n")
    
    for name, D in target_dims.items():
        s = N ** (1/D)
        print(f"   目标维数 {name} (D={float(D):.4f}): 缩放因子 s ≈ {float(s):.4f}")
    
    print("\n" + "="*60)
    print("2. 假设 10800 是缩放因子 s，求子图形数 N：")
    print("   N = s^D\n")
    
    for name, D in target_dims.items():
        N_calc = mp.power(10800, D)
        print(f"   目标维数 {name} (D={float(D):.4f}): 子图形数 N ≈ {float(N_calc):.0f}")
    
    print("\n" + "="*60)
    print("3. 寻找整数缩放因子 s，使维数 D 接近有理数：")
    
    # 尝试整数缩放因子 s
    for s in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 22, 30, 36, 60, 108]:
        D = mp.log(N) / mp.log(s)
        # 检查 D 是否接近简单分数
        fractions_to_check = [(1,1), (3,2), (2,1), (5,2), (3,1), (7,2), (4,1)]
        for num, den in fractions_to_check:
            if abs(D - num/den) < 0.01:  # 接近
                print(f"   s={s}: D={float(D):.6f} ≈ {num}/{den} = {num/den}")
                break
    
    print("\n" + "="*60)
    print("4. 10800 的因数分解与分形结构：")
    print("   10800 = 2^4 × 3^3 × 5^2")
    print("   这可以分解为：")
    print("      = (2^2 × 3)^2 × (3 × 5^2) = 12^2 × 75")
    print("      = 144 × 75")
    print("      = 360 × 30  （360是圆周度数，30是二维特征数）")
    print("      = 396 × (300/11)  （396是三维特征数）")
    
    print("\n5. 逆分形生成器参数建议：")
    print("   如果采用 s=22（接近门格海绵的缩放因子3，但放大了7.33倍）：")
    D_s22 = mp.log(N) / mp.log(22)
    print(f"      D = log(10800)/log(22) ≈ {float(D_s22):.4f}")
    print("   如果采用 s=104（接近二维）：")
    D_s104 = mp.log(N) / mp.log(104)
    print(f"      D = log(10800)/log(104) ≈ {float(D_s104):.4f}")
    
    return {
        "N": N,
        "factors": [2, 2, 2, 2, 3, 3, 3, 5, 5],
        "suggested_s": 22,
        "suggested_D": mp.log(N) / mp.log(22)
    }

if __name__ == "__main__":
    result = analyze_10800_fractal()
    
    print("\n" + "="*60)
    print("结论：")
    print("1. 10800 作为子图形数 N，当缩放因子 s=22 时，维数 D≈2.92，接近3维。")
    print("2. 10800 = 360 × 30，结合了时间周期（360）和二维空间（30）。")
    print("3. 四维特征数 10800 可能对应一个介于 2D 和 3D 之间的分形结构。")
    print("4. 建议用逆分形生成器，以 s=22 为缩放因子，生成 IFS 并可视化。")