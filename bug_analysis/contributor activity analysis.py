import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# 加载提交历史数据
commits = pd.read_csv('commits_history.csv')  # 替换为实际数据路径

# 解析提交日期
commits['date'] = pd.to_datetime(commits['date'])

# 按日期分组，统计每一天的提交数
commits_by_date = commits.groupby(commits['date'].dt.date).size()

# 绘制贡献者活动随时间变化的图表
plt.figure(figsize=(10, 6))
commits_by_date.plot(kind='line')
plt.title('贡献者活动随时间变化')
plt.xlabel('日期')
plt.ylabel('提交数')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
