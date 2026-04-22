import random
import math
import mpmath as mp

# ============================================================
# 进化搜索大底数 Q
# 目标：找到使拉马努金级数收敛最快的整数底数 Q
# ============================================================

class Individual:
    def __init__(self):
        # 整数底数 Q，范围 100-20000
        self.Q = random.randint(100, 20000)
        # 系数 A 和 B，范围 1-50000
        self.A = random.randint(1, 50000)
        self.B = random.randint(1, 50000)
    
    def mutate(self):
        # 变异：小幅调整 Q, A, B
        if random.random() < 0.5:
            self.Q += random.randint(-100, 100)
        else:
            self.Q = random.randint(100, 20000)
        
        if random.random() < 0.5:
            self.A += random.randint(-100, 100)
        else:
            self.A = random.randint(1, 50000)
            
        if random.random() < 0.5:
            self.B += random.randint(-100, 100)
        else:
            self.B = random.randint(1, 50000)
        
        # 确保正数
        self.Q = max(100, self.Q)
        self.A = max(1, self.A)
        self.B = max(1, self.B)
    
    def crossover(self, other):
        child1 = Individual()
        child2 = Individual()
        # 单点交叉
        if random.random() < 0.5:
            child1.Q, child1.A, child1.B = self.Q, self.A, other.B
            child2.Q, child2.A, child2.B = other.Q, other.A, self.B
        else:
            child1.Q, child1.A, child1.B = self.Q, other.A, self.B
            child2.Q, child2.A, child2.B = other.Q, self.A, other.B
        return child1, child2

def fitness(ind, terms=3):
    """适应度函数：误差越小越好，同时奖励更大的底数 Q"""
    mp.mp.dps = 50
    C = 2 * mp.sqrt(2) / 9801
    Q = mp.mpf(ind.Q)
    
    total = mp.mpf(0)
    for n in range(terms):
        fact_4n = mp.factorial(4*n)
        fact_n4 = mp.factorial(n) ** 4
        term = fact_4n * (ind.A * n + ind.B) / (fact_n4 * (Q ** (4*n)))
        total += term
    
    pi_approx = 1 / (C * total)
    error = abs(pi_approx - mp.pi)
    
    # 适应度 = 1/(误差+1e-20) + 奖励底数大小（对数尺度）
    fitness_score = 1.0 / (float(error) + 1e-20) + math.log(ind.Q)
    return fitness_score

def evolve(pop_size=100, generations=500):
    print("🧬 进化搜索大底数 Q")
    print("=" * 60)
    
    population = [Individual() for _ in range(pop_size)]
    best_fitness = float('-inf')
    best_ind = None
    best_error = float('inf')
    
    for gen in range(generations):
        scored = [(ind, fitness(ind)) for ind in population]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        if scored[0][1] > best_fitness:
            best_fitness = scored[0][1]
            best_ind = scored[0][0]
            # 计算误差
            mp.mp.dps = 50
            C = 2 * mp.sqrt(2) / 9801
            Q = mp.mpf(best_ind.Q)
            total = mp.mpf(0)
            for n in range(3):
                fact_4n = mp.factorial(4*n)
                fact_n4 = mp.factorial(n) ** 4
                term = fact_4n * (best_ind.A * n + best_ind.B) / (fact_n4 * (Q ** (4*n)))
                total += term
            pi_approx = 1 / (C * total)
            best_error = abs(pi_approx - mp.pi)
        
        if gen % 50 == 0:
            print(f"Gen {gen:03d} | Best Q={best_ind.Q} | A={best_ind.A} | B={best_ind.B} | Error={best_error:.2e}")
        
        # 选择精英
        elite = [ind for ind, _ in scored[:20]]
        new_pop = elite[:]
        while len(new_pop) < pop_size:
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)
            child1, child2 = parent1.crossover(parent2)
            child1.mutate()
            child2.mutate()
            new_pop.extend([child1, child2])
        population = new_pop[:pop_size]
    
    print("\n🎯 进化结束")
    print("=" * 60)
    print(f"最佳底数 Q = {best_ind.Q}")
    print(f"最佳系数 A = {best_ind.A}, B = {best_ind.B}")
    print(f"误差 = {best_error:.2e}")
    
    # 验证收敛速度
    print("\n验证收敛速度（前5次迭代）：")
    mp.mp.dps = 80
    C = 2 * mp.sqrt(2) / 9801
    Q = mp.mpf(best_ind.Q)
    total = mp.mpf(0)
    for n in range(5):
        fact_4n = mp.factorial(4*n)
        fact_n4 = mp.factorial(n) ** 4
        term = fact_4n * (best_ind.A * n + best_ind.B) / (fact_n4 * (Q ** (4*n)))
        total += term
        pi_approx = 1 / (C * total)
        error = abs(pi_approx - mp.pi)
        print(f"  n={n}: 误差 = {error:.10e}")

if __name__ == "__main__":
    evolve(pop_size=200, generations=1000)