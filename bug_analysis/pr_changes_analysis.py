def pr_changes_analysis(pr_data):
    """
    分析PR的修改内容，包括修改的文件数量、增加的行数和删除的行数。
    :param pr_data: PR详细数据，来自analyze_open_prs方法返回的DataFrame
    :return: PR修改内容的统计
    """
    total_changed_files = pr_data['changed_files'].sum()
    total_additions = pr_data['additions'].sum()
    total_deletions = pr_data['deletions'].sum()

    avg_changed_files = pr_data['changed_files'].mean()
    avg_additions = pr_data['additions'].mean()
    avg_deletions = pr_data['deletions'].mean()

    print("\n=== PR修改内容分析 ===")
    print(f"总共修改的文件数: {total_changed_files}")
    print(f"总共增加的行数: {total_additions}")
    print(f"总共删除的行数: {total_deletions}")
    print(f"\n平均修改文件数: {avg_changed_files:.1f}")
    print(f"平均增加行数: {avg_additions:.1f}")
    print(f"平均删除行数: {avg_deletions:.1f}")

    return {
        'total_changed_files': total_changed_files,
        'total_additions': total_additions,
        'total_deletions': total_deletions,
        'avg_changed_files': avg_changed_files,
        'avg_additions': avg_additions,
        'avg_deletions': avg_deletions
    }
