import random
import math
from decimal import Decimal, getcontext

# ============================================================
# 1. 六维进化预测
# ============================================================

class SixDimIndividual:
    def __init__(self):
        self.factors = [random.uniform(1.0, 50.0) for _ in range(6)]
        
    def mutate(self):
        idx = random.randint(0, 5)
        self.factors[idx] *= random.uniform(0.95, 1.05)
        self.factors[idx] = max(0.1, min(100.0, self.factors[idx]))
        
    def crossover(self, other):
        child1 = SixDimIndividual()
        child2 = SixDimIndividual()
        split = random.randint(1, 5)
        child1.factors = self.factors[:split] + other.factors[split:]
        child2.factors = other.factors[:split] + self.factors[split:]
        return child1, child2

def evaluate_six_dim(ind):
    val = 1.0
    history = [val]
    for i in range(6):
        val *= ind.factors[i]
        history.append(val)
    return history  # [D1, D2, D3, D4, D5, D6]

def fitness_six_dim(ind):
    history = evaluate_six_dim(ind)
    D3, D4, D5, D6 = history[2], history[3], history[4], history[5]
    
    K3 = D3 / (math.pi ** 2)
    K4 = D4 / (math.pi ** 3)
    K5 = D5 / (math.pi ** 4)
    K6 = D6 / (math.pi ** 5)
    
    # 奖励所有硬化因子接近整数
    deviation = (abs(K3 - round(K3)) + abs(K4 - round(K4)) +
                 abs(K5 - round(K5)) + abs(K6 - round(K6)))
    
    # 奖励 D3 和 D4 接近结构解（但不是强制，因为整数化更重要）
    deviation += 0.01 * (abs(D3 - 473.78) + abs(D4 - 10759.42))
    
    return deviation  # 越小越好

# ============================================================
# 2. 拉马努金级数高精度验证
# ============================================================

def ramanujan_test(d3_param, iterations=5):
    print(f"🧪 拉马努金级数测试：D3 = {d3_param}")
    getcontext().prec = 80
    C = Decimal(2) * Decimal(2).sqrt() / Decimal(9801)
    total = Decimal(0)
    for k in range(iterations):
        term = Decimal(math.factorial(4*k)) * (Decimal(1103 + 26390*k)) / (Decimal(math.factorial(k))**4 * Decimal(d3_param)**(4*k))
        total += term
    pi_estimate = 1 / (C * total)
    pi_true = Decimal(str(math.pi))
    error = abs(pi_estimate - pi_true)
    print(f"   迭代 {iterations} 次结果: {pi_estimate}")
    print(f"   误差: {error}")
    return error

# ============================================================
# 3. 精细结构常数关联分析
# ============================================================

def analyze_fine_structure(d3_list):
    alpha_inv = 137.036
    print("\n🔍 精细结构常数关联分析:")
    for name, d3 in d3_list.items():
        ratio = d3 / alpha_inv
        print(f"   {name}: D3={d3:.2f} -> D3/α⁻¹ = {ratio:.6f}")

# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("🌌 未闭环数学 · 终极验证")
    print("=" * 70)
    
    # --- 第一部分：六维预测 ---
    print("🚀 阶段一：预测 D6 与 K6 的整数性")
    population = [SixDimIndividual() for _ in range(500)]
    best_deviation = float('inf')
    best_history = []
    
    for gen in range(1000):
        scores = [(ind, fitness_six_dim(ind)) for ind in population]
        scores.sort(key=lambda x: x[1])
        
        if scores[0][1] < best_deviation:
            best_deviation = scores[0][1]
            best_history = evaluate_six_dim(scores[0][0])
        
        if gen % 100 == 0:
            print(f"Gen {gen:04d} | Best Dev: {best_deviation:.6f} | D3:{best_history[2]:.2f}, D6:{best_history[5]:.2f}")
        
        elite = [ind for ind, _ in scores[:50]]
        new_pop = elite[:]
        while len(new_pop) < 500:
            p1, p2 = random.sample(elite, 2)
            c1, c2 = p1.crossover(p2)
            c1.mutate(); c2.mutate()
            new_pop.extend([c1, c2])
        population = new_pop[:500]
    
    print("\n🎯 六维预测结果:")
    D3, D4, D5, D6 = best_history[2], best_history[3], best_history[4], best_history[5]
    K3, K4, K5, K6 = D3/math.pi**2, D4/math.pi**3, D5/math.pi**4, D6/math.pi**5
    print(f"   D3={D3:.4f}, D4={D4:.4f}, D5={D5:.4f}, D6={D6:.4f}")
    print(f"   K3={K3:.4f} (≈{round(K3)}), K4={K4:.4f} (≈{round(K4)}), K5={K5:.4f} (≈{round(K5)}), K6={K6:.4f} (≈{round(K6)})")
    
    # --- 第二部分：拉马努金验证 ---
    print("\n🚀 阶段二：拉马努金级数高精度验证")
    ramanujan_test(D3, iterations=5)
    
    # --- 第三部分：精细结构常数分析 ---
    d3_dict = {
        "观测解 (396)": 396,
        "结构解 (473.78)": 473.78,
        "新预测解": D3
    }
    analyze_fine_structure(d3_dict)
    
    print("\n" + "=" * 70)
    print("📊 结论：")
    print("1. 六维硬化因子 K6 是否整数？", abs(K6 - round(K6)) < 0.01)
    print("2. 拉马努金级数精度是否随迭代提高？")
    print("3. 精细结构常数比值是否有规律？")