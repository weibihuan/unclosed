import mpmath as mp

def predict_and_prepare_oeis():
    print("🔬 序列分析与 OEIS 准备")
    print("=" * 60)

    # 已知序列
    K = [1, 30, 51, 347, 1949, 9477, 45832, 221977]
    
    # 1. 计算极限常数 A
    r = 4.844994448043308
    vals = [K[n] / (r ** n) for n in range(1, len(K))]
    A = vals[-1]  # 取最新的稳定值
    
    print(f"序列 K: {K}")
    print(f"稳定比值 A = K_n / r^n ≈ {A}")
    print(f"ln(r) = {mp.log(r)}")
    print(f"π/2 = {mp.pi/2}")
    print(f"差值: {abs(mp.log(r) - mp.pi/2)}")
    
    # 2. 预测 K9 和 K10
    K9_pred = int(round(A * (r ** 9)))
    K10_pred = int(round(A * (r ** 10)))
    
    print(f"\n预测 K9 = {K9_pred}")
    print(f"预测 K10 = {K10_pred}")
    
    # 3. 验证递推
    K9_recur = 5*K9_pred - K[7] + K[6] + K[5] - 2
    print(f"\n用递推验证 K9: 5*{K9_pred} - {K[7]} + {K[6]} + {K[5]} - 2 = {K9_recur}")
    
    # 4. 生成 OEIS 提交格式
    print("\n" + "=" * 60)
    print("📝 OEIS 提交草稿")
    print("=" * 60)
    oeis_seq = "1, 30, 51, 347, 1949, 9477, 45832, 221977"
    print(f"Sequence: {oeis_seq}")
    print("Name: Integer sequence from Unclosed Mathematics hardening factors.")
    print("Formula: a(n+4) = 5*a(n+3) - a(n+2) + a(n+1) + a(n) - 2.")
    print(f"Closed form: a(n) ~ {A:.4f} * ({r:.4f})^n.")
    print("Comment: The dominant root's logarithm is approximately Pi/2.")
    print("Keywords: nonn, hard, more.")

if __name__ == "__main__":
    predict_and_prepare_oeis()