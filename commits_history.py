from git import Repo
from collections import Counter
import pandas as pd
import os
def analyze_git_repo(repo_path):
    """分析Github仓库的提交历史"""
    try:
        print("开始分析仓库...")
        repo = Repo(repo_path)
        default_branch = repo.active_branch
        commits = list(repo.iter_commits(default_branch))
        print(f"获取到 {len(commits)} 个提交记录，开始统计...")
        total_commits = len(commits)
        authors = Counter()
        commit_data = []

        for i, commit in enumerate(commits):
            if i % 100 == 0:
                print(f"已处理 {i}/{total_commits} 个提交...")
            try:
                # 将时区感知的datetime转换为UTC时间
                commit_date = pd.to_datetime(commit.authored_datetime).tz_convert('UTC')
                # 获取文件变更统计，如果失败则使用默认值
                try:
                    stats = commit.stats.total
                    files_changed = stats.get('files', 0)
                    insertions = stats.get('insertions', 0)
                    deletions = stats.get('deletions', 0)
                except:
                    files_changed = 0
                    insertions = 0
                    deletions = 0

                commit_data.append({
                    'date': commit_date,
                    'author': commit.author.name,
                    'message': commit.message.strip(),
                    'files_changed': files_changed,
                    'insertions': insertions,
                    'deletions': deletions,
                    'hash': commit.hexsha[:7]  # 添加提交哈希值
                })
                authors[commit.author.name] += 1
            except Exception as e:
                print(f"处理提交 {commit.hexsha[:7]} 时出错: {str(e)}")
                continue

        # 创建DataFrame
        df = pd.DataFrame(commit_data)

        # 转换时间列为UTC时间
        df['year_month'] = df['date'].dt.to_period('M')
        monthly_commits = df.groupby('year_month').size()

        # 输出基础统计结果
        print(f"\n=== Git 仓库分析报告 ===")
        print(f"\n总提交数: {total_commits}")

        print(f"\n前5名贡献者:")
        for author, count in authors.most_common(5):
            percentage = (count / total_commits) * 100
            print(f"{author}: {count} commits ({percentage:.1f}%)")

        # 分析提交类型
        def categorize_commit(message):
            message = message.lower()
            if 'fix' in message or 'bug' in message:
                return 'Bug修复'
            elif 'feat' in message or 'feature' in message:
                return '新功能'
            elif 'docs' in message or 'documentation' in message:
                return '文档'
            elif 'test' in message:
                return '测试'
            elif 'refactor' in message:
                return '重构'
            else:
                return '其他'

        df['commit_type'] = df['message'].apply(categorize_commit)
        commit_types = df['commit_type'].value_counts()

        # 计算代码变更统计
        total_insertions = df['insertions'].sum()
        total_deletions = df['deletions'].sum()
        total_files_changed = df['files_changed'].sum()

        # 输出详细统计结果
        print("\n=== 详细统计信息 ===")
        print(f"\n代码变更统计:")
        print(f"总共修改文件数: {total_files_changed}")
        print(f"总共增加代码行数: {total_insertions}")
        print(f"总共删除代码行数: {total_deletions}")
        print(f"净增加代码行数: {total_insertions - total_deletions}")

        print(f"\n提交类型统计:")
        for type_name, count in commit_types.items():
            percentage = (count / total_commits) * 100
            print(f"{type_name}: {count} commits ({percentage:.1f}%)")

        # 分析提交时间分布
        df['hour'] = df['date'].dt.hour
        hour_dist = df['hour'].value_counts().sort_index()

        print("\n提交时间分布:")
        for hour, count in hour_dist.items():
            percentage = (count / total_commits) * 100
            print(f"{hour:02d}:00-{hour:02d}:59: {'#' * int(percentage)} ({count} commits, {percentage:.1f}%)")

        print("\n月度提交趋势 (最近12个月):")
        monthly_trend = monthly_commits.tail(12)
        for month, count in monthly_trend.items():
            percentage = (count / monthly_trend.sum()) * 100
            print(f"{month}: {'#' * int(percentage / 5)} ({count} commits, {percentage:.1f}%)")

        # 保存分析结果
        output_dir = "D:/test/analysis_results"
        os.makedirs(output_dir, exist_ok=True)

        # 保存详细数据
        df.to_csv(f"{output_dir}/commit_details.csv")
        monthly_commits.to_csv(f"{output_dir}/monthly_commits.csv")
        pd.DataFrame(authors.most_common(), columns=['Author', 'Commits']).to_csv(f"{output_dir}/author_stats.csv")

        print(f"\n详细分析结果已保存到: {output_dir}")

        return {
            'total_commits': total_commits,
            'authors': dict(authors),
            'monthly_commits': monthly_commits.to_dict(),
            'commit_types': commit_types.to_dict(),
            'code_stats': {
                'total_insertions': total_insertions,
                'total_deletions': total_deletions,
                'total_files_changed': total_files_changed
            }
        }

    except Exception as e:
        print(f"分析过程中出现错误: {str(e)}")
        return None


def main():
    repo_path = "D:/test/openfga"# 代码地址（即把GitHub上的项目拉下来后存放的位置），原项目地址：https://github.com/openfga/openfga
    results = analyze_git_repo(repo_path)
    if results:
        print("\n分析完成!")

if __name__ == "__main__":
    main()

