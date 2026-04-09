# 用户指南

## 项目概述

本项目是"未闭环数学"理论框架下的一个实证案例研究，专注于分析谢尔宾斯基地毯的"编译指纹"。

## 快速开始

### 1. 环境准备
克隆或下载项目

git clone https://github.com/weibihuan/unclosed.git

cd Sierpinski_Experiment

安装依赖

pip install -r requirements.txt

### 2. 运行分析
有几种不同的运行方式：

#### 方式A：快速测试（推荐新手）

python scripts/quick_test.py

#### 方式B：完整分析

bash

python scripts/run_full_analysis.py

#### 方式C：交互式分析

bash

jupyter notebook notebooks/01_primary_analysis.ipynb

#### 方式D：简化分析

bash

python notebooks/run_simple_analysis.py

### 3. 查看结果
分析完成后，结果将保存在：
- `results/` - 分析结果文件
- `data/` - 原始数据文件
- `figures/` - 图表文件（如果生成）

## 项目结构详解

### 根目录文件
- `README.md` - 项目总览
- `requirements.txt` - Python依赖
- `config.yaml` - 配置文件

### src/ - 源代码
- `constants.py` - 常数定义和计算
- `continued_fraction.py` - 连分数分析
- `pslq_analyzer.py` - 整数关系分析
- `visualization.py` - 数据可视化

### scripts/ - 执行脚本
- `run_full_analysis.py` - 完整分析脚本
- `quick_test.py` - 快速测试脚本

### notebooks/ - 交互式分析
- `01_primary_analysis.ipynb` - 主分析笔记本
- `run_simple_analysis.py` - 可直接运行的简化脚本

### data/ - 数据文件
- 存储原始数据和计算结果

### results/ - 分析结果
- 存储分析输出文件

### paper/ - 技术报告
- `technical_report.md` - 完整技术报告

## 配置说明

### 修改配置
编辑 `config.yaml` 文件可调整分析参数：

yaml

precision:

dps: 50                    # 计算精度（十进制位数）

max_cf_terms: 100         # 最大连分数项数

pslq_maxcoeff: 1000       # PSLQ最大系数

analysis:

large_quotient_threshold: 100  # 巨大偏商阈值

### 常见配置调整
1. **提高精度**：增加 `dps` 值
2. **分析更多项**：增加 `max_cf_terms` 值
3. **调整阈值**：修改 `large_quotient_threshold`

## 故障排除

### 常见问题

#### 1. ModuleNotFoundError
**症状**：`ImportError: No module named 'mpmath'`
**解决**：

bash

pip install mpmath

#### 2. 不在正确目录
**症状**：`FileNotFoundError` 或 `ImportError from src`
**解决**：

bash

cd /path/to/Sierpinski_Experiment

pwd  # 确认当前目录

#### 3. Python版本问题
**症状**：语法错误或不兼容
**解决**：需要 Python 3.6+

bash

python --version

### 调试建议

1. **先运行快速测试**：

bash

python scripts/quick_test.py

2. **检查目录结构**：

bash

ls -la

3. **验证Python环境**：

bash

python -c "import mpmath; print('mpmath ok')"

## 扩展项目

### 添加新的分析
1. 在 `src/` 目录创建新的Python模块
2. 在 `scripts/` 创建对应的运行脚本
3. 更新配置文件和文档

### 分析其他分形
修改 `src/constants.py` 中的常数定义，分析其他分形如：
- 科赫雪花
- 曼德博集合
- 门格海绵

## 贡献指南

### 报告问题
1. 在GitHub Issues中描述问题
2. 提供错误信息和运行环境
3. 附上相关代码和配置

### 提交改进
1. Fork项目仓库
2. 创建功能分支
3. 提交Pull Request

## 许可证
MIT License - 详见根目录LICENSE文件

## 联系方式
- GitHub Issues: 项目问题
- 邮件: 未提供

