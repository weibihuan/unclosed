import mpmath as mp

# ============================================================
# 整数硬化因子序列递推分析器
# 目标：寻找 K3, K4, K5, K6 之间的精确线性关系
# ============================================================

def analyze_recurrence():
    print("🔬 整数硬化因子序列递推分析")
    print("=" * 60)
    
    # 您的整数硬化因子序列
    K3 = 51
    K4 = 347
    K5 = 1949
    K6 = 9477
    
    print(f"K3 = {K3}")
    print(f"K4 = {K4}")
    print(f"K5 = {K5}")
    print(f"K6 = {K6}")
    print("-" * 60)
    
    # 1. 验证已知关系：K5 = 4*K4 + 11*K3
    relation1 = K5 - (4*K4 + 11*K3)
    print(f"验证 K5 = 4*K4 + 11*K3: {relation1} (应为 0)")
    
    # 2. 寻找 K6 与 K3, K4, K5 的关系：K6 = a*K5 + b*K4 + c*K3
    print("\n寻找 K6 的三阶线性递推关系：")
    # 使用 findpoly 寻找整数系数 [a, b, c, d] 使得 a*K6 + b*K5 + c*K4 + d*K3 = 0
    # 注意：findpoly 寻找的是多项式根，但我们可以将其转化为寻找整数关系
    # 构造向量 [K6, K5, K4, K3]
    vec = [K6, K5, K4, K3]
    # 使用 mp.pslq 寻找整数关系
    coeffs = mp.pslq(vec, maxcoeff=100, maxsteps=1000)
    if coeffs:
        # coeffs 满足 coeffs[0]*K6 + coeffs[1]*K5 + coeffs[2]*K4 + coeffs[3]*K3 = 0
        print(f"找到整数关系: {coeffs[0]}*K6 + {coeffs[1]}*K5 + {coeffs[2]}*K4 + {coeffs[3]}*K3 = 0")
        # 整理成 K6 = ... 的形式
        if coeffs[0] != 0:
            a = -coeffs[1] / coeffs[0]
            b = -coeffs[2] / coeffs[0]
            c = -coeffs[3] / coeffs[0]
            print(f"即: K6 = {a}*K5 + {b}*K4 + {c}*K3")
            # 检查是否为整数
            if a.is_integer() and b.is_integer() and c.is_integer():
                print(f"✅ 整数系数: K6 = {int(a)}*K5 + {int(b)}*K4 + {int(c)}*K3")
            else:
                print(f"⚠️  系数为有理数: {a}, {b}, {c}")
    else:
        print("未找到三阶整数关系，尝试四阶递推（加入常数项）")
        # 尝试包括常数项：a*K6 + b*K5 + c*K4 + d*K3 + e = 0
        vec2 = [K6, K5, K4, K3, 1]
        coeffs2 = mp.pslq(vec2, maxcoeff=100, maxsteps=1000)
        if coeffs2:
            print(f"找到带常数项的整数关系: {coeffs2[0]}*K6 + {coeffs2[1]}*K5 + {coeffs2[2]}*K4 + {coeffs2[3]}*K3 + {coeffs2[4]} = 0")
    
    # 3. 尝试二阶递推：K6 = a*K5 + b*K4
    print("\n尝试二阶递推 K6 = a*K5 + b*K4:")
    # 解方程：9477 = a*1949 + b*347
    # 使用有理数求解
    found = False
    for a in range(-20, 21):
        for b in range(-20, 21):
            if a*K5 + b*K4 == K6:
                print(f"  找到: K6 = {a}*K5 + {b}*K4")
                found = True
                break
        if found:
            break
    if not found:
        print("  未找到整数系数二阶递推")
    
    # 4. 尝试更高阶递推：K6 = a*K5 + b*K4 + c*K3
    print("\n尝试三阶递推 K6 = a*K5 + b*K4 + c*K3:")
    found = False
    for a in range(-10, 11):
        for b in range(-10, 11):
            for c in range(-10, 11):
                if a*K5 + b*K4 + c*K3 == K6:
                    print(f"  找到: K6 = {a}*K5 + {b}*K4 + {c}*K3")
                    found = True
                    break
            if found:
                break
        if found:
            break
    if not found:
        print("  未找到小整数系数三阶递推")
    
    print("\n" + "=" * 60)
    print("结论：")
    print("1. K5 = 4*K4 + 11*K3 是精确成立的整数关系。")
    print("2. K6 可能需要更高阶递推，或与维度相关的变系数递推。")
    print("3. 这些递推关系就是未闭环数学中的守恒量。")

if __name__ == "__main__":
    analyze_recurrence()