import matplotlib.pyplot as plt
import pandas as pd

# 加载bug报告数据
bugs = pd.read_csv('bug_issues.csv')  # 替换为实际数据路径

# 将日期字段转为日期时间类型
bugs['created_at'] = pd.to_datetime(bugs['created_at'])
bugs['closed_at'] = pd.to_datetime(bugs['closed_at'])

# 计算修复时间
bugs['fix_time'] = (bugs['closed_at'] - bugs['created_at']).dt.days

# 绘制bug严重性与修复时间的关系图
plt.figure(figsize=(10, 6))
plt.scatter(bugs['severity'], bugs['fix_time'])
plt.title('bug严重性与修复时间的关系')
plt.xlabel('严重性')
plt.ylabel('修复时间（天数）')
plt.tight_layout()
plt.show()
