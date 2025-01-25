import requests
import pandas as pd
import random
from datetime import datetime
import os
import time
from requests.exceptions import RequestException

class GitHubCodeReviewAnalyzer:
    def __init__(self, owner: str, repo: str):
        """
        初始化代码审查分析器
        :param owner: 仓库所有者
        :param repo: 仓库名称
        """
        self.owner = owner
        self.repo = repo
        self.headers = {}  # 无需 Token
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'
        self.output_dir = f"D:/test/{repo}_code_review_analysis"
        os.makedirs(self.output_dir, exist_ok=True)

    def get_pull_requests(self, state='all'):
        """
        获取仓库的所有 Pull Requests
        :param state: PR 状态（open/closed/all）
        """
        prs = []
        page = 1
        per_page = 100
        while True:
            url = f'{self.base_url}/pulls'
            params = {
                'state': state,
                'page': page,
                'per_page': per_page
            }
            try:
                response = requests.get(url, headers=self.headers, params=params)
                if response.status_code == 403 and "rate limit exceeded" in response.text:
                    print("速率限制已超出，请稍后重试。")
                    break
                if response.status_code != 200:
                    print(f"获取数据失败: {response.status_code}")
                    break
                page_prs = response.json()
                if not page_prs:
                    break
                prs.extend(page_prs)
                page += 1
                time.sleep(1)  # 避免触发 API 限制
            except RequestException as e:
                print(f"请求失败: {e}")
                time.sleep(5)  # 等待 5 秒后重试
                continue
        return prs

    def get_reviews_for_pr(self, pr_number):
        """
        获取单个 PR 的代码审查数据
        :param pr_number: PR 编号
        """
        url = f'{self.base_url}/pulls/{pr_number}/reviews'
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"获取 PR #{pr_number} 的审查数据失败: {response.status_code}")
                return []
            return response.json()
        except RequestException as e:
            print(f"请求失败: {e}")
            return []

    def analyze_code_reviews(self):
        """
        分析代码审查数据
        """
        prs = self.get_pull_requests()
        review_data = []
        for pr in prs:
            pr_number = pr['number']
            reviews = self.get_reviews_for_pr(pr_number)
            for review in reviews:
                review_data.append({
                    'pr_number': pr_number,
                    'reviewer': review['user']['login'],
                    'state': review['state'],
                    'submitted_at': review['submitted_at'],
                    'body': review.get('body', '')
                })
            time.sleep(1)  # 避免触发 API 限制
        return pd.DataFrame(review_data)

    def save_results(self, df):
        """
        保存分析结果
        :param df: 包含代码审查数据的 DataFrame
        """
        # 保存整体数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(self.output_dir, f"code_reviews_{timestamp}.csv")
        df.to_csv(file_path, index=False)
        print(f"整体数据已保存到: {file_path}")

        # 按审查者保存数据
        self.save_reviewer_csv(df)

    def save_reviewer_csv(self, df):
        """
        按审查者生成单独的 CSV 文件
        :param df: 包含代码审查数据的 DataFrame
        """
        reviewers = df['reviewer'].unique()
        for reviewer in reviewers:
            reviewer_data = df[df['reviewer'] == reviewer]
            file_path = os.path.join(self.output_dir, f"{reviewer}_reviews.csv")
            reviewer_data.to_csv(file_path, index=False)
            print(f"审查者 {reviewer} 的数据已保存到: {file_path}")

    def generate_mock_data(self):
        """
        生成模拟代码审查数据
        """
        print("生成模拟代码审查数据...")
        data = []
        reviewers = ['Alice', 'Bob', 'Charlie']
        states = ['APPROVED', 'CHANGES_REQUESTED', 'COMMENTED']
        for i in range(12):  # 模拟12个月的数据
            for reviewer in reviewers:
                for _ in range(10):  # 每个审查者每月 10 条记录
                    month = datetime(2025, i + 1, 1)
                    data.append({
                        'pr_number': random.randint(1, 100),
                        'reviewer': reviewer,
                        'state': random.choice(states),
                        'submitted_at': month.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        'body': f"Review comment by {reviewer}"
                    })

        mock_df = pd.DataFrame(data)
        self.save_results(mock_df)

def main():
    owner = "openfga"
    repo = "openfga"

    analyzer = GitHubCodeReviewAnalyzer(owner, repo)

    # 生成模拟数据
    analyzer.generate_mock_data()

    # 分析真实数据
    # review_df = analyzer.analyze_code_reviews()
    # analyzer.save_results(review_df)

if __name__ == "__main__":
    main()