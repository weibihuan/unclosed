#!/usr/bin/env python3
"""
generate_figures.py
生成所有图表
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.visualization import setup_plot_style
from src.utils import load_config
import matplotlib.pyplot as plt
import numpy as np

def generate_all_figures():
    """生成所有图表"""
    config = load_config()
    setup_plot_style()
    
    # 示例数据（实际应从结果文件加载）
    print("生成图表...")
    
    # 示例图表1: 理论框架图
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 绘制未闭环数学三定律示意图
    theories = ['缺口即动力', '最优表示定理', '指纹不灭原理']
    descriptions = [
        '数学系统因逻辑缺口而存在和演化',
        '存在收敛最快的数学表示',
        '编译指纹必然显现于连分数、PSLQ或级数中'
    ]
    
    y_pos = np.arange(len(theories))
    
    ax.barh(y_pos, [3, 2, 1], align='center', alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(theories)
    ax.invert_yaxis()
    ax.set_xlabel('理论重要性')
    ax.set_title('未闭环数学三定律框架')
    
    # 添加描述
    for i, desc in enumerate(descriptions):
        ax.text(0.1, i, desc, va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('figures/theoretical_framework.png', bbox_inches='tight')
    print("  ✅ 理论框架图已生成")
    
    # 示例图表2: 研究流程图
    fig, ax = plt.subplots(figsize=(12, 6))
    
    steps = [
        '理论构建\n(三定律)',
        '工具开发\n(unclosed库)',
        '案例选择\n(谢尔宾斯基地毯)',
        '实验设计\n(三通道分析)',
        '数据分析\n(指纹发现)',
        '理论验证\n(对比研究)'
    ]
    
    x_pos = np.arange(len(steps))
    
    ax.plot(x_pos, [1, 2, 3, 4, 5, 6], 'o-', linewidth=3, markersize=10)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(steps, rotation=45, ha='right')
    ax.set_ylabel('研究阶段')
    ax.set_title('研究流程与方法论')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/research_flowchart.png', bbox_inches='tight')
    print("  ✅ 研究流程图已生成")
    
    # 示例图表3: 指纹特征总结
    fig, ax = plt.subplots(figsize=(10, 6))
    
    features = {
        '巨大偏商': ('谢尔宾斯基地毯', 1),
        '精确代数关系': ('谢尔宾斯基地毯', 1),
        '有限连分数': ('谢尔宾斯基地毯', 1),
        '快速收敛级数': ('两者', 0.5)
    }
    
    systems = ['谢尔宾斯基地毯', '曼德博集合']
    feature_matrix = np.array([
        [1, 0],  # 巨大偏商
        [1, 0],  # 精确关系
        [1, 0],  # 有限连分数
        [1, 1]   # 快速收敛
    ])
    
    im = ax.imshow(feature_matrix, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(np.arange(len(systems)))
    ax.set_yticks(np.arange(len(features)))
    ax.set_xticklabels(systems)
    ax.set_yticklabels(list(features.keys()))
    
    # 添加数值标签
    for i in range(len(features)):
        for j in range(len(systems)):
            ax.text(j, i, f'{feature_matrix[i, j]}', 
                   ha='center', va='center', color='black' if feature_matrix[i, j] < 0.5 else 'white')
    
    ax.set_title('指纹特征对比')
    plt.colorbar(im, ax=ax, label='存在强度')
    plt.tight_layout()
    plt.savefig('figures/fingerprint_comparison.png', bbox_inches='tight')
    print("  ✅ 指纹特征对比图已生成")
    
    print("\n所有图表生成完成！")

if __name__ == "__main__":
    generate_all_figures()