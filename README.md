# 开源软件基础项目

本项目包含六个 Python 文件，用于分析和可视化 GitHub 仓库的提交历史、Bug 报告和 Pull Request（PR）数据。以下是每个文件的详细说明以及如何运行这些代码的指南。

## 文件结构

```
.
├── bug_issues.py            # 分析 GitHub 仓库的 Bug 报告
├── bug_issues_vis.py        # 可视化 Bug 报告分析结果
├── commits_history.py       # 分析 Git 仓库的提交历史
├── commits_history_vis.py   # 可视化提交历史分析结果
├── Pull_request.py          # 分析 GitHub 仓库的 Pull Request
└── Pull_request_vis.py      # 可视化 Pull Request 分析结果
```

## 文件功能说明

### 1. `bug_issues.py`
- **功能**: 分析 GitHub 仓库的 Bug 报告。
- **主要功能**:
  - 获取指定仓库的所有 Bug 报告。
  - 统计 Bug 的状态、类型、标签、报告者等信息。
  - 计算 Bug 的平均修复时间。
  - 保存分析结果为 CSV 文件。
- **依赖库**: `requests`, `pandas`, `collections`, `datetime`, `os`, `time`

### 2. `bug_issues_vis.py`
- **功能**: 可视化 Bug 报告分析结果。
- **主要功能**:
  - 绘制 Bug 类型分布饼图。
  - 绘制受影响组件分布饼图。
  - 绘制 Bug 状态分布饼图。
  - 绘制月度 Bug 趋势折线图。
  - 绘制报告者贡献柱状图（前 10 名）。
- **依赖库**: `pandas`, `matplotlib`

### 3. `commits_history.py`
- **功能**: 分析 Git 仓库的提交历史。
- **主要功能**:
  - 获取仓库的提交记录。
  - 统计提交的作者、提交类型、代码变更等信息。
  - 分析提交的时间分布和月度趋势。
  - 保存分析结果为 CSV 文件。
- **依赖库**: `gitpython`, `pandas`, `collections`, `os`

### 4. `commits_history_vis.py`
- **功能**: 可视化 Git 仓库的提交历史分析结果。
- **主要功能**:
  - 绘制贡献者分布饼图。
  - 绘制提交类型分布饼图。
  - 绘制月度提交趋势折线图。
  - 绘制提交时间分布直方图。
  - 绘制代码变更统计柱状图。
  - 绘制贡献者活动热力图。
  - 绘制月度代码变更趋势图。
- **依赖库**: `pandas`, `matplotlib`, `seaborn`

### 5. `Pull_request.py`
- **功能**: 分析 GitHub 仓库的 Pull Request。
- **主要功能**:
  - 获取指定仓库的开放 PR。
  - 统计 PR 的作者、标签、代码变更等信息。
  - 计算 PR 的平均年龄、平均修改文件数、平均增加/删除行数。
  - 保存分析结果为 CSV 文件。
- **依赖库**: `requests`, `pandas`, `collections`, `datetime`, `os`, `time`

### 6. `Pull_request_vis.py`
- **功能**: 可视化 Pull Request 分析结果。
- **主要功能**:
  - 绘制 PR 年龄分布直方图。
  - 绘制作者分布饼图。
  - 绘制标签分布条形图。
  - 绘制 PR 大小分布直方图。
  - 绘制评审活动散点图。
  - 绘制 PR 创建时间线。
  - 绘制变更热力图。
- **依赖库**: `pandas`, `matplotlib`, `seaborn`, `os`

---

## 运行说明

### 1. 安装依赖
确保已安装以下 Python 库：
```bash
pip install requests pandas gitpython matplotlib seaborn
```

### 2. 配置 GitHub Token
部分脚本需要 GitHub API Token 才能运行。请将以下代码中的 `token` 替换为你自己的 GitHub Token：
```python
token = 'your_github_token_here'
```

### 3. 运行脚本

#### 运行 `bug_issues.py`
1. 打开终端或命令行。
2. 导航到项目目录。
3. 运行以下命令：
   ```bash
   python bug_issues.py
   ```
4. 分析结果将保存到 `D:/test/openfga_bug_analysis` 目录中。

#### 运行 `bug_issues_vis.py`
1. 确保已经运行过 `bug_issues.py` 并生成了分析结果。
2. 运行以下命令：
   ```bash
   python bug_issues_vis.py
   ```
3. 可视化结果将通过 `matplotlib` 显示。

#### 运行 `commits_history.py`
1. 打开终端或命令行。
2. 导航到项目目录。
3. 运行以下命令：
   ```bash
   python commits_history.py
   ```
4. 分析结果将保存到 `D:/test/analysis_results` 目录中。

#### 运行 `commits_history_vis.py`
1. 确保已经运行过 `commits_history.py` 并生成了分析结果。
2. 运行以下命令：
   ```bash
   python commits_history_vis.py
   ```
3. 可视化结果将通过 `matplotlib` 显示。

#### 运行 `Pull_request.py`
1. 打开终端或命令行。
2. 导航到项目目录。
3. 运行以下命令：
   ```bash
   python Pull_request.py
   ```
4. 分析结果将保存到 `D:/test/openfga_open_pr_analysis` 目录中。

#### 运行 `Pull_request_vis.py`
1. 确保已经运行过 `Pull_request.py` 并生成了分析结果。
2. 运行以下命令：
   ```bash
   python Pull_request_vis.py
   ```
3. 可视化结果将通过 `matplotlib` 显示。

---

## 注意事项
1. **路径配置**: 确保代码中的路径（如 `D:/test/openfga`）与你的本地环境一致。
2. **GitHub API 限制**: 由于 GitHub API 有速率限制，建议在脚本中增加 `time.sleep()` 以避免触发限制。
3. **数据保存**: 分析结果将保存为 CSV 文件，路径为 `D:/test/analysis_results` 或 `D:/test/openfga_bug_analysis`。

---

## 许可证
本项目采用 [MIT 许可证](LICENSE)。

---

希望这个 `README.md` 文档能帮助你更好地理解和使用这些代码！如果有任何问题，请随时联系。
