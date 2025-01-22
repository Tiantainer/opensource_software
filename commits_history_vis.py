import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def translate_chinese_to_english(text):
    """将所有中文文本转换为英文"""
    translations = {
        '功能错误': 'Bug Fix',
        '新功能': 'New Feature',
        '文档': 'Documentation',
        '测试': 'Testing',
        '重构': 'Refactor',
        '其他': 'Other',
        '修复': 'Fix',
        '复': 'Fix'  # 处理可能的部分中文
    }

    if pd.isna(text):
        return 'Other'

    for cn, en in translations.items():
        text = str(text).replace(cn, en)
    return text


def clean_data(commit_details):
    """清理数据中的中文"""
    # 转换提交类型
    commit_details['commit_type'] = commit_details['commit_type'].apply(translate_chinese_to_english)
    # 清理提交信息中的中文
    commit_details['message'] = commit_details['message'].apply(translate_chinese_to_english)
    return commit_details


def visualize_git_analysis(data_dir):
    """可视化Github仓库分析结果"""
    # 设置样式
    plt.style.use('seaborn')
    plt.rcParams['font.family'] = 'DejaVu Sans'  # 更通用的字体

    # 读取和清理数据
    commit_details = pd.read_csv(f"{data_dir}/commit_details.csv")
    commit_details = clean_data(commit_details)
    author_stats = pd.read_csv(f"{data_dir}/author_stats.csv")

    # 设置图表颜色
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f', '#9b59b6', '#95a5a6']

    # 1. Contributor Distribution
    plt.figure(figsize=(12, 8))
    plt.pie(author_stats['Commits'],
            labels=author_stats['Author'],
            autopct='%1.1f%%',
            textprops={'fontsize': 8},
            colors=colors)
    plt.title('Contributor Distribution', pad=20)
    plt.show()

    # 2. Commit Type Distribution
    plt.figure(figsize=(10, 8))
    commit_types = commit_details['commit_type'].value_counts()
    plt.pie(commit_types.values,
            labels=commit_types.index,
            autopct='%1.1f%%',
            colors=colors)
    plt.title('Commit Type Distribution', pad=20)
    plt.show()

    # 3. Monthly Commit Trend
    plt.figure(figsize=(15, 6))
    commit_details['date'] = pd.to_datetime(commit_details['date'])
    monthly_commits = commit_details.groupby(commit_details['date'].dt.strftime('%Y-%m')).size()

    plt.plot(range(len(monthly_commits)), monthly_commits.values,
             marker='o', linewidth=2, markersize=8, color='#3498db')
    plt.title('Monthly Commit Trend', pad=20)
    plt.xlabel('Month')
    plt.ylabel('Number of Commits')
    step = max(len(monthly_commits) // 10, 1)
    plt.xticks(range(0, len(monthly_commits), step),
               monthly_commits.index[::step],
               rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # 4. Commit Time Distribution
    plt.figure(figsize=(12, 6))
    commit_details['hour'] = commit_details['date'].dt.hour
    sns.histplot(data=commit_details, x='hour', bins=24, color='#3498db')
    plt.title('Commit Time Distribution (24-hour)', pad=20)
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Commits')
    plt.grid(True, alpha=0.3)
    plt.show()

    # 5. Code Changes Statistics
    plt.figure(figsize=(10, 6))
    changes = {
        'Files Changed': commit_details['files_changed'].sum(),
        'Lines Added': commit_details['insertions'].sum(),
        'Lines Deleted': commit_details['deletions'].sum()
    }
    bars = plt.bar(changes.keys(), changes.values(), color=colors[:3])
    plt.title('Code Changes Statistics', pad=20)
    plt.ylabel('Count')

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{int(height):,}',
                 ha='center', va='bottom')

    plt.grid(True, alpha=0.3)
    plt.show()

    # 6. Top 10 Contributors Activity
    plt.figure(figsize=(15, 8))
    top_authors = author_stats.nlargest(10, 'Commits')['Author']
    author_monthly = pd.crosstab(
        commit_details['date'].dt.strftime('%Y-%m'),
        commit_details['author']
    )[top_authors]

    sns.heatmap(author_monthly,
                cmap='YlOrRd',
                annot=True,
                fmt='d',
                cbar_kws={'label': 'Number of Commits'})
    plt.title('Top 10 Contributors Activity Heatmap', pad=20)
    plt.xlabel('Contributor')
    plt.ylabel('Month')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # 7. Code Changes by Top Contributors
    plt.figure(figsize=(15, 6))
    author_changes = commit_details.groupby('author').agg({
        'insertions': 'sum',
        'deletions': 'sum'
    })
    author_changes = author_changes.nlargest(10, 'insertions')

    ax = author_changes.plot(kind='bar', stacked=True,
                             color=['#2ecc71', '#e74c3c'])
    plt.title('Top 10 Contributors Code Changes', pad=20)
    plt.xlabel('Contributor')
    plt.ylabel('Lines of Code')
    plt.legend(['Added', 'Deleted'])
    plt.xticks(rotation=45, ha='right')

    for c in ax.containers:
        ax.bar_label(c, fmt='%d', label_type='center')

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # 8. Monthly Code Changes Trend
    plt.figure(figsize=(15, 6))
    monthly_changes = commit_details.groupby(commit_details['date'].dt.strftime('%Y-%m')).agg({
        'insertions': 'sum',
        'deletions': 'sum'
    })

    plt.plot(range(len(monthly_changes)), monthly_changes['insertions'],
             label='Added', color='#2ecc71', marker='o')
    plt.plot(range(len(monthly_changes)), monthly_changes['deletions'],
             label='Deleted', color='#e74c3c', marker='o')

    plt.title('Monthly Code Changes Trend', pad=20)
    plt.xlabel('Month')
    plt.ylabel('Lines of Code')
    plt.legend()
    step = max(len(monthly_changes) // 10, 1)
    plt.xticks(range(0, len(monthly_changes), step),
               monthly_changes.index[::step],
               rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def main():
    data_dir = "D:/test/analysis_results"
    visualize_git_analysis(data_dir)


if __name__ == "__main__":
    main()

