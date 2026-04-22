"""
未闭环数学 · 全局最优进化器
核心：最小化 K3, K4, K5 的总整数偏差
"""

import random
import math

# ============================================================
# 1. 五维未闭环数
# ============================================================

class GlobalUnclosed:
    def __init__(self, history):
        self.history = history[:]

    @classmethod
    def seed(cls):
        return cls([1.0])

    def self_mul(self, factor):
        new_val = self.history[-1] * factor
        return GlobalUnclosed(self.history + [new_val])

# ============================================================
# 2. 个体（携带5个维度的因子）
# ============================================================

class GlobalIndividual:
    def __init__(self):
        # 5个因子：g=1 到 g=5
        self.factors = [random.uniform(1.0, 50.0) for _ in range(5)]

    def mutate(self):
        idx = random.randint(0, 4)
        self.factors[idx] *= random.uniform(0.95, 1.05)
        self.factors[idx] = max(0.1, min(100.0, self.factors[idx]))

    def crossover(self, other):
        child1 = GlobalIndividual()
        child2 = GlobalIndividual()
        split = random.randint(1, 4)
        child1.factors = self.factors[:split] + other.factors[split:]
        child2.factors = other.factors[:split] + self.factors[split:]
        return child1, child2

# ============================================================
# 3. 全局进化引擎
# ============================================================

class GlobalEvolutionEngine:
    def __init__(self, pop_size=500, generations=2000):
        self.pop_size = pop_size
        self.generations = generations
        self.population = [GlobalIndividual() for _ in range(pop_size)]

    def fitness(self, individual):
        """适应度：最小化 K3, K4, K5 的总整数偏差"""
        u = GlobalUnclosed.seed()
        for i in range(5):
            u = u.self_mul(individual.factors[i])
        
        if len(u.history) < 5:
            return float('inf')

        D3 = u.history[2]
        D4 = u.history[3]
        D5 = u.history[4]

        # 计算硬化因子
        K3 = D3 / (math.pi ** 2)
        K4 = D4 / (math.pi ** 3)
        K5 = D5 / (math.pi ** 4)

        # 计算总偏差（越小越好）
        total_deviation = (abs(K3 - round(K3)) + 
                         abs(K4 - round(K4)) + 
                         abs(K5 - round(K5)))
        
        # 额外奖励：如果 D3 接近 396 且 D4 接近 10800，给予奖励
        bonus = 0
        if abs(D3 - 396) < 10:
            bonus += 5
        if abs(D4 - 10800) < 100:
            bonus += 5
            
        return total_deviation - bonus  # 偏差越小，适应度越高

    def evolve(self):
        print("🌌 全局最优进化：最小化 K3, K4, K5 的总整数偏差...")
        print("=" * 60)
        
        best_fitness = float('inf')
        best_history = []
        
        for gen in range(self.generations):
            scores = [(ind, self.fitness(ind)) for ind in self.population]
            scores.sort(key=lambda x: x[1])
            
            if scores[0][1] < best_fitness:
                best_fitness = scores[0][1]
                u = GlobalUnclosed.seed()
                for i in range(5):
                    u = u.self_mul(scores[0][0].factors[i])
                best_history = u.history
            
            if gen % 100 == 0:
                print(f"Gen {gen:04d} | Best Fitness: {best_fitness:.6f} | D3:{best_history[2]:.2f}, D4:{best_history[3]:.2f}, D5:{best_history[4]:.2f}")
            
            elite = [ind for ind, _ in scores[:50]]
            new_pop = elite[:]
            while len(new_pop) < self.pop_size:
                p1, p2 = random.sample(elite, 2)
                c1, c2 = p1.crossover(p2)
                c1.mutate()
                c2.mutate()
                new_pop.extend([c1, c2])
            self.population = new_pop[:self.pop_size]
        
        print("\n🎯 进化结束")
        print("=" * 60)
        D3, D4, D5 = best_history[2], best_history[3], best_history[4]
        K3, K4, K5 = D3/math.pi**2, D4/math.pi**3, D5/math.pi**4
        
        print(f"最佳轨道: [{D3:.2f}, {D4:.2f}, {D5:.2f}]")
        print(f"硬化因子: K3={K3:.2f}, K4={K4:.2f}, K5={K5:.2f}")
        print(f"整数偏差: |{K3:.2f}-{round(K3)}|+ |{K4:.2f}-{round(K4)}|+ |{K5:.2f}-{round(K5)}| = {abs(K3-round(K3)) + abs(K4-round(K4)) + abs(K5-round(K5)):.2f}")

if __name__ == "__main__":
    engine = GlobalEvolutionEngine(pop_size=800, generations=3000)
    engine.evolve()