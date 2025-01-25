def contributor_activity_analysis(pr_data):
    """
    计算每个贡献者的活动情况，分析哪些贡献者提交了最多的PR。
    :param pr_data: PR详细数据，来自analyze_open_prs方法返回的DataFrame
    :return: 每个贡献者的PR数量
    """
    contributor_count = pr_data['author'].value_counts()
    print("\n=== 贡献者活动分析 ===")
    print(f"\n活跃贡献者 PR 数量:")
    for author, count in contributor_count.items():
        print(f"{author}: {count} PRs")

    return contributor_count

