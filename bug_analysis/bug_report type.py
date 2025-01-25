import matplotlib.pyplot as plt
import pandas as pd

# 加载bug报告数据
bugs = pd.read_csv('bug_issues.csv')  # 替换为实际数据路径

# 统计各类型bug的数量
issue_types = bugs['issue_type'].value_counts()

# 绘制bug类型分布图
plt.figure(figsize=(8, 6))
issue_types.plot(kind='bar', color='skyblue')
plt.title('bug报告类型分布')
plt.xlabel('bug类型')
plt.ylabel('数量')
plt.tight_layout()
plt.show()
