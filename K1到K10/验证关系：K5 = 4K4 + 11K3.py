import random
import math

# 已知的硬化因子
K3_base = 51
K4_base = 347
K5_base = 1949
K6_base = 9477

# 验证关系：K5 = 4*K4 + 11*K3
print("验证关系 K5 = 4*K4 + 11*K3:")
print(f"4*{K4_base} + 11*{K3_base} = {4*K4_base + 11*K3_base}")
print(f"K5 = {K5_base}")
print(f"是否相等: {4*K4_base + 11*K3_base == K5_base}")

# 生成带噪声的数据，验证关系是否仍然近似成立
print("\n带噪声的数据验证:")
for i in range(5):
    noise3 = random.uniform(0.999, 1.001)
    noise4 = random.uniform(0.999, 1.001)
    noise5 = random.uniform(0.999, 1.001)
    noise6 = random.uniform(0.999, 1.001)
    
    K3 = K3_base * noise3
    K4 = K4_base * noise4
    K5 = K5_base * noise5
    K6 = K6_base * noise6
    
    left = 4*K4 + 11*K3
    diff = abs(left - K5)
    print(f"第{i+1}组: K3={K3:.2f}, K4={K4:.2f}, K5={K5:.2f}, 4*K4+11*K3={left:.2f}, 差值={diff:.2e}")

# 尝试寻找K6的递推关系：假设 K6 = a*K5 + b*K4 + c*K3
# 使用整数求解（可能有多组解）
print("\n寻找K6的递推关系（整数系数）：")
# 我们尝试小整数范围内的系数
found = False
for a in range(-20, 21):
    for b in range(-20, 21):
        for c in range(-20, 21):
            if a == 0 and b == 0 and c == 0:
                continue
            if a*K5_base + b*K4_base + c*K3_base == K6_base:
                print(f"找到关系: K6 = {a}*K5 + {b}*K4 + {c}*K3")
                found = True
                # 验证
                print(f"验证: {a}*{K5_base} + {b}*{K4_base} + {c}*{K3_base} = {a*K5_base + b*K4_base + c*K3_base}")
if not found:
    print("在小整数范围内未找到精确关系。")