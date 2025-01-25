def pr_merge_status_analysis(pr_data):
    """
    分析PR的合并状态，统计已合并和未合并的PR数量。
    :param pr_data: PR详细数据，来自analyze_open_prs方法返回的DataFrame
    :return: 合并状态统计
    """
    merge_status_count = pr_data['merged'].value_counts()
    print("\n=== PR合并状态分析 ===")
    print(f"\nPR合并状态:")
    for status, count in merge_status_count.items():
        status_str = "已合并" if status else "未合并"
        print(f"{status_str}: {count} 次")

    return merge_status_count
