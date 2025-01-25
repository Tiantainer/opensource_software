import pandas as pd
import os
from datetime import datetime
import random

class CodeQualityAnalyzer:
    def __init__(self, repo_name, output_dir):
        """
        初始化代码质量分析器
        :param repo_name: 仓库名称
        :param output_dir: 保存分析结果的目录
        """
        self.repo_name = repo_name
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_module_csv(self, quality_data):
        """
        按模块生成单独的 CSV 文件
        :param quality_data: 代码质量数据
        """
        modules = quality_data['module'].unique()
        for module in modules:
            module_data = quality_data[quality_data['module'] == module]
            file_path = os.path.join(self.output_dir, f"{module}_code_quality.csv")
            module_data.to_csv(file_path, index=False)
            print(f"模块数据已保存到: {file_path}")

    def generate_mock_data(self):
        """
        生成模拟代码质量数据
        """
        print("生成模拟代码质量数据...")
        data = []
        modules = ['module1', 'module2', 'module3']
        contributors = ['Alice', 'Bob', 'Charlie']
        issue_types = ['Bug', 'Performance', 'Maintainability']

        for i in range(12):  # 模拟12个月的数据
            for module in modules:
                for contributor in contributors:
                    month = datetime(2025, i + 1, 1)
                    complexity = random.uniform(5, 15)
                    issues = random.randint(50, 150)
                    coverage = random.uniform(60, 90)
                    issue_type = random.choice(issue_types)
                    data.append({
                        "date": month,
                        "module": module,
                        "contributor": contributor,
                        "complexity": complexity,
                        "issues": issues,
                        "coverage": coverage,
                        "issue_type": issue_type
                    })

        quality_data = pd.DataFrame(data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(self.output_dir, f"{self.repo_name}_code_quality_{timestamp}.csv")
        quality_data.to_csv(file_path, index=False)
        print(f"整体数据已保存到: {file_path}")

        # 按模块生成 CSV 文件
        self.save_module_csv(quality_data)


def main():
    repo_name = "openfga"
    output_dir = f"D:/test/{repo_name}_code_quality"

    analyzer = CodeQualityAnalyzer(repo_name, output_dir)
    analyzer.generate_mock_data()  # 生成模拟数据


if __name__ == "__main__":
    main()
