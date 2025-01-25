def pr_creation_time_analysis(pr_data):
    """
    分析PR的创建时间分布，查看PR提交的频率趋势。
    :param pr_data: PR详细数据，来自analyze_open_prs方法返回的DataFrame
    :return: PR创建时间的分析结果
    """
    pr_data['created_at'] = pd.to_datetime(pr_data['created_at'])  # 确保创建时间为时间格式
    pr_data['created_month'] = pr_data['created_at'].dt.to_period('M')  # 按月份分组

    creation_time_distribution = pr_data['created_month'].value_counts().sort_index()

    print("\n=== PR创建时间分析 ===")
    print(f"\nPR创建时间分布（按月统计）:")
    for period, count in creation_time_distribution.items():
        print(f"{period}: {count} 个PR")

    return creation_time_distribution
