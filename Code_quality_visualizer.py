import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def visualize_code_quality(data_dir):
    """
    可视化代码质量数据
    :param data_dir: 包含代码质量数据的目录
    """
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.family'] = 'DejaVu Sans'

    # 设置输出目录
    output_dir = os.path.join(data_dir, "quality_visualization")
    os.makedirs(output_dir, exist_ok=True)

    # 读取代码质量数据
    quality_data_path = os.path.join(data_dir, "openfga_code_quality.csv")
    if not os.path.exists(quality_data_path):
        print(f"代码质量数据文件不存在: {quality_data_path}")
        return

    quality_data = pd.read_csv(quality_data_path)
    quality_data['date'] = pd.to_datetime(quality_data['date'])

    # 1. 代码复杂度趋势
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='complexity', data=quality_data, marker='o', color='#e74c3c')
    plt.title('Code Complexity Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Complexity')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'code_complexity_trend.png'))
    plt.show()

    # 2. 未解决问题数量趋势
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='issues', data=quality_data, marker='o', color='#3498db')
    plt.title('Unresolved Issues Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Issues')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'unresolved_issues_trend.png'))
    plt.show()

    # 3. 代码覆盖率趋势
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='coverage', data=quality_data, marker='o', color='#2ecc71')
    plt.title('Code Coverage Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Coverage (%)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'code_coverage_trend.png'))
    plt.show()


def main():
    data_dir = "D:/test/openfga_code_quality"
    visualize_code_quality(data_dir)


if __name__ == "__main__":
    main()
