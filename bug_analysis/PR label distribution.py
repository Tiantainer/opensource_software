def pr_labels_distribution_analysis(pr_data):
    """
    分析PR标签的分布情况，计算每个标签的出现频率。
    :param pr_data: PR详细数据，来自analyze_open_prs方法返回的DataFrame
    :return: 每个标签的出现次数
    """
    labels_count = pr_data['labels'].explode().value_counts()
    print("\n=== PR标签分布分析 ===")
    print(f"\nPR标签分布:")
    for label, count in labels_count.items():
        print(f"{label}: {count} 次")

    return labels_count
