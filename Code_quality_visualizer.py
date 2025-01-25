import pandas as pd
import os


def analyze_and_save(data_dir):
    """
    分析代码质量数据并保存结果为多个 CSV 文件
    :param data_dir: 包含代码质量数据的目录
    """
    output_dir = os.path.join(data_dir, "analysis_results")
    os.makedirs(output_dir, exist_ok=True)

    # 读取最新生成的质量数据文件
    quality_data_path = max([os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')], key=os.path.getctime)
    print(f"加载数据文件: {quality_data_path}")
    quality_data = pd.read_csv(quality_data_path)

    # 1. 按模块统计平均值
    module_summary = quality_data.groupby('module').mean().reset_index()
    module_summary_file = os.path.join(output_dir, "module_summary.csv")
    module_summary.to_csv(module_summary_file, index=False)
    print(f"模块统计已保存到: {module_summary_file}")

    # 2. 按贡献者统计问题数量
    contributor_summary = quality_data.groupby('contributor')['issues'].sum().reset_index()
    contributor_summary_file = os.path.join(output_dir, "contributor_summary.csv")
    contributor_summary.to_csv(contributor_summary_file, index=False)
    print(f"贡献者统计已保存到: {contributor_summary_file}")

    # 3. 问题类型分布统计
    issue_type_summary = quality_data['issue_type'].value_counts().reset_index()
    issue_type_summary.columns = ['issue_type', 'count']
    issue_type_summary_file = os.path.join(output_dir, "issue_type_summary.csv")
    issue_type_summary.to_csv(issue_type_summary_file, index=False)
    print(f"问题类型分布统计已保存到: {issue_type_summary_file}")

    # 4. 按日期统计覆盖率和复杂度趋势
    trend_summary = quality_data.groupby('date')[['coverage', 'complexity']].mean().reset_index()
    trend_summary_file = os.path.join(output_dir, "trend_summary.csv")
    trend_summary.to_csv(trend_summary_file, index=False)
    print(f"趋势统计已保存到: {trend_summary_file}")


def main():
    data_dir = "D:/test/openfga_code_quality"
    analyze_and_save(data_dir)


if __name__ == "__main__":
    main()
