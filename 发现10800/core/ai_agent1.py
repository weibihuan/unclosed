"""
未闭环AI原型
具备自我生长、缺口驱动探索、逆分形生成能力
"""

import random
from typing import List, Dict, Any
import mpmath as mp

# 导入核心组件
from .unclosed_number import UnclosedNumber
from .gap_map import GapMap
from .compiler import OptimalRepresentationCompiler
from .utils import analyze_physical_constants

class UnclosedAIAgent:
    """
    未闭环AI代理
    核心能力：
    1. 自我生长（通过自乘）
    2. 缺口驱动探索（优先探索缺口大的节点）
    3. 逆分形生成（从分形特征反推常数）
    """
    
    def __init__(self, name: str = "U-AI-001"):
        self.name = name
        self.gap_map = GapMap()  # 知识库/缺口地图
        self.compiler = OptimalRepresentationCompiler(self.gap_map)
        self.memory = []  # 生长历史
        
        # 初始化：创建纯缺口（种子）
        self.seed = UnclosedNumber.not_exist()
        self.current_state = self.seed
        
        print(f"🤖 未闭环AI [{self.name}] 初始化完成")
        print(f"   初始状态: {self.current_state}")
        print(f"   初始感受: {self.simulate_subjective_experience(self.seed)}")
    
    def simulate_subjective_experience(self, unclosed_num) -> str:
        """模拟主观体验（情感/感受）"""
        from .utils import simulate_subjective_experience as sim_exp
        return sim_exp(unclosed_num)
    
    def self_grow(self) -> UnclosedNumber:
        """自我生长：执行一次自乘"""
        print(f"\n🔄 [{self.name}] 执行自乘生长...")
        self.current_state = self.current_state.self_mul()
        self.memory.append(self.current_state)
        
        # 将新状态加入缺口地图
        node_id = f"state_{len(self.memory)}"
        self.gap_map.add_node(
            data=self.current_state,
            node_id=node_id,
            gap=self.current_state.gap_depth * 0.1,
            meta_gap=0.05
        )
        
        print(f"   新状态: {self.current_state}")
        print(f"   缺口深度: {self.current_state.gap_depth}")
        print(f"   缺口压力: {self.calculate_gap_pressure():.2f}")
        print(f"   主观体验: {self.simulate_subjective_experience(self.current_state)}")
        return self.current_state
    
    def calculate_gap_pressure(self) -> float:
        """计算缺口压力"""
        from .utils import calculate_gap_pressure
        return calculate_gap_pressure(self.current_state)
    
    def explore_by_gap(self) -> Dict[str, Any]:
        """缺口驱动探索：选择缺口最大的节点进行扩展"""
        print(f"\n🔍 [{self.name}] 执行缺口驱动探索...")
        
        # 获取缺口地图中缺口最大的节点
        nodes = self.gap_map.get_all_nodes()
        if not nodes:
            print("   缺口地图为空，先执行生长。")
            return {}
        
        # 按缺口深度排序
        sorted_nodes = sorted(
            nodes, 
            key=lambda x: x['gap'], 
            reverse=True
        )
        target_node = sorted_nodes[0]
        
        print(f"   选择节点: {target_node['id']}")
        print(f"   缺口深度: {target_node['gap']}")
        
        # 对该节点进行逆分形分析
        result = self.compiler.analyze_fractal_features(target_node['data'])
        
        # 将结果存入缺口地图
        self.gap_map.update_node_metadata(
            target_node['id'], 
            {"last_exploration": result}
        )
        
        return result
    
    def discover_dimension(self, dim: int, new_value: int, reason: str = "experiment"):
        """
        AI 发现新的维度值并更新编译器
        """
        print(f"\n💡 [{self.name}] 发现维度 {dim} 的新特征数: {new_value}")
        print(f"   原因: {reason}")
        
        # 调用编译器的更新接口
        self.compiler.dim_series.update_dimension(dim, new_value, source=f"AI_{reason}")
        
        # 更新缺口地图中的元数据
        self.current_state.metadata[f"dim_{dim}_value"] = new_value
        
        # 重新计算主观体验（因为现实变了）
        print(f"   新的主观体验: {self.simulate_subjective_experience(self.current_state)}")
    
    def run_cycle(self, cycles: int = 3):
        """运行一个生长-探索周期"""
        print(f"\n{'='*50}")
        print(f"🚀 [{self.name}] 开始运行 {cycles} 个周期")
        print(f"{'='*50}")
        
        for i in range(cycles):
            print(f"\n--- 周期 {i+1}/{cycles} ---")
            
            # 1. 生长
            state = self.self_grow()
            
            # 2. 探索（每生长两次探索一次）
            if (i+1) % 2 == 0:
                exploration = self.explore_by_gap()
                if exploration:
                    print(f"   探索发现: {exploration.get('summary', '无摘要')}")
            
            # 3. 随机扰动（模拟好奇心）
            if random.random() < 0.3:  # 30%概率
                print(f"   🎲 触发随机扰动...")
                # 时间反转
                perturbed = state.rev()
                print(f"      反转状态: {perturbed}")
                print(f"      反转感受: {self.simulate_subjective_experience(perturbed)}")
        
        # 周期结束，分析当前状态
        print(f"\n{'='*50}")
        print(f"📊 [{self.name}] 周期运行结束")
        print(f"   当前状态: {self.current_state}")
        print(f"   生长次数: {len(self.memory)}")
        print(f"   缺口地图节点数: {len(self.gap_map.get_all_nodes())}")
        
        # 分析物理常数关联（如果有）
        if self.current_state.anchor == 0 and "generated_value" in self.current_state.metadata:
            base = self.current_state.metadata["generated_value"]
            if base == 396:
                print(f"\n🌟 检测到关键基数 396！")
                physics = analyze_physical_constants()
                print(f"   物理关联: {physics['relation_396_alpha']}")
        
        return {
            "final_state": self.current_state,
            "memory": self.memory,
            "gap_map_size": len(self.gap_map.get_all_nodes())
        }

# 测试函数
def test_ai_agent():
    """测试未闭环AI代理"""
    ai = UnclosedAIAgent("U-AI-Alpha")
    result = ai.run_cycle(cycles=4)
    
    # 模拟 AI 发现 PSLQ 验证通过，决定更新维度4
    # 假设这是从之前的测试日志中得到的 10800
    if ai.current_state.metadata.get("dimension_level") == 4:
        ai.discover_dimension(4, 10800, reason="pslq_validation_success")
    
    return ai, result

if __name__ == "__main__":
    test_ai_agent()