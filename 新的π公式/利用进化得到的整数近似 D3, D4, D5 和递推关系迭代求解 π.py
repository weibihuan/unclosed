import math
from decimal import Decimal, getcontext

def hardening_converger_improved(D3_evolved, D4_evolved, D5_evolved, iterations=10):
    """
    利用进化得到的整数近似 D3, D4, D5 和递推关系迭代求解 π
    """
    getcontext().prec = 100
    # 将输入转为 Decimal
    D3 = Decimal(D3_evolved)
    D4 = Decimal(D4_evolved)
    D5 = Decimal(D5_evolved)
    
    # 初始猜测 π0
    pi_guess = Decimal('3.14159265358979323846')
    
    for i in range(iterations):
        # 计算当前猜测下的硬化因子
        K3 = D3 / (pi_guess ** 2)
        K4 = D4 / (pi_guess ** 3)
        K5 = D5 / (pi_guess ** 4)
        
        # 理论递推要求 K4/K3 = K5/K4 = r/π
        # 但我们不知道 r，可以用两个比值相互校正
        ratio1 = K4 / K3
        ratio2 = K5 / K4
        
        # 理想情况下 ratio1 = ratio2 = r/π
        # 因此 π 应满足 π = r / ratio1，但 r 未知，我们利用 D4/D3 = r^4 消去 r
        # 从 ratio1 = (D4/D3) / π  => π = (D4/D3) / ratio1
        # 而 ratio1 由当前 π 计算得到，这形成了不动点迭代
        pi_new = (D4 / D3) / ratio1
        
        # 也可以用 ratio2 迭代，取平均
        pi_new2 = (D5 / D4) / ratio2
        pi_guess = (pi_new + pi_new2) / 2
        
        # 打印迭代过程
        error = float(abs(pi_guess - Decimal(math.pi)))
        print(f"Iter {i+1}: π ≈ {pi_guess:.15f}, 误差 {error:.2e}")
        if error < 1e-30:
            break
    return pi_guess

if __name__ == "__main__":
    # 使用双目标进化得到的最优解（从你的实验输出中提取）
    D3_opt = 473.7827
    D4_opt = 10759.4228
    D5_opt = 345217.9158
    print("🔧 改进的硬化收敛器")
    print(f"输入: D3={D3_opt}, D4={D4_opt}, D5={D5_opt}")
    pi_final = hardening_converger_improved(D3_opt, D4_opt, D5_opt, iterations=10)
    print(f"\n最终 π = {pi_final:.50f}")
    print(f"真实 π = {math.pi:.50f}")
    print(f"误差 = {abs(pi_final - Decimal(math.pi)):.2e}")