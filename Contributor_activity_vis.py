import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def visualize_contributor_activity(data_dir):
    """
    可视化贡献者活动数据
    :param data_dir: 包含贡献者活动数据的目录
    """
    # 设置样式
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.family'] = 'DejaVu Sans'  # 更通用的字体

    # 创建保存图片的目录
    output_dir = os.path.join(data_dir, "visualization_results")
    os.makedirs(output_dir, exist_ok=True)

    # 读取贡献者活动数据
    contributor_stats_path = os.path.join(data_dir, "contributor_details.csv")
    if not os.path.exists(contributor_stats_path):
        print(f"文件不存在: {contributor_stats_path}")
        return

    contributor_stats = pd.read_csv(contributor_stats_path)

    # 设置图表颜色
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f', '#9b59b6', '#95a5a6']

    # 1. 贡献者贡献分布（饼图）
    plt.figure(figsize=(10, 8))
    plt.pie(contributor_stats['contributions'],
            labels=contributor_stats['login'],
            autopct='%1.1f%%',
            textprops={'fontsize': 8},
            colors=colors)
    plt.title('Contributor Contribution Distribution', pad=20)
    plt.savefig(os.path.join(output_dir, 'contributor_distribution.png'))  # 保存图片
    plt.show()

    # 2. 贡献者贡献排名（柱状图）
    plt.figure(figsize=(12, 6))
    top_contributors = contributor_stats.nlargest(10, 'contributions')  # 取贡献最多的前10名
    sns.barplot(x='login', y='contributions', data=top_contributors, palette=colors)
    plt.title('Top 10 Contributors by Contributions', pad=20)
    plt.xlabel('Contributor')
    plt.ylabel('Number of Contributions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_contributors.png'))  # 保存图片
    plt.show()

    # 3. 贡献者活动趋势（折线图）
    # 假设数据中有日期字段（需要根据实际数据调整）
    if 'date' in contributor_stats.columns:
        plt.figure(figsize=(15, 6))
        contributor_stats['date'] = pd.to_datetime(contributor_stats['date'])
        contributor_stats['month'] = contributor_stats['date'].dt.to_period('M')
        monthly_activity = contributor_stats.groupby('month').size()

        plt.plot(range(len(monthly_activity)), monthly_activity.values,
                 marker='o', linewidth=2, markersize=8, color='#3498db')
        plt.title('Monthly Contributor Activity Trend', pad=20)
        plt.xlabel('Month')
        plt.ylabel('Number of Contributions')
        step = max(len(monthly_activity) // 10, 1)
        plt.xticks(range(0, len(monthly_activity), step),
                   monthly_activity.index[::step],
                   rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'monthly_activity_trend.png'))  # 保存图片
        plt.show()
    else:
        print("数据中没有日期字段，无法绘制活动趋势图。")

    # 4. 贡献者贡献时间分布（24小时）
    if 'date' in contributor_stats.columns:
        plt.figure(figsize=(12, 6))
        contributor_stats['hour'] = pd.to_datetime(contributor_stats['date']).dt.hour
        sns.histplot(data=contributor_stats, x='hour', bins=24, color='#3498db')
        plt.title('Contributor Activity Time Distribution (24-hour)', pad=20)
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Contributions')
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(output_dir, 'contributor_time_distribution.png'))  # 保存图片
        plt.show()
    else:
        print("数据中没有日期字段，无法绘制时间分布图。")


def main():
    # 设置数据目录
    repo = "openfga"
    data_dir = f"D:/test/{repo}_contributor_analysis"

    # 可视化贡献者活动数据
    visualize_contributor_activity(data_dir)


if __name__ == "__main__":
    main()