"""
未闭环数学 · 整数底数进化搜索（拉马努金型级数）
目标：找到整数 Q，使得级数 1/π = C·Σ (4n)!/(n!)^4·(26390n+1103)/Q^{4n} 的前几项和极度逼近 1/π，
同时使硬化因子 K = Q^{1/4} / π² 接近整数。
"""

import math
import random
import mpmath as mp

# 设置高精度
mp.dps = 100

# 拉马努金级数常数
C = 2 * mp.sqrt(2) / 9801

# 固定的系数（来自Chudnovsky，也可以作为进化参数，但先固定）
A = 26390
B = 1103

def compute_pi_error(Q, terms=5):
    """
    给定整数底数 Q，计算级数前 terms 项的和，返回估计的 π 与真实 π 的误差。
    """
    total = mp.mpf(0)
    Q_mp = mp.mpf(Q)
    for n in range(terms):
        # 计算 (4n)! / (n!)^4
        fact4n = mp.fac(4*n)
        fact_n = mp.fac(n)
        comb = fact4n / (fact_n ** 4)
        term = comb * (A * n + B) / (Q_mp ** (4*n))
        total += term
    pi_approx = 1 / (C * total)
    return abs(pi_approx - mp.pi)

def hardening_integerity(Q):
    """
    计算硬化因子 K = Q^{1/4} / π² 与最近整数的偏差。
    偏差越小，说明硬化因子越接近整数。
    """
    D3 = mp.power(mp.mpf(Q), 0.25)          # D3 ≈ Q^{1/4}
    K = D3 / (mp.pi ** 2)
    nearest = round(K)
    return abs(K - nearest)

def fitness(Q):
    """
    适应度函数：误差越小越好，硬化因子越整数越好。
    """
    try:
        err = compute_pi_error(Q, terms=5)
        # 避免除零，若误差极小则直接返回巨大值
        if err < mp.mpf('1e-50'):
            return 1e100
        int_dev = hardening_integerity(Q)
        # 误差贡献：1/err，整数性贡献：10/(int_dev+0.01)
        # 权重可调
        score = 1.0 / float(err) + 10.0 / (float(int_dev) + 0.01)
        return score
    except Exception:
        return 0.0

def mutate(Q, step=1):
    """变异：随机调整 Q 的值，保证 Q >= 10"""
    new_Q = Q + random.randint(-step, step)
    if new_Q < 10:
        new_Q = 10
    # 有时乘除小质数
    if random.random() < 0.3:
        if random.random() < 0.5:
            new_Q = int(new_Q * random.choice([2, 3, 5, 7]))
        else:
            new_Q = int(new_Q / random.choice([2, 3, 5, 7]))
            if new_Q < 10:
                new_Q = 10
    return new_Q

def crossover(Q1, Q2):
    """交叉：随机取平均值或随机选择"""
    if random.random() < 0.5:
        return (Q1 + Q2) // 2
    else:
        return random.choice([Q1, Q2])

def evolution_search(pop_size=50, generations=200, init_min=300, init_max=5000):
    """
    进化搜索主函数。
    """
    print("🚀 启动整数底数 Q 进化搜索（拉马努金型级数）...")
    print("="*60)
    # 初始化种群
    population = [random.randint(init_min, init_max) for _ in range(pop_size)]
    best_Q = None
    best_fitness = -float('inf')
    best_error = None

    for gen in range(generations):
        # 评估适应度
        scored = [(Q, fitness(Q)) for Q in population]
        scored.sort(key=lambda x: x[1], reverse=True)
        # 记录最佳
        if scored[0][1] > best_fitness:
            best_fitness = scored[0][1]
            best_Q = scored[0][0]
            best_error = compute_pi_error(best_Q, terms=5)
        # 打印进度
        if gen % 20 == 0:
            print(f"Gen {gen:03d} | Best Q = {best_Q} | Fitness = {best_fitness:.2f} | π error = {float(best_error):.2e}")

        # 选择精英（前20%）
        elite_size = pop_size // 5
        elite = [Q for Q, _ in scored[:elite_size]]
        # 生成下一代
        new_pop = elite[:]
        while len(new_pop) < pop_size:
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_pop.append(child)
        population = new_pop

    print("\n🎯 进化结束")
    print(f"最佳整数底数 Q = {best_Q}")
    print(f"对应 π 近似误差（5项）: {float(best_error):.2e}")
    # 验证硬化因子
    D3 = mp.power(mp.mpf(best_Q), 0.25)
    K = D3 / (mp.pi ** 2)
    print(f"硬化因子 K ≈ {float(K):.6f}，与整数偏差 = {abs(float(K) - round(float(K))):.6f}")
    # 输出高精度 π 近似
    pi_approx = 1 / (C * sum(
        mp.fac(4*n) / (mp.fac(n)**4) * (A*n + B) / (mp.mpf(best_Q)**(4*n))
        for n in range(5)
    ))
    print(f"使用 {best_Q} 的 5 项 π 近似值:\n{mp.nstr(pi_approx, 30)}")
    print(f"真实 π = {mp.nstr(mp.pi, 30)}")
    return best_Q

if __name__ == "__main__":
    best = evolution_search(pop_size=60, generations=300, init_min=300, init_max=6000)