def pr_comments_analysis(pr_data):
    """
    计算每个PR的评论数，并分析评论数的平均值。
    :param pr_data: PR详细数据，来自analyze_open_prs方法返回的DataFrame
    :return: 每个PR的评论数
    """
    pr_data['comment_count'] = pr_data['comment_count'].astype(int)  # 确保评论数是整数
    print("\n=== 评论分析 ===")
    print(f"\n每个PR的评论数:")
    print(pr_data[['number', 'title', 'comment_count']])

    avg_comments = pr_data['comment_count'].mean()
    print(f"\n平均评论数: {avg_comments:.1f}")

    return pr_data[['number', 'title', 'comment_count']]
