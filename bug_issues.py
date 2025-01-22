import requests
import pandas as pd
from collections import Counter, defaultdict
from datetime import datetime
import os
import time

class GitHubBugAnalyzer:
    def __init__(self, owner: str, repo: str, token: str = None):
        """
        初始化分析器
        :param owner: 仓库所有者
        :param repo: 仓库名称
        :param token: GitHub API token（可选）
        """
        self.owner = owner
        self.repo = repo
        self.headers = {'Authorization': f'token {token}'} if token else {}
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'

    def get_issues(self, state='all', label='bug'):
        """获取仓库的所有bug issues"""
        print(f"开始获取 {self.owner}/{self.repo} 的bug报告...")
        issues = []
        page = 1
        per_page = 100

        while True:
            print(f"正在获取第 {page} 页...")
            url = f'{self.base_url}/issues'
            params = {
                'state': state,
                'labels': label,
                'page': page,
                'per_page': per_page
            }

            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code != 200:
                print(f"获取数据失败: {response.status_code}")
                break

            page_issues = response.json()
            if not page_issues:
                break

            issues.extend(page_issues)
            page += 1
            time.sleep(1)  # 避免触发API限制

        print(f"共获取到 {len(issues)} 个bug报告")
        return issues

    def analyze_issues(self):
        """分析bug报告"""
        issues = self.get_issues()

        # 初始化统计数据
        stats = {
            'total_bugs': len(issues),
            'status': defaultdict(int),
            'labels': Counter(),
            'monthly_trend': defaultdict(int),
            'bug_types': Counter(),
            'components': Counter(),
            'reporters': Counter(),
            'fix_times': [],
            'priorities': Counter(),
            'severity': Counter()
        }

        issue_data = []
        processed_issues = 0

        for issue in issues:
            try:
                # 解析issue
                issue_info = self._parse_issue(issue)

                # 更新统计信息
                self._update_stats(stats, issue_info)

                issue_data.append(issue_info)
                processed_issues += 1

            except Exception as e:
                print(f"处理issue #{issue['number']} 时出错: {str(e)}")
                continue

        print(f"\n成功处理 {processed_issues} 个issues（共 {len(issues)} 个）")

        return stats, pd.DataFrame(issue_data)

    def _parse_issue(self, issue):
        """解析单个issue的信息"""
        created_at = datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        closed_at = None
        if issue['closed_at']:
            closed_at = datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ')

        # 获取标签名称
        labels = [label['name'] for label in issue['labels']]
        body = issue.get('body', '') or ''  # 确保body不是None

        # 基础信息
        info = {
            'number': issue['number'],
            'title': issue['title'],
            'state': issue['state'],
            'created_at': created_at,
            'closed_at': closed_at,
            'reporter': issue['user']['login'],
            'labels': labels,
            'comments_count': issue['comments'],
            'body': body,
            'type': self._categorize_bug_type(issue['title'], body),
            'component': self._extract_component(issue['title'], body),
            'severity': self._extract_severity(labels),
            'priority': self._extract_priority(labels),
            'has_reproduction': self._check_reproducibility(body)
        }

        # 计算修复时间
        if closed_at:
            info['fix_time_days'] = (closed_at - created_at).days
        else:
            info['fix_time_days'] = None

        return info

    def _update_stats(self, stats, issue_info):
        """更新统计信息"""
        try:
            # 更新状态统计
            stats['status'][issue_info['state']] += 1

            # 更新标签统计
            for label in issue_info['labels']:
                stats['labels'][label] += 1

            # 更新月度趋势
            month_key = issue_info['created_at'].strftime('%Y-%m')
            stats['monthly_trend'][month_key] += 1

            # 更新bug类型统计
            if issue_info.get('type'):
                stats['bug_types'][issue_info['type']] += 1

            # 更新组件统计
            if issue_info.get('component'):
                stats['components'][issue_info['component']] += 1

            # 更新报告者统计
            if issue_info.get('reporter'):
                stats['reporters'][issue_info['reporter']] += 1

            # 更新严重程度统计
            if issue_info.get('severity'):
                stats['severity'][issue_info['severity']] += 1

            # 更新优先级统计
            if issue_info.get('priority'):
                stats['priorities'][issue_info['priority']] += 1

            # 更新修复时间统计
            if issue_info.get('fix_time_days') is not None:
                stats['fix_times'].append(issue_info['fix_time_days'])

        except Exception as e:
            print(f"更新统计信息时出错: {str(e)}")

    def _categorize_bug_type(self, title: str, body: str) -> str:
        """对bug类型进行分类"""
        text = (title + ' ' + body).lower()

        categories = {
            '功能错误': ['function', 'feature', 'not working', 'doesn\'t work', 'broken', 'incorrect'],
            '性能问题': ['performance', 'slow', 'memory', 'cpu', 'leak', 'timeout'],
            '兼容性问题': ['compatibility', 'version', 'platform', 'browser', 'dependency'],
            '安全问题': ['security', 'vulnerability', 'exploit', 'auth', 'permission'],
            '崩溃': ['crash', 'exception', 'error', 'fail', 'null'],
            'UI问题': ['ui', 'interface', 'display', 'visual', 'style', 'layout'],
            '构建问题': ['build', 'compile', 'install', 'deploy', 'package'],
            '数据问题': ['data', 'database', 'storage', 'corrupt', 'invalid']
        }

        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category

        return '其他'

    def _extract_component(self, title: str, body: str) -> str:
        """提取受影响的组件"""
        text = (title + ' ' + body).lower()

        components = {
            '前端': ['frontend', 'ui', 'interface', 'css', 'html', 'javascript', 'web'],
            '后端': ['backend', 'server', 'api', 'service', 'endpoint'],
            '数据库': ['database', 'db', 'sql', 'storage', 'data'],
            '认证': ['auth', 'login', 'permission', 'security', 'access'],
            '构建系统': ['build', 'ci', 'pipeline', 'deploy', 'package'],
            '文档': ['doc', 'documentation', 'example', 'comment'],
            '测试': ['test', 'testing', 'unittest', 'integration test']
        }

        for component, keywords in components.items():
            if any(keyword in text for keyword in keywords):
                return component

        return '其他'

    def _extract_severity(self, labels) -> str:
        """从标签中提取严重程度"""
        severity_keywords = {
            '严重': ['critical', 'severe', 'major', 'high'],
            '中等': ['medium', 'moderate', 'normal'],
            '轻微': ['minor', 'low', 'trivial']
        }

        label_texts = [label.lower() for label in labels]

        for severity, keywords in severity_keywords.items():
            if any(any(keyword in label for keyword in keywords) for label in label_texts):
                return severity

        return '未指定'

    def _extract_priority(self, labels) -> str:
        """从标签中提取优先级"""
        priority_keywords = {
            'P0': ['p0', 'critical', 'blocker'],
            'P1': ['p1', 'high', 'important'],
            'P2': ['p2', 'medium', 'normal'],
            'P3': ['p3', 'low', 'minor']
        }

        label_texts = [label.lower() for label in labels]

        for priority, keywords in priority_keywords.items():
            if any(any(keyword in label for keyword in keywords) for label in label_texts):
                return priority

        return '未指定'

    def _check_reproducibility(self, body: str) -> bool:
        """检查是否提供了复现步骤"""
        if not body:
            return False

        reproduction_keywords = [
            'steps to reproduce',
            'reproduction steps',
            'how to reproduce',
            'to reproduce',
            'steps:',
            'reproduce:'
        ]

        return any(keyword in body.lower() for keyword in reproduction_keywords)


def print_analysis(stats):
    """打印分析结果"""
    print("\n=== Bug报告分析结果 ===")
    print(f"\n总bug数: {stats['total_bugs']}")

    # 状态分布
    if stats['status']:
        print("\nBug状态分布:")
        for status, count in stats['status'].items():
            percentage = count / stats['total_bugs'] * 100
            print(f"{status}: {count} ({percentage:.1f}%)")

    # Bug类型分布
    if stats['bug_types']:
        print("\nBug类型分布:")
        for bug_type, count in stats['bug_types'].most_common():
            percentage = count / stats['total_bugs'] * 100
            print(f"{bug_type}: {count} ({percentage:.1f}%)")

    # 组件分布
    if stats['components']:
        print("\n受影响组件分布:")
        for component, count in stats['components'].most_common():
            percentage = count / stats['total_bugs'] * 100
            print(f"{component}: {count} ({percentage:.1f}%)")

    # 标签分布
    if stats['labels']:
        print("\n标签分布:")
        for label, count in stats['labels'].most_common():
            percentage = count / stats['total_bugs'] * 100
            print(f"{label}: {count} ({percentage:.1f}%)")

    # 月度趋势
    if stats['monthly_trend']:
        print("\n月度bug趋势:")
        for month, count in sorted(stats['monthly_trend'].items()):
            print(f"{month}: {count}")

    # 修复时间
    if stats['fix_times']:
        avg_fix_time = sum(stats['fix_times']) / len(stats['fix_times'])
        print(f"\n平均修复时间: {avg_fix_time:.1f} 天")

    # 报告者统计
    if stats['reporters']:
        print("\n活跃bug报告者 (前5名):")
        for reporter, count in stats['reporters'].most_common(5):
            percentage = count / stats['total_bugs'] * 100
            print(f"{reporter}: {count} ({percentage:.1f}%)")


def save_results(stats, df, output_dir):
    """保存分析结果"""
    os.makedirs(output_dir, exist_ok=True)

    # 保存原始数据
    df.to_csv(f"{output_dir}/bug_details.csv", index=False)

    # 保存统计数据
    summary_data = {
        'total_bugs': stats['total_bugs'],
        'open_bugs': stats['status'].get('open', 0),
        'closed_bugs': stats['status'].get('closed', 0),
        'avg_fix_time': sum(stats['fix_times']) / len(stats['fix_times']) if stats['fix_times'] else 0
    }
    pd.DataFrame([summary_data]).to_csv(f"{output_dir}/summary.csv", index=False)

    # 保存各类统计数据
    for name, data in {
        'bug_types': stats['bug_types'],
        'components': stats['components'],
        'severity': stats['severity'],
        'reporters': stats['reporters'],
        'monthly_trend': stats['monthly_trend']
    }.items():
        pd.DataFrame(list(data.items()),
                     columns=['Name', 'Count']).to_csv(f"{output_dir}/{name}.csv", index=False)

    print(f"\n分析结果已保存到: {output_dir}")


def main():
    # 设置要分析的仓库
    owner = "openfga"
    repo = "openfga"

    # 创建分析器
    analyzer = GitHubBugAnalyzer(owner, repo)

    # 执行分析
    stats, df = analyzer.analyze_issues()

    # 打印分析结果
    print_analysis(stats)

    # 保存结果
    output_dir = f"D:/test/{repo}_bug_analysis"
    save_results(stats, df, output_dir)


if __name__ == "__main__":
    main()


