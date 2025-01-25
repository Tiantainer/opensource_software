def pr_resolution_time_analysis(pr_data):
    """
    计算每个PR的解决时间（创建到关闭的时间差）。
    :param pr_data: PR详细数据，来自analyze_open_prs方法返回的DataFrame
    :return: 每个PR的解决时间
    """
    pr_data['resolution_time'] = (pr_data['closed_at'] - pr_data['created_at']).dt.days
    print("\n=== PR解决时间分析 ===")
    print(f"\n每个PR的解决时间（天数）:")
    print(pr_data[['number', 'title', 'resolution_time']])

    avg_resolution_time = pr_data['resolution_time'].mean()
    print(f"\n平均解决时间: {avg_resolution_time:.1f} 天")

    return pr_data[['number', 'title', 'resolution_time']]
