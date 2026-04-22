"""
未闭环数学 · D5 进化验证器
核心：从 NOT_EXIST 进化出 D5 ≈ 294,489
"""

import random
import math
import zlib

# ============================================================
# 1. D5 未闭环数
# ============================================================

class D5UnclosedNumber:
    """支持五维演化的未闭环数"""
    def __init__(self, anchor, history, gap_depth):
        self.anchor = anchor
        self.history = history[:]  # 记录每一步的值
        self.gap_depth = gap_depth

    @classmethod
    def not_exist(cls):
        return cls(0, [], 0)

    def self_mul(self, factors):
        """自乘：使用对应深度的因子"""
        if self.anchor == 0 and self.gap_depth == 0:
            # 第一次自乘：从 NOT_EXIST 到存在
            return D5UnclosedNumber(1, [1.0], 1)
        elif self.anchor == 0:
            # 纯缺口跃迁
            return D5UnclosedNumber(0, self.history, self.gap_depth + 1)
        else:
            # 使用当前深度对应的因子
            factor = factors[self.gap_depth - 1]  # gap_depth 从1开始
            new_val = self.history[-1] * factor
            new_history = self.history + [new_val]
            return D5UnclosedNumber(self.anchor, new_history, self.gap_depth + 1)

# ============================================================
# 2. D5 进化个体
# ============================================================

class D5Individual:
    """携带五个维度的乘法因子"""
    def __init__(self):
        # 五个因子：对应 g=1,2,3,4,5 的自乘
        self.factors = [random.uniform(1.0, 50.0) for _ in range(5)]
    
    def mutate(self):
        """随机变异一个因子"""
        idx = random.randint(0, 4)
        self.factors[idx] *= random.uniform(0.9, 1.1)
        self.factors[idx] = max(0.1, min(100.0, self.factors[idx]))
    
    def crossover(self, other):
        """交叉：交换部分因子"""
        child1 = D5Individual()
        child2 = D5Individual()
        split = random.randint(1, 4)
        child1.factors = self.factors[:split] + other.factors[split:]
        child2.factors = other.factors[:split] + self.factors[split:]
        return child1, child2

# ============================================================
# 3. D5 进化引擎
# ============================================================

class D5EvolutionEngine:
    def __init__(self, pop_size=500, generations=2000):
        self.pop_size = pop_size
        self.generations = generations
        self.population = [D5Individual() for _ in range(pop_size)]
        self.target_D5 = 3023 * (math.pi ** 4)  # ≈ 294,489
        self.target_K5 = 3023
        
    def fitness(self, individual):
        """适应度：D5 接近目标且 K5 接近整数"""
        u = D5UnclosedNumber.not_exist()
        for _ in range(5):  # 五次自乘，到达 D5
            u = u.self_mul(individual.factors)
        
        if len(u.history) < 5:
            return float('inf')
        
        D5 = u.history[-1]
        
        # 误差1：D5 接近目标
        error_D5 = abs(D5 - self.target_D5)
        
        # 误差2：K5 = D5 / π^4 接近整数 3023
        K5 = D5 / (math.pi ** 4)
        error_K5 = abs(K5 - round(K5))
        
        # 奖励 D3 和 D4 也符合已知值（可选）
        D3 = u.history[2] if len(u.history) >= 3 else 0
        D4 = u.history[3] if len(u.history) >= 4 else 0
        error_D3 = abs(D3 - 396) if D3 > 0 else 1000
        error_D4 = abs(D4 - 10800) if D4 > 0 else 1000
        
        # 综合适应度（越小越好）
        total_error = error_D5 + 10 * error_K5 + 0.1 * error_D3 + 0.1 * error_D4
        
        # 奖励适度复杂（避免平凡解）
        seq_str = ','.join(map(str, u.history))
        compressed = zlib.compress(seq_str.encode('utf-8'))
        compression_ratio = len(compressed) / len(seq_str) if seq_str else 1.0
        complexity_bonus = 0
        if 0.3 < compression_ratio < 0.7:
            complexity_bonus = 1000  # 降低总误差
        
        return total_error - complexity_bonus
    
    def evolve(self):
        print("🌌 D5 进化验证：从 NOT_EXIST 到 294,489...")
        print("=" * 60)
        print(f"目标 D5 = {self.target_D5:.2f}")
        print(f"目标 K5 = {self.target_K5} (整数)")
        print("=" * 60)
        
        best_error = float('inf')
        best_history = []
        stagnation = 0
        
        for gen in range(self.generations):
            fitness_scores = [(ind, self.fitness(ind)) for ind in self.population]
            fitness_scores.sort(key=lambda x: x[1])
            
            current_best = fitness_scores[0][1]
            if current_best < best_error:
                best_error = current_best
                # 重新计算最佳历史
                best_ind = fitness_scores[0][0]
                u = D5UnclosedNumber.not_exist()
                temp_history = []
                for _ in range(5):
                    u = u.self_mul(best_ind.factors)
                    if u.history:
                        temp_history = u.history
                best_history = temp_history
                stagnation = 0
            else:
                stagnation += 1
            
            if gen % 100 == 0:
                print(f"Gen {gen:04d} | Best Error: {best_error:.6f} | D5: {best_history[-1] if best_history else 0:.2f}")
            
            # 如果停滞，引入随机重启
            if stagnation > 200:
                print(f"Gen {gen}: 检测到停滞，引入随机重启！")
                self.population = [D5Individual() for _ in range(self.pop_size)]
                stagnation = 0
                continue
            
            elite = [ind for ind, _ in fitness_scores[:50]]
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
        print(f"最佳演化轨道: {[round(x, 4) for x in best_history]}")
        
        if len(best_history) >= 5:
            D3 = best_history[2]
            D4 = best_history[3]
            D5 = best_history[4]
            
            print(f"\n验证结果：")
            print(f"D3 = {D3:.2f} (目标 396)")
            print(f"D4 = {D4:.2f} (目标 10800)")
            print(f"D5 = {D5:.2f} (目标 {self.target_D5:.2f})")
            
            K3 = D3 / (math.pi ** 2)
            K4 = D4 / (math.pi ** 3)
            K5 = D5 / (math.pi ** 4)
            
            print(f"\n硬化因子：")
            print(f"K3 = {K3:.2f} (目标 ~40.12)")
            print(f"K4 = {K4:.2f} (目标 ~348.32)")
            print(f"K5 = {K5:.2f} (目标 {self.target_K5})")
            
            # 检查是否接近整数
            print(f"\n整数检查：")
            print(f"K3 接近整数: {round(K3)} (误差 {abs(K3 - round(K3)):.2f})")
            print(f"K4 接近整数: {round(K4)} (误差 {abs(K4 - round(K4)):.2f})")
            print(f"K5 接近整数: {round(K5)} (误差 {abs(K5 - round(K5)):.2f})")
            
            # 计算投影 π
            projected_pi = math.sqrt(D3 / round(K3)) if K3 > 0 else 0
            print(f"\n投影 π = {projected_pi:.10f}")
            print(f"真实 π   = {math.pi:.10f}")
            print(f"误差     = {abs(projected_pi - math.pi):.10f}")

if __name__ == "__main__":
    engine = D5EvolutionEngine(pop_size=800, generations=3000)
    engine.evolve()