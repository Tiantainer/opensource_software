import requests
import pandas as pd
from collections import Counter, defaultdict
from datetime import datetime
import os
import time
# 代码中要用到token，一定要换成自己的token才能运行

class GitHubPRAnalyzer:
    def __init__(self, owner: str, repo: str, token: str = None):
        """
        初始化GitHub PR分析器
        :param owner: 仓库所有者
        :param repo: 仓库名称
        :param token: GitHub API token（可选）
        """
        self.owner = owner
        self.repo = repo
        self.headers = {'Authorization': f'token {token}'} if token else {}
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'

    def get_pull_request_details(self, pr_number):
        """获取单个PR的详细信息"""
        url = f'{self.base_url}/pulls/{pr_number}'
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"获取PR #{pr_number} 详细信息失败: {response.status_code}")
            return None

        return response.json()

    def get_open_pull_requests(self, state='open'):
        """获取仓库的开放PR"""
        print(f"开始获取 {self.owner}/{self.repo} 的开放Pull Requests...")
        prs = []
        page = 1
        per_page = 100

        while True:
            print(f"正在获取第 {page} 页...")
            url = f'{self.base_url}/pulls'
            params = {
                'state': 'open',  # 只获取开放的PR
                'page': page,
                'per_page': per_page
            }

            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code != 200:
                print(f"获取数据失败: {response.status_code}")# !=200即未成功
                break

            page_prs = response.json()
            if not page_prs:
                break

            # 获取每个PR的详细信息
            for pr in page_prs:
                pr_number = pr['number']
                print(f"获取PR #{pr_number} 的详细信息...")
                pr_details = self.get_pull_request_details(pr_number)
                if pr_details:
                    prs.append(pr_details)
                time.sleep(1)  # 避免触发API限制

            page += 1

        print(f"共获取到 {len(prs)} 个开放的Pull Requests")
        return prs

    def _parse_pr(self, pr):
        """解析单个PR的信息"""
        try:
            created_at = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            closed_at = None
            if pr['closed_at']:
                closed_at = datetime.strptime(pr['closed_at'], '%Y-%m-%dT%H:%M:%SZ')

            info = {
                'number': pr['number'],
                'title': pr['title'],
                'state': pr['state'],
                'created_at': created_at,
                'closed_at': closed_at,
                'author': pr['user']['login'],
                'labels': [label['name'] for label in pr['labels']],
                'changed_files': pr.get('changed_files', 0),
                'additions': pr.get('additions', 0),
                'deletions': pr.get('deletions', 0),
                'merged': pr.get('merged', False),
                'merged_by': pr['merged_by']['login'] if pr.get('merged_by') else None,
                'review_comments': pr.get('review_comments', 0),
                'url': pr['html_url'],
                'branch': pr['head']['ref'],
                'base_branch': pr['base']['ref'],
                'body': pr.get('body', ''),
                'draft': pr.get('draft', False)
            }

            # 计算PR年龄
            info['age_days'] = (datetime.now() - created_at).days

            # 解析评论数
            info['comment_count'] = pr.get('comments', 0)

            # 解析审查状态
            info['review_state'] = 'pending'
            if pr.get('merged'):
                info['review_state'] = 'merged'
            elif pr.get('draft'):
                info['review_state'] = 'draft'

            return info

        except Exception as e:
            print(f"解析PR #{pr['number']} 时出错: {str(e)}")
            return None

    def analyze_open_prs(self):
        """分析开放的PR"""
        prs = self.get_open_pull_requests()

        # 初始化统计数据
        stats = {
            'total_open_prs': len(prs),
            'authors': Counter(),
            'labels': Counter(),
            'age_days': [],
            'changed_files': [],
            'additions': [],
            'deletions': [],
            'review_states': Counter(),
            'branches': Counter(),
            'base_branches': Counter(),
            'draft_count': 0,
            'review_comments': [],
            'comment_count': []
        }

        pr_data = []

        for pr in prs:
            try:
                # 解析PR数据
                pr_info = self._parse_pr(pr)
                if pr_info:
                    # 更新统计信息
                    stats['authors'][pr_info['author']] += 1
                    for label in pr_info['labels']:
                        stats['labels'][label] += 1

                    stats['age_days'].append(pr_info['age_days'])
                    stats['changed_files'].append(pr_info['changed_files'])
                    stats['additions'].append(pr_info['additions'])
                    stats['deletions'].append(pr_info['deletions'])
                    stats['review_states'][pr_info['review_state']] += 1
                    stats['branches'][pr_info['branch']] += 1
                    stats['base_branches'][pr_info['base_branch']] += 1

                    if pr_info['draft']:
                        stats['draft_count'] += 1

                    stats['review_comments'].append(pr_info['review_comments'])
                    stats['comment_count'].append(pr_info['comment_count'])

                    pr_data.append(pr_info)

            except Exception as e:
                print(f"处理PR #{pr['number']} 时出错: {str(e)}")
                continue

        return stats, pd.DataFrame(pr_data)

    def print_open_pr_analysis(self, stats):
        """打印开放PR的分析结果"""
        print("\n=== 开放Pull Request分析 ===")
        print(f"\n当前开放PR数: {stats['total_open_prs']}")
        print(f"草稿PR数: {stats['draft_count']}")

        if stats['age_days']:
            avg_age = sum(stats['age_days']) / len(stats['age_days'])
            max_age = max(stats['age_days'])
            print(f"\nPR年龄统计:")
            print(f"平均开放时间: {avg_age:.1f} 天")
            print(f"最长开放时间: {max_age} 天")

        print("\n活跃贡献者:")
        for author, count in stats['authors'].most_common():
            percentage = count / stats['total_open_prs'] * 100
            print(f"{author}: {count} PRs ({percentage:.1f}%)")

        if stats['labels']:
            print("\n标签统计:")
            for label, count in stats['labels'].most_common():
                percentage = count / stats['total_open_prs'] * 100
                print(f"{label}: {count} ({percentage:.1f}%)")

        print("\n目标分支统计:")
        for branch, count in stats['base_branches'].most_common():
            percentage = count / stats['total_open_prs'] * 100
            print(f"{branch}: {count} PRs ({percentage:.1f}%)")

        if stats['changed_files']:
            avg_files = sum(stats['changed_files']) / len(stats['changed_files'])
            avg_additions = sum(stats['additions']) / len(stats['additions'])
            avg_deletions = sum(stats['deletions']) / len(stats['deletions'])
            print(f"\n代码变更统计:")
            print(f"平均修改文件数: {avg_files:.1f}")
            print(f"平均增加行数: {avg_additions:.1f}")
            print(f"平均删除行数: {avg_deletions:.1f}")

        if stats['review_comments']:
            avg_comments = sum(stats['review_comments']) / len(stats['review_comments'])
            print(f"\n评论统计:")
            print(f"平均评论数: {avg_comments:.1f}")


def save_results(stats, df, output_dir):
    """保存分析结果"""
    os.makedirs(output_dir, exist_ok=True)

    # 保存PR详细数据
    df.to_csv(f"{output_dir}/open_pr_details.csv", index=False)

    # 保存统计数据
    summary_data = {
        'total_open_prs': stats['total_open_prs'],
        'draft_prs': stats['draft_count'],
        'avg_age_days': sum(stats['age_days']) / len(stats['age_days']) if stats['age_days'] else 0,
        'max_age_days': max(stats['age_days']) if stats['age_days'] else 0,
        'avg_changed_files': sum(stats['changed_files']) / len(stats['changed_files']) if stats['changed_files'] else 0,
        'avg_additions': sum(stats['additions']) / len(stats['additions']) if stats['additions'] else 0,
        'avg_deletions': sum(stats['deletions']) / len(stats['deletions']) if stats['deletions'] else 0,
        'avg_comments': sum(stats['review_comments']) / len(stats['review_comments']) if stats['review_comments'] else 0
    }
    pd.DataFrame([summary_data]).to_csv(f"{output_dir}/summary.csv", index=False)

    # 保存各类统计数据
    for name, data in {
        'authors': stats['authors'],
        'labels': stats['labels'],
        'branches': stats['branches'],
        'base_branches': stats['base_branches'],
        'review_states': stats['review_states']
    }.items():
        pd.DataFrame(list(data.items()),
                     columns=['Name', 'Count']).to_csv(f"{output_dir}/{name}.csv", index=False)

    print(f"\n分析结果已保存到: {output_dir}")


def main():
    owner = "openfga"
    repo = "openfga"

    # GitHub token，运行时一定要换成自己的token，token在GitHub上生成
    token = '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'  # 替换为你的GitHub token

    # 创建分析器
    analyzer = GitHubPRAnalyzer(owner, repo, token)

    # 分析开放的PR
    stats, df = analyzer.analyze_open_prs()

    # 打印分析结果
    analyzer.print_open_pr_analysis(stats)

    # 保存结果
    output_dir = f"D:/test/{repo}_open_pr_analysis"
    save_results(stats, df, output_dir)


if __name__ == "__main__":
    main()
