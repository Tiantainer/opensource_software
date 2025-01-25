def pr_target_branch_analysis(pr_data):
    """
    分析PR提交到不同目标分支的分布情况。
    :param pr_data: PR详细数据，来自analyze_open_prs方法返回的DataFrame
    :return: 目标分支的统计
    """
    target_branch_count = pr_data['base_branch'].value_counts()

    print("\n=== PR目标分支分布分析 ===")
    print(f"\nPR目标分支分布:")
    for branch, count in target_branch_count.items():
        print(f"{branch}: {count} 次")

    return target_branch_count
