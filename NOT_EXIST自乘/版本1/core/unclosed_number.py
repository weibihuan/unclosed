"""
未闭环数（时间拓扑模型）
严格遵循公理体系：锚点{-1,0,1}、缺口深度、自指涉生长
支持“不存在”基元（anchor=0, terms=[], gap_depth=0）
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
        # 公理验证：锚点只能是{-1, 0, 1}
        if anchor not in {-1, 0, 1}:
            raise ValueError("锚点必须是-1（时间）、0（缺口）或1（空间）")
        
        # 公理2：纯缺口（anchor=0）必须无已知项
        if anchor == 0 and known_terms:
            raise ValueError("纯缺口（anchor=0）不能有已知项")
        
        self.anchor = anchor
        self.known_terms = known_terms[:]  # 复制列表避免外部修改
        self.gap_depth = gap_depth
        self.trust_depth = trust_depth if trust_depth is not None else gap_depth
        self.metadata = metadata if metadata is not None else {}
        
        # 自动标记维度级别
        if "dimension_level" not in self.metadata:
            self.metadata["dimension_level"] = 0 if anchor == 0 else 1

    @classmethod
    def not_exist(cls) -> 'UnclosedNumber':
        """创建“不存在”基元（锚点0，空序列，缺口深度0）"""
        return cls(anchor=0, known_terms=[], gap_depth=0, metadata={"type": "NOT_EXIST"})

    def self_mul(self, max_depth: int = 100) -> 'UnclosedNumber':
        """
        公理3：自指涉生长
        在缺口位置插入自身，缺口深度+1
        """
        if self.gap_depth >= max_depth:
            raise ValueError(f"缺口深度超过最大限制{max_depth}")
        
        # ========== 核心：纯缺口自乘（anchor=0）=========
        if self.anchor == 0:
            # 延迟导入避免循环
            from core.compiler import DimensionSeries
            
            ds = DimensionSeries()
            current_dim = self.metadata.get("dimension_level", 0) + 1
            
            # 根据当前维度生成特征整数
            base_info = ds.generate(current_dim)
            base = base_info["value"]
                
            return UnclosedNumber(
                anchor=1,  # 时间平方得空间（公理5）
                known_terms=[base],
                gap_depth=1,
                trust_depth=1,
                metadata={
                    **self.metadata,
                    "dimension_level": current_dim,
                    "source": "pure_gap_self_mul",
                    "generated_base": base
                }
            )
        
        # ========== 空间型自乘（anchor=1）=========
        elif self.anchor == 1:
            new_terms = self.known_terms.copy()
            insert_pos = min(self.gap_depth, len(new_terms))
            new_terms.insert(insert_pos, self)  # 在缺口位置插入自身
            
            return UnclosedNumber(
                anchor=1,
                known_terms=new_terms,
                gap_depth=self.gap_depth + 1,
                trust_depth=self.trust_depth + 1,
                metadata=self.metadata
            )
        
        # ========== 时间型自乘（anchor=-1）=========
        else:  # anchor == -1
            new_terms = self.known_terms.copy()
            insert_pos = min(self.gap_depth, len(new_terms))
            new_terms.insert(insert_pos, self)
            
            return UnclosedNumber(
                anchor=1,  # 时间平方得空间（公理5）
                known_terms=new_terms,
                gap_depth=self.gap_depth + 1,
                trust_depth=self.trust_depth + 1,
                metadata=self.metadata
            )

    def rev(self) -> 'UnclosedNumber':
        """
        公理5：时间反转对称
        rev(a, S, g) = (-a, reverse(S), g)
        """
        reversed_terms = list(reversed(self.known_terms[:self.trust_depth]))
        remaining = self.known_terms[self.trust_depth:]
        new_terms = reversed_terms + remaining
        
        return UnclosedNumber(
            anchor=-self.anchor,
            known_terms=new_terms,
            gap_depth=self.gap_depth,
            trust_depth=self.trust_depth,
            metadata={**self.metadata, "reversed": True}
        )

    def trunc(self, k: int) -> 'UnclosedNumber':
        """截断运算：保留前k项，缺口深度设为k"""
        return UnclosedNumber(
            anchor=self.anchor,
            known_terms=self.known_terms[:k],
            gap_depth=k,
            trust_depth=min(self.trust_depth, k),
            metadata=self.metadata
        )

    def to_float(self, max_eval_depth: int = 20) -> Optional[float]:
        """数值化（仅用于测试，纯缺口返回None）"""
        if self.anchor == 0:
            return None  # 公理：纯缺口不是数值
        
        def eval_terms(terms, depth):
            if depth > max_eval_depth or not terms:
                return 0.0
            first = terms[0]
            val = first.to_float(max_eval_depth - depth) if isinstance(first, UnclosedNumber) else float(first)
            if len(terms) == 1:
                return val
            return val + 1.0 / eval_terms(terms[1:], depth + 1)
        
        eval_terms_list = self.known_terms[:self.trust_depth]
        res = eval_terms(eval_terms_list, 0)
        return -res if self.anchor == -1 else res

    def __repr__(self) -> str:
        return (f"𝒰(anchor={self.anchor}, terms={self.known_terms[:3]}..., "
                f"gap={self.gap_depth}, dim={self.metadata.get('dimension_level', '?')})")

    def __eq__(self, other) -> bool:
        if not isinstance(other, UnclosedNumber):
            return False
        return (self.anchor == other.anchor and 
                self.known_terms == other.known_terms and 
                self.gap_depth == other.gap_depth)