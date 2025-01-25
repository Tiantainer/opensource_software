import requests
import pandas as pd
from datetime import datetime
import os
import time
from collections import Counter

class GitHubIssueCommentAnalyzer:
    def __init__(self, owner: str, repo: str):
        """
        初始化 Issue 评论分析器
        :param owner: 仓库所有者
        :param repo: 仓库名称
        """
        self.owner = owner
        self.repo = repo
        self.headers = {}  # 无需 Token
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'
        self.output_dir = f"D:/test/{repo}_issue_comments_analysis"
        os.makedirs(self.output_dir, exist_ok=True)

    def get_issue_comments(self):
        """
        获取仓库的所有 Issue 评论
        """
        print(f"开始获取 {self.owner}/{self.repo} 的 Issue 评论...")
        comments = []
        page = 1
        per_page = 100

        while True:
            print(f"正在获取第 {page} 页...")
            url = f'{self.base_url}/issues/comments'
            params = {
                'page': page,
                'per_page': per_page
            }
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code != 200:
                print(f"获取数据失败: {response.status_code}")
                break

            page_comments = response.json()
            if not page_comments:
                break

            comments.extend(page_comments)
            page += 1
            time.sleep(1)  # 避免触发 API 限制

        print(f"共获取到 {len(comments)} 条 Issue 评论")
        return comments

    def analyze_issue_comments(self):
        """
        分析 Issue 评论数据
        """
        comments = self.get_issue_comments()
        comment_data = []
        stats = {
            'total_comments': len(comments),
            'commenters': Counter(),
            'comments_per_issue': Counter(),
            'comments_by_month': Counter(),
            'comments_by_hour': Counter()
        }

        for comment in comments:
            try:
                created_at = datetime.strptime(comment['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                comment_info = {
                    'issue_number': comment['issue_url'].split('/')[-1],
                    'commenter': comment['user']['login'],
                    'created_at': created_at,
                    'body': comment['body']
                }
                comment_data.append(comment_info)

                # 更新统计信息
                stats['commenters'][comment_info['commenter']] += 1
                stats['comments_per_issue'][comment_info['issue_number']] += 1
                stats['comments_by_month'][created_at.strftime('%Y-%m')] += 1
                stats['comments_by_hour'][created_at.hour] += 1

            except Exception as e:
                print(f"处理评论时出错: {str(e)}")
                continue

        return stats, pd.DataFrame(comment_data)

    def save_results(self, stats, df):
        """
        保存分析结果
        """
        # 保存评论数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(self.output_dir, f"issue_comments_{timestamp}.csv")
        df.to_csv(file_path, index=False)
        print(f"评论数据已保存到: {file_path}")

        # 保存统计数据
        stats_df = pd.DataFrame({
            'total_comments': [stats['total_comments']],
            'unique_commenters': [len(stats['commenters'])],
            'most_active_commenter': [stats['commenters'].most_common(1)[0][0]],
            'most_commented_issue': [stats['comments_per_issue'].most_common(1)[0][0]]
        })
        stats_df.to_csv(os.path.join(self.output_dir, "summary.csv"), index=False)

        # 保存评论者数据
        pd.DataFrame(stats['commenters'].most_common(), columns=['Commenter', 'Count']).to_csv(
            os.path.join(self.output_dir, "commenters.csv"), index=False
        )

        # 保存月度评论数据
        pd.DataFrame(stats['comments_by_month'].items(), columns=['Month', 'Count']).to_csv(
            os.path.join(self.output_dir, "comments_by_month.csv"), index=False
        )

        # 保存小时评论数据
        pd.DataFrame(stats['comments_by_hour'].items(), columns=['Hour', 'Count']).to_csv(
            os.path.join(self.output_dir, "comments_by_hour.csv"), index=False
        )

def main():
    owner = "openfga"
    repo = "openfga"

    analyzer = GitHubIssueCommentAnalyzer(owner, repo)
    stats, df = analyzer.analyze_issue_comments()
    analyzer.save_results(stats, df)

if __name__ == "__main__":
    main()