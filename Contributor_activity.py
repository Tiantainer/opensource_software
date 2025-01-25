import requests
import pandas as pd
from collections import Counter, defaultdict
from datetime import datetime
import os
import time

class GitHubContributorAnalyzer:
    def __init__(self, owner: str, repo: str, token: str = None):
        """
        初始化贡献者活动分析器
        :param owner: 仓库所有者
        :param repo: 仓库名称
        :param token: GitHub API token（可选）
        """
        self.owner = owner
        self.repo = repo
        self.headers = {'Authorization': f'token {token}'} if token else {}
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'

    def get_contributors(self):
        """获取仓库的所有贡献者"""
        print(f"开始获取 {self.owner}/{self.repo} 的贡献者活动...")

        contributors = []
        url = f'{self.base_url}/contributors'
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"获取数据失败: {response.status_code}")
            return []

        contributors = response.json()
        print(f"共获取到 {len(contributors)} 个贡献者")
        return contributors

    def analyze_contributors(self):
        """分析贡献者活动"""
        contributors = self.get_contributors()

        # 初始化统计数据
        stats = {
            'total_contributors': len(contributors),
            'contributors': Counter(),
            'activity_by_month': defaultdict(int),
            'contributor_activity': defaultdict(int)
        }

        contributor_data = []

        for contributor in contributors:
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
            'contributions': contributions,
        }

        return contributor_info

    def _update_stats(self, stats, contributor_info):
        """更新统计信息"""
        try:
            stats['contributors'][contributor_info['login']] += contributor_info['contributions']
            
            # 更新贡献者的活动
            stats['contributor_activity'][contributor_info['login']] += contributor_info['contributions']
            
        except Exception as e:
            print(f"更新统计信息时出错: {str(e)}")

    def print_analysis(self, stats):
        """打印贡献者分析结果"""
        print("\n=== 贡献者活动分析结果 ===")
        print(f"\n总贡献者数: {stats['total_contributors']}")

        # 贡献者活动分布
        if stats['contributors']:
            print("\n贡献者活动分布:")
            for contributor, contributions in stats['contributors'].items():
                percentage = contributions / sum(stats['contributors'].values()) * 100
                print(f"{contributor}: {contributions} 次贡献 ({percentage:.1f}%)")

        # 贡献者活动趋势
        if stats['activity_by_month']:
            print("\n贡献者活动趋势 (按月统计):")
            for month, count in sorted(stats['activity_by_month'].items()):
                print(f"{month}: {count} 次贡献")

    def save_results(self, stats, df, output_dir):
        """保存贡献者分析结果"""
        os.makedirs(output_dir, exist_ok=True)

        # 保存原始数据
        df.to_csv(f"{output_dir}/contributor_details.csv", index=False)

        # 保存统计数据
        summary_data = {
            'total_contributors': stats['total_contributors'],
            'avg_contributions': sum(stats['contributors'].values()) / len(stats['contributors']) if stats['contributors'] else 0
        }
        pd.DataFrame([summary_data]).to_csv(f"{output_dir}/summary.csv", index=False)

        # 保存贡献者活动数据
        for name, data in {
            'contributors': stats['contributors'],
            'activity_by_month': stats['activity_by_month'],
            'contributor_activity': stats['contributor_activity']
        }.items():
            pd.DataFrame(list(data.items()), columns=['Contributor', 'Activity Count']).to_csv(f"{output_dir}/{name}.csv", index=False)

        print(f"\n分析结果已保存到: {output_dir}")


def main():
    # 设置要分析的仓库
    owner = "openfga"
    repo = "openfga"

    # 创建分析器
    analyzer = GitHubContributorAnalyzer(owner, repo)

    # 执行分析
    stats, df = analyzer.analyze_contributors()

    # 打印分析结果
    analyzer.print_analysis(stats)

    # 保存结果
    output_dir = f"D:/test/{repo}_contributor_analysis"
    analyzer.save_results(stats, df, output_dir)


if __name__ == "__main__":
    main()
