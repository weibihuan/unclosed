import mpmath as mp

# ============================================================
# 硬化因子序列终极关系搜索（修正版）
# 目标：全面搜索 K3, K4, K5, K6 之间的精确整数关系
# ============================================================

def search_relations():
    print("🔬 硬化因子序列终极关系搜索")
    print("=" * 60)
    
    K1 = 1
    K2 = 30
    K3 = 51
    K4 = 347
    K5 = 1949
    K6 = 9477
    
    print(f"序列: K1={K1}, K2={K2}, K3={K3}, K4={K4}, K5={K5}, K6={K6}")
    print("-" * 60)
    
    # 1. 验证已知的 K5 关系
    print("1. 验证 K5 关系:")
    rel1 = K5 - (4*K4 + 11*K3)
    print(f"   4*K4 + 11*K3 = {4*K4 + 11*K3}")
    print(f"   K5 = {K5}")
    print(f"   差值 = {rel1} (应为 0)")
    
    # 2. 搜索 K6 与 K5, K4, K3 的非齐次线性递推（包含常数项）
    print("\n2. 搜索 K6 的非齐次线性递推（含常数项）:")
    # 寻找 a, b, c, d 使得 a*K6 + b*K5 + c*K4 + d*K3 + e = 0
    vec = [K6, K5, K4, K3, 1]  # 加入常数项 1
    coeffs = mp.pslq(vec, maxcoeff=1000, maxsteps=2000)
    if coeffs:
        # coeffs[0]*K6 + coeffs[1]*K5 + coeffs[2]*K4 + coeffs[3]*K3 + coeffs[4] = 0
        print(f"   找到整数关系: {coeffs[0]}*K6 + {coeffs[1]}*K5 + {coeffs[2]}*K4 + {coeffs[3]}*K3 + {coeffs[4]} = 0")
        if coeffs[0] != 0:
            a = -coeffs[1] / coeffs[0]
            b = -coeffs[2] / coeffs[0]
            c = -coeffs[3] / coeffs[0]
            d = -coeffs[4] / coeffs[0]
            print(f"   即: K6 = {a}*K5 + {b}*K4 + {c}*K3 + {d}")
            if all(mp.isint(a) and mp.isint(b) and mp.isint(c) and mp.isint(d)):
                print(f"   ✅ 整数系数: K6 = {int(a)}*K5 + {int(b)}*K4 + {int(c)}*K3 + {int(d)}")
        else:
            print("   ⚠️ 首项系数为0，关系不包含 K6 的独立项")
    else:
        print("   未找到非齐次线性递推")
    
    # 3. 搜索包含 K2 的四阶递推
    print("\n3. 搜索包含 K2 的四阶递推:")
    vec2 = [K6, K5, K4, K3, K2, 1]
    coeffs2 = mp.pslq(vec2, maxcoeff=1000, maxsteps=2000)
    if coeffs2:
        print(f"   找到四阶关系: {coeffs2[0]}*K6 + {coeffs2[1]}*K5 + {coeffs2[2]}*K4 + {coeffs2[3]}*K3 + {coeffs2[4]}*K2 + {coeffs2[5]} = 0")
    else:
        print("   未找到四阶递推")
    
    # 4. 尝试二次关系：K6 = a*K5^2 + b*K4 + c
    print("\n4. 尝试二次关系（K6 = a*K5^2 + b*K4 + c）:")
    # 由于 K5^2 很大，a 可能很小
    found = False
    for a in [-2, -1, 0, 1, 2]:
        for b in range(-20, 21):
            for c in range(-20, 21):
                if a*K5*K5 + b*K4 + c == K6:
                    print(f"   找到: K6 = {a}*K5^2 + {b}*K4 + {c}")
                    found = True
                    break
            if found:
                break
        if found:
            break
    if not found:
        print("   未找到小整数系数的二次关系")
    
    # 5. 与数学常数的关系
    print("\n5. 搜索与数学常数 (π, e) 的线性关系:")
    constants = [mp.pi, mp.e, mp.sqrt(2), mp.phi]
    const_names = ['π', 'e', '√2', 'φ']
    for const, name in zip(constants, const_names):
        vec_const = [K3, K4, K5, K6, const]
        coeffs_c = mp.pslq(vec_const, maxcoeff=1000, maxsteps=2000)
        if coeffs_c:
            print(f"   与 {name} 的关系: {coeffs_c[0]}*K3 + {coeffs_c[1]}*K4 + {coeffs_c[2]}*K5 + {coeffs_c[3]}*K6 + {coeffs_c[4]}*{name} = 0")
    
    # 6. 对数差分（检查等比性）
    print("\n6. 对数差分（检查是否等比数列）:")
    seq = [K1, K2, K3, K4, K5, K6]
    ratios = [seq[i+1]/seq[i] for i in range(len(seq)-1)]
    log_diffs = [mp.log(r) for r in ratios]
    print(f"   比值: {ratios}")
    print(f"   对数差值: {log_diffs}")
    # 检查对数差值是否恒定
    is_geometric = all(abs(log_diffs[i] - log_diffs[0]) < 1e-10 for i in range(len(log_diffs)))
    print(f"   是否为等比数列? {is_geometric}")
    
    print("\n" + "=" * 60)
    print("结论:")
    print("1. K5 = 4*K4 + 11*K3 是精确的整数守恒量。")
    print("2. K6 可能需要非齐次递推（含常数项）或更高阶递推。")
    print("3. 这些递推关系构成了未闭环数学中的守恒定律。")

if __name__ == "__main__":
    search_relations()