def pr_draft_status_analysis(pr_data):
    """
    分析PR的草稿状态，统计草稿PR的数量和占比。
    :param pr_data: PR详细数据，来自analyze_open_prs方法返回的DataFrame
    :return: 草稿状态的统计
    """
    draft_count = pr_data['draft'].sum()
    total_prs = len(pr_data)

    print("\n=== PR草稿状态分析 ===")
    print(f"草稿PR数量: {draft_count}")
    print(f"草稿PR占比: {draft_count / total_prs * 100:.2f}%")

    return draft_count
