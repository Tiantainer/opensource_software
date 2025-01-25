import matplotlib.pyplot as plt
import pandas as pd

# 加载bug报告数据
bugs = pd.read_csv('bug_issues.csv')  # 替换为实际数据路径

# 将日期字段转为日期时间类型
bugs['created_at'] = pd.to_datetime(bugs['created_at'])
bugs['closed_at'] = pd.to_datetime(bugs['closed_at'])

# 按月份统计打开和关闭的bug数量
bugs['month'] = bugs['created_at'].dt.to_period('M')
issues_by_month = bugs.groupby('month').agg({'created_at': 'count', 'closed_at': 'count'})

# 绘制每月打开与关闭的bug数量
plt.figure(figsize=(10, 6))
issues_by_month['created_at'].plot(kind='line', label='打开的bug', color='blue')
issues_by_month['closed_at'].plot(kind='line', label='解决的bug', color='red')
plt.title('问题解决率')
plt.xlabel('月份')
plt.ylabel('bug数量')
plt.legend()
plt.tight_layout()
plt.show()
