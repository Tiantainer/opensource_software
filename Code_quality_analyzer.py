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

    def generate_mock_data(self):
        """
        生成模拟代码质量数据，便于展示趋势
        """
        print("生成模拟代码质量数据...")
        data = []
        for i in range(12):  # 模拟12个月的代码质量数据
            month = datetime(2025, i + 1, 1)
            complexity = random.uniform(5, 15)  # 代码复杂度
            issues = random.randint(50, 150)   # 未解决的问题
            coverage = random.uniform(60, 90)  # 代码覆盖率（百分比）
            data.append({
                "date": month,
                "complexity": complexity,
                "issues": issues,
                "coverage": coverage
            })
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(self.output_dir, f"{self.repo_name}_code_quality.csv"), index=False)
        print(f"模拟数据已保存到 {self.output_dir}")

    def analyze_quality(self):
        """
        分析代码质量数据
        """
        file_path = os.path.join(self.output_dir, f"{self.repo_name}_code_quality.csv")
        if not os.path.exists(file_path):
            print(f"代码质量数据文件不存在: {file_path}")
            return None

        quality_data = pd.read_csv(file_path)
        quality_data['date'] = pd.to_datetime(quality_data['date'])
        print(f"加载了 {len(quality_data)} 条代码质量记录")
        return quality_data


def main():
    repo_name = "openfga"
    output_dir = f"D:/test/{repo_name}_code_quality"

    analyzer = CodeQualityAnalyzer(repo_name, output_dir)
    analyzer.generate_mock_data()  # 生成模拟数据
    quality_data = analyzer.analyze_quality()

    if quality_data is not None:
        print(quality_data.head())  # 打印前几条数据


if __name__ == "__main__":
    main()
