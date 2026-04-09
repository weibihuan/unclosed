# 分析笔记本说明

## 可用笔记本

### 1. `01_primary_analysis.ipynb` - 主分析笔记本
**功能**：完整的交互式分析，包括常数计算、连分数分析、代数关系验证
**运行方式**：
bash

cd /path/to/Sierpinski_Experiment

jupyter notebook notebooks/01_primary_analysis.ipynb

复制
**或使用以下命令直接运行**：

bash

cd /path/to/Sierpinski_Experiment

jupyter nbconvert --to notebook --execute notebooks/01_primary_analysis.ipynb --output results/primary_output.ipynb

复制
### 2. `run_simple_analysis.py` - 简化分析脚本
**功能**：不需要Jupyter环境的简化分析脚本
**运行方式**：

bash

cd /path/to/Sierpinski_Experiment

python notebooks/run_simple_analysis.py

## 运行前提

### 1. 确保目录结构正确

Sierpinski_Experiment/  ← 必须在此目录下运行

├── src/

├── notebooks/

├── results/

└── ...

### 2. 安装依赖

bash

pip install mpmath

如果使用Jupyter Notebook：

pip install jupyter numpy matplotlib

### 3. 检查Python版本
需要 Python 3.6+：

bash

python --version

## 故障排除

### 问题1：ModuleNotFoundError
**解决**：确保在项目根目录运行，而不是在notebooks目录

### 问题2：ImportError from src
**解决**：运行 `run_simple_analysis.py`，它不依赖src模块

### 问题3：mpmath未安装
**解决**：

bash

pip install mpmath


## 输出文件
分析结果会保存到 `results/` 目录：
- `primary_analysis.json` - JSON格式结果
- `primary_analysis.txt` - 文本格式结果
- `simple_analysis.txt` - 简化分析结果