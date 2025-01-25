import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from datetime import datetime
import time


class GitHubContributorActivityAnalyzer:
    def __init__(self, owner: str, repo: str, token: str = None):
        """
        初始化GitHub贡献者活动分析器
        :param owner: 仓库所有者
        :param repo: 仓库名称
        :param token: GitHub API token（可选）
        """
        self.owner = owner
        self.repo = repo
        self.headers = {'Authorization': f'token {token}'} if token else {}
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'

    def get_contributors_activity(self):
        """获取贡献者活动数据"""
        print(f"开始获取 {self.owner}/{self.repo} 的贡献者活动数据...")
        contributors_activity = []
        url = f'{self.base_url}/contributors'
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"获取数据失败: {response.status_code}")
            return []

        contributors_activity = response.json()
        print(f"共获取到 {len(contributors_activity)} 个贡献者")
        return contributors_activity

    def analyze_contributors_activity(self):
        """分析贡献者活动"""
        contributors_activity = self.get_contributors_activity()

        # 初始化统计数据
        stats = {
            'total_contributors': len(contributors_activity),
            'contributors': Counter(),
            'activity_by_month': Counter(),
            'contributor_activity': Counter()
        }

        contributor_data = []

        for contributor in contributors_activity:
            try:
                contributor_info = self._parse_contributor(contributor)
                # 更新统计信息
                self._update_stats(stats, contributor_info)
                contributor_data.append(contributor_info)

            except Exception as e:
                print(f"处理贡献者 {contributor['login']} 时出错: {str(e)}")
                continue

        print(f"\n成功处理 {len(contributor_data)} 个贡献者活动数据")
        return stats, pd.DataFrame(contributor_data)

    def _parse_contributor(self, contributor):
        """解析单个贡献者的信息"""
        login = contributor['login']
        contributions = contributor['contributions']
        contributor_info = {
            'login': login,
            'contributions': contributions
        }

        return contributor_info

    def _update_stats(self, stats, contributor_info):
        """更新统计信息"""
        try:
            stats['contributors'][contributor_info['login']] += contributor_info['contributions']
            stats['contributor_activity'][contributor_info['login']] += contributor_info['contributions']
        except Exception as e:
            print(f"更新统计信息时出错: {str(e)}")

    def visualize_contributor_activity(self, data_dir):
        """可视化Github贡献者活动数据"""
        # 设置样式
        plt.style.use('seaborn')
        plt.rcParams['font.family'] = 'DejaVu Sans'  # 更通用的字体

        # 读取和清理数据
        contributor_stats = pd.read_csv(f"{data_dir}/contributor_stats.csv")
        contributor_stats = self.clean_data(contributor_stats)

        # 设置图表颜色
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f', '#9b59b6', '#95a5a6']

        # 1. 贡献者分布
        plt.figure(figsize=(12, 8))
        plt.pie(contributor_stats['contributions'],
                labels=contributor_stats['login'],
                autopct='%1.1f%%',
                textprops={'fontsize': 8},
                colors=colors)
        plt.title('Contributor Distribution', pad=20)
        plt.show()

        # 2. 贡献者活动趋势
        plt.figure(figsize=(15, 6))
        contributor_stats['month'] = pd.to_datetime(contributor_stats['date']).dt.to_period('M')
        monthly_activity = contributor_stats.groupby(contributor_stats['month']).size()

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
        plt.show()

        # 3. 贡献者时间分布
        plt.figure(figsize=(12, 6))
        contributor_stats['hour'] = pd.to_datetime(contributor_stats['date']).dt.hour
        sns.histplot(data=contributor_stats, x='hour', bins=24, color='#3498db')
        plt.title('Contributor Activity Time Distribution (24-hour)', pad=20)
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Contributions')
        plt.grid(True, alpha=0.3)
        plt.show()

        # 4. 代码贡献统计
        plt.figure(figsize=(10, 6))
        changes = {
            'Total Contributions': contributor_stats['contributions'].sum(),
        }
        bars = plt.bar(changes.keys(), changes.values(), color=colors[:3])
        plt.title('Code Contributions Statistics', pad=20)
        plt.ylabel('Count')

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{int(height):,}',
                     ha='center', va='bottom')

        plt.grid(True, alpha=0.3)
        plt.show()

    def clean_data(self, contributor_stats):
        """清理数据中的中文"""
        # 清理贡献者活动中的中文信息，如果需要的话
        return contributor_stats

    def save_results(self, stats, df, output_dir):
        """保存分析结果"""
        os.makedirs(output_dir, exist_ok=True)

        # 保存原始数据
        df.to_csv(f"{output_dir}/contributor_details.csv", index=False)

        # 保存统计数据
        summary_data = {
            'total_contributors': stats['total_contributors'],
            'avg_contributions': sum(stats['contributors'].values()) / len(stats['contributors']) if stats['contributors'] else 0
        }
        pd.DataFrame([summary_data]).to_csv(f"{output_dir}/summary.csv", index=False)

        # 保存各类统计数据
        for name, data in {
            'contributors': stats['contributors'],
            'activity_by_month': stats['activity_by_month'],
            'contributor_activity': stats['contributor_activity']
        }.items():
            pd.DataFrame(list(data.items()), columns=['Contributor', 'Activity Count']).to_csv(f"{output_dir}/{name}.csv", index=False)

        print(f"\n分析结果已保存到: {output_dir}")


def main():
    data_dir = "D:/test/analysis_results"
    owner = "openfga"
    repo = "openfga"
    token = "your_github_token_here"  # 在此处插入GitHub的token

    analyzer = GitHubContributorActivityAnalyzer(owner, repo, token)

    # 执行贡献者活动分析
    stats, df = analyzer.analyze_contributors_activity()

    # 可视化贡献者活动数据
    analyzer.visualize_contributor_activity(data_dir)

    # 保存结果
    output_dir = f"D:/test/{repo}_contributor_analysis"
    analyzer.save_results(stats, df, output_dir)


if __name__ == "__main__":
    main()
