import random
import math
import mpmath as mp

# ============================================================
# 未闭环数学 · π 的不动点生成器
# 核心：让 π 从缺口自乘的迭代中自然涌现
# ============================================================

class UnclosedPiGenerator:
    """生成 π 的不动点迭代器"""
    def __init__(self, seed=None):
        self.seed = seed or random.uniform(1.0, 10.0)
        self.sequence = [self.seed]
        self.depth = 0
        
    def self_multiply(self, rule):
        """自乘：根据规则生成新值"""
        new_val = rule(self.sequence, self.depth)
        self.sequence.append(new_val)
        self.depth += 1
        return new_val
    
    def project(self):
        """投影：将序列映射为实数"""
        # 投影规则1：取序列最后一个元素
        return self.sequence[-1]
    
    def project_inverse(self):
        """逆投影：用连分数展开"""
        # 将序列视为连分数系数
        if len(self.sequence) < 2:
            return self.sequence[0]
        
        # 计算连分数 [a0; a1, a2, ...]
        result = mp.mpf(0)
        for a in reversed(self.sequence[1:]):
            result = 1 / (a + result)
        return self.sequence[0] + result

# ============================================================
# 进化规则搜索器
# ============================================================

class RuleIndividual:
    """携带自乘规则的个体"""
    def __init__(self):
        # 规则参数：新值 = (前一项 * a + b) / (c * depth + d)
        self.a = random.uniform(0.1, 5.0)
        self.b = random.uniform(0.1, 5.0)
        self.c = random.uniform(0.1, 5.0)
        self.d = random.uniform(0.1, 5.0)
    
    def apply(self, sequence, depth):
        """应用规则生成新值"""
        if not sequence:
            return 1.0
        prev = sequence[-1]
        # 非线性规则
        return (prev * self.a + self.b) / (self.c * depth + self.d)
    
    def mutate(self):
        """变异"""
        if random.random() < 0.5:
            self.a += random.uniform(-0.1, 0.1)
        else:
            self.a = random.uniform(0.1, 5.0)
        
        if random.random() < 0.5:
            self.b += random.uniform(-0.1, 0.1)
        else:
            self.b = random.uniform(0.1, 5.0)
        
        if random.random() < 0.5:
            self.c += random.uniform(-0.1, 0.1)
        else:
            self.c = random.uniform(0.1, 5.0)
        
        if random.random() < 0.5:
            self.d += random.uniform(-0.1, 0.1)
        else:
            self.d = random.uniform(0.1, 5.0)
        
        # 确保正数
        self.a = max(0.1, self.a)
        self.b = max(0.1, self.b)
        self.c = max(0.1, self.c)
        self.d = max(0.1, self.d)
    
    def crossover(self, other):
        """交叉"""
        child1 = RuleIndividual()
        child2 = RuleIndividual()
        
        # 单点交叉
        if random.random() < 0.5:
            child1.a, child1.b, child1.c, child1.d = self.a, self.b, other.c, other.d
            child2.a, child2.b, child2.c, child2.d = other.a, other.b, self.c, self.d
        else:
            child1.a, child1.b, child1.c, child1.d = self.a, other.b, self.c, other.d
            child2.a, child2.b, child2.c, child2.d = other.a, self.b, other.c, self.d
        
        return child1, child2

def fitness(individual, iterations=10):
    """适应度：迭代后投影值接近 π"""
    generator = UnclosedPiGenerator(seed=1.0)  # 固定种子
    
    for i in range(iterations):
        generator.self_multiply(individual.apply)
    
    # 使用两种投影方式
    proj1 = generator.project()
    proj2 = generator.project_inverse()
    
    # 计算与 π 的误差
    error1 = abs(proj1 - mp.pi)
    error2 = abs(proj2 - mp.pi)
    
    # 选择较小的误差
    error = min(error1, error2)
    
    # 奖励序列的稳定性（最后几次迭代变化小）
    stability = 0
    if len(generator.sequence) > 3:
        changes = [abs(generator.sequence[-i] - generator.sequence[-i-1]) 
                   for i in range(1, 4)]
        stability = sum(changes) / len(changes)
    
    # 适应度 = 1/(误差+稳定性+1e-10)
    return 1.0 / (float(error) + float(stability) + 1e-10)

def evolve_rules(pop_size=100, generations=500):
    """进化搜索规则"""
    print("🧬 进化搜索 π 的不动点生成规则")
    print("=" * 60)
    
    mp.mp.dps = 50  # 设置高精度
    
    population = [RuleIndividual() for _ in range(pop_size)]
    best_fitness = float('-inf')
    best_rule = None
    best_sequence = []
    
    for gen in range(generations):
        scored = [(ind, fitness(ind)) for ind in population]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        if scored[0][1] > best_fitness:
            best_fitness = scored[0][1]
            best_rule = scored[0][0]
            
            # 记录最佳序列
            gen_test = UnclosedPiGenerator(seed=1.0)
            for _ in range(10):
                gen_test.self_multiply(best_rule.apply)
            best_sequence = gen_test.sequence
            
            print(f"Gen {gen:03d} | Best Fitness: {best_fitness:.6f}")
            print(f"  规则: a={best_rule.a:.4f}, b={best_rule.b:.4f}, c={best_rule.c:.4f}, d={best_rule.d:.4f}")
            print(f"  序列: {[round(x, 4) for x in best_sequence[-3:]]}")
        
        # 选择精英
        elite = [ind for ind, _ in scored[:20]]
        new_pop = elite[:]
        
        # 生成新种群
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
    
    # 最终测试
    final_gen = UnclosedPiGenerator(seed=1.0)
    for _ in range(10):
        final_gen.self_multiply(best_rule.apply)
    
    print(f"最佳规则: a={best_rule.a:.6f}, b={best_rule.b:.6f}, c={best_rule.c:.6f}, d={best_rule.d:.6f}")
    print(f"最终序列: {[round(x, 10) for x in final_gen.sequence]}")
    print(f"投影值 (最后一项): {float(final_gen.sequence[-1]):.15f}")
    # 将逆投影值转换为浮点数再格式化
    inv_proj = float(final_gen.project_inverse())
    print(f"逆投影值 (连分数): {inv_proj:.15f}")
    print(f"真实 π: {float(mp.pi):.15f}")
    print(f"误差: {abs(inv_proj - float(mp.pi)):.15e}")
    
    return best_rule, final_gen.sequence

if __name__ == "__main__":
    best_rule, best_seq = evolve_rules(pop_size=200, generations=1000)