"""
未闭环数（时间拓扑模型）
严格遵循：不存在基元连续自乘生成维度谱
"""

from typing import List, Union, Optional, Dict, Any
import math

class UnclosedNumber:
    """
    未闭环数 𝒰 = (a, S, g)
    a ∈ {-1, 0, 1}：锚点（时间/缺口/空间）
    S：序列（整数或未闭环数嵌套）
    g：缺口深度
    """
    
    def __init__(
        self,
        anchor: int,
        known_terms: List[Union[int, float, 'UnclosedNumber']],
        gap_depth: int,
        trust_depth: Optional[int] = None,
        metadata: Optional[Dict] = None
    ):
        if anchor not in {-1, 0, 1}:
            raise ValueError("锚点必须是-1（时间）、0（缺口）或1（空间）")
        
        if anchor == 0 and known_terms:
            raise ValueError("纯缺口（anchor=0）不能有已知项")
        
        self.anchor = anchor
        self.known_terms = known_terms[:]
        self.gap_depth = gap_depth
        self.trust_depth = trust_depth if trust_depth is not None else gap_depth
        self.metadata = metadata if metadata is not None else {}
        
        # 自动标记维度级别
        if "dimension_level" not in self.metadata:
            self.metadata["dimension_level"] = 0 if anchor == 0 else 1
    
    @classmethod
    def not_exist(cls):
        """创建“不存在”基元"""
        return cls(anchor=0, known_terms=[], gap_depth=0, metadata={"dimension_level": 0})
    
    def self_mul(self, max_depth: int = 100, transform_rule: str = "default") -> 'UnclosedNumber':
        """
        自指涉生长
        核心：纯缺口自乘生成下一个维度的特征整数
        """
        if self.gap_depth >= max_depth:
            raise ValueError(f"缺口深度超过最大限制{max_depth}")
        
        # ========== 核心：纯缺口自乘（生成维度）=========
        if self.anchor == 0:
            from core.compiler import DimensionSeries
            
            ds = DimensionSeries()
            current_dim = self.metadata.get("dimension_level", 0)
            next_dim = current_dim + 1
            
            # 生成下一个维度的特征整数
            base_info = ds.generate(next_dim)
            base = base_info["value"]
            
            # 返回新的纯缺口，维度+1，缺口深度+1（关键修复！）
            new_metadata = self.metadata.copy()
            new_metadata["dimension_level"] = next_dim
            new_metadata["generated_value"] = base
            
            return UnclosedNumber(
                anchor=0,  # 保持为纯缺口
                known_terms=[],
                gap_depth=self.gap_depth + 1,  # ✅ 缺口深度递增！
                trust_depth=0,
                metadata=new_metadata
            )
        
        # ========== 空间型自乘（插入自身）=========
        elif self.anchor == 1:
            new_terms = self.known_terms.copy()
            insert_pos = min(self.gap_depth, len(new_terms))
            new_terms.insert(insert_pos, self)
            
            return UnclosedNumber(
                anchor=1,
                known_terms=new_terms,
                gap_depth=self.gap_depth + 1,
                trust_depth=self.trust_depth + 1,
                metadata=self.metadata
            )
        
        # ========== 时间型自乘（反转锚点）=========
        else:
            new_terms = self.known_terms.copy()
            insert_pos = min(self.gap_depth, len(new_terms))
            new_terms.insert(insert_pos, self)
            
            return UnclosedNumber(
                anchor=1,  # 时间平方得空间
                known_terms=new_terms,
                gap_depth=self.gap_depth + 1,
                trust_depth=self.trust_depth + 1,
                metadata=self.metadata
            )
    
    def rev(self) -> 'UnclosedNumber':
        """时间反转操作"""
        if self.anchor == 1:
            new_anchor = -1
        elif self.anchor == -1:
            new_anchor = 1
        else:  # anchor == 0
            new_anchor = 0
        
        return UnclosedNumber(
            anchor=new_anchor,
            known_terms=self.known_terms.copy(),
            gap_depth=self.gap_depth,
            trust_depth=self.trust_depth,
            metadata=self.metadata.copy()
        )
    
    def __repr__(self) -> str:
        gen_val = self.metadata.get("generated_value", "")
        dim = self.metadata.get("dimension_level", "?")
        return (f"𝒰(anchor={self.anchor}, terms={self.known_terms[:3]}..., "
                f"gap={self.gap_depth}, dim={dim}, val={gen_val})")