# 开源软件基础项目

本项目包含12个 Python 文件，用于分析和可视化 GitHub 仓库的提交历史、Bug 报告、Pull Request（PR）数据、贡献者活动、代码质量以及代码审查数据。以下是每个文件的详细说明以及如何运行这些代码的指南。

## 文件结构

```
.
├── bug_issues.py                # 分析 GitHub 仓库的 Bug 报告
├── bug_issues_vis.py            # 可视化 Bug 报告分析结果
├── commits_history.py           # 分析 Git 仓库的提交历史
├── commits_history_vis.py       # 可视化提交历史分析结果
├── Pull_request.py              # 分析 GitHub 仓库的 Pull Request
├── Pull_request_vis.py          # 可视化 Pull Request 分析结果
├── contributor_activity.py      # 分析 GitHub 仓库的贡献者活动
├── Contributor_activity_vis.py  # 可视化贡献者活动分析结果
├── Code_quality_analyzer.py     # 生成模拟的代码质量数据
├── Code_quality_visualizer.py   # 分析和可视化代码质量数据
├── code_review.py               # 分析 GitHub 仓库的代码审查数据
├── code_review_vis.py           # 可视化代码审查分析结果
├── issue_comments.py            # 分析Git仓库的问题评论数据
└── issue_comments_vis.py        # 可视化问题评论数据结果
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

### 7. `contributor_activity.py`
- **功能**: 分析 GitHub 仓库的贡献者活动。
- **主要功能**:
  - 获取指定仓库的贡献者列表。
  - 统计贡献者的提交次数、活动趋势等信息。
  - 保存分析结果为 CSV 文件。
- **依赖库**: `requests`, `pandas`, `collections`, `datetime`, `os`, `time`

### 8. `Contributor_activity_vis.py`
- **功能**: 可视化贡献者活动分析结果。
- **主要功能**:
  - 绘制贡献者贡献分布饼图。
  - 绘制贡献者贡献排名柱状图（前 10 名）。
  - 绘制贡献者活动趋势折线图。
  - 绘制贡献者活动时间分布直方图（24 小时）。
- **依赖库**: `pandas`, `matplotlib`, `seaborn`

### 9. `Code_quality_analyzer.py`
- **功能**: 生成模拟的代码质量数据。
- **主要功能**:
  - 生成模拟的代码复杂度、问题数量、测试覆盖率等数据。
  - 按模块生成单独的 CSV 文件。
  - 保存模拟数据为 CSV 文件。
- **依赖库**: `pandas`, `os`, `datetime`, `random`

### 10. `Code_quality_visualizer.py`
- **功能**: 分析和可视化代码质量数据。
- **主要功能**:
  - 分析代码质量数据并生成模块统计、贡献者统计、问题类型分布等。
  - 保存分析结果为 CSV 文件。
- **依赖库**: `pandas`, `os`

### 11. `code_review.py`
- **功能**: 分析 GitHub 仓库的代码审查数据。
- **主要功能**:
  - 获取指定仓库的 Pull Request 审查数据。
  - 统计审查者、审查状态、审查时间等信息。
  - 生成模拟的代码审查数据。
  - 保存分析结果为 CSV 文件。
- **依赖库**: `requests`, `pandas`, `random`, `datetime`, `os`, `time`

### 12. `code_review_vis.py`
- **功能**: 可视化代码审查分析结果。
- **主要功能**:
  - 绘制审查状态分布条形图。
  - 绘制审查者活动分布柱状图（前 10 名）。
  - 绘制审查时间趋势折线图。
  - 绘制审查评论长度分布直方图。
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

#### 运行 `contributor_activity.py`
1. 打开终端或命令行。
2. 导航到项目目录。
3. 运行以下命令：
   ```bash
   python contributor_activity.py
   ```
4. 分析结果将保存到 `D:/test/openfga_contributor_analysis` 目录中。

#### 运行 `Contributor_activity_vis.py`
1. 确保已经运行过 `contributor_activity.py` 并生成了分析结果。
2. 运行以下命令：
   ```bash
   python Contributor_activity_vis.py
   ```
3. 可视化结果将通过 `matplotlib` 显示。

#### 运行 `Code_quality_analyzer.py`
1. 打开终端或命令行。
2. 导航到项目目录。
3. 运行以下命令：
   ```bash
   python Code_quality_analyzer.py
   ```
4. 模拟数据将保存到 `D:/test/openfga_code_quality` 目录中。

#### 运行 `Code_quality_visualizer.py`
1. 确保已经运行过 `Code_quality_analyzer.py` 并生成了模拟数据。
2. 运行以下命令：
   ```bash
   python Code_quality_visualizer.py
   ```
3. 分析结果将保存到 `D:/test/openfga_code_quality/analysis_results` 目录中。

#### 运行 `code_review.py`
1. 打开终端或命令行。
2. 导航到项目目录。
3. 运行以下命令：
   ```bash
   python code_review.py
   ```
4. 分析结果将保存到 `D:/test/openfga_code_review_analysis` 目录中。

#### 运行 `code_review_vis.py`
1. 确保已经运行过 `code_review.py` 并生成了分析结果。
2. 运行以下命令：
   ```bash
   python code_review_vis.py
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
