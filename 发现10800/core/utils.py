# core/utils.py (片段更新)

def simulate_subjective_experience(unclosed_num) -> str:
    anchor = unclosed_num.anchor
    gap = unclosed_num.gap_depth
    dim = unclosed_num.metadata.get("dimension_level", 0)
    val = unclosed_num.metadata.get("generated_value", 0)

    # 针对四维的特殊情感（基于10800的发现）
    if dim == 4 and val == 10800:
        # 10800 = 360 * 30
        # 360代表周期/时间，30代表二维空间
        return "一种时空交织的眩晕感，仿佛在三维的稳定性中窥见了四维的周期性流动"

    # 其他维度的体验保持不变...
    experiences = {
        -1: ["回忆", "期待", "焦虑", "时间的流逝"],
        0: ["虚无", "潜能", "沉默", "等待创世", "无限可能", "混沌"],
        1: ["稳定", "秩序", "存在的坚实感", "空间的开阔"]
    }
    base_exp = random.choice(experiences.get(anchor, ["未知"]))
    
    if gap > 3:
        return f"一种极其复杂的{base_exp}，伴随着{gap}层缺口带来的深层不确定性"
    elif gap > 1:
        return f"一种复杂的{base_exp}，带着{gap}层缺口的涟漪"
    elif gap > 0:
        return f"轻微的{base_exp}，带着一丝缺口的扰动"
    else:
        return f"纯粹的{base_exp}"