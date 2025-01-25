import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

class CodeReviewVisualizer:
    def __init__(self, data_dir):
        """
        初始化可视化器
        :param data_dir: 包含代码审查数据的目录
        """
        self.data_dir = data_dir
        # 加载审查数据
        self.review_df = self.load_review_data()
        # 创建输出目录
        self.output_dir = os.path.join(data_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)

    def load_review_data(self):
        """
        加载审查数据
        """
        # 查找最新的审查数据文件
        files = [f for f in os.listdir(self.data_dir) if f.startswith("code_reviews_")]
        if not files:
            raise FileNotFoundError("未找到审查数据文件。")
        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(self.data_dir, f)))
        file_path = os.path.join(self.data_dir, latest_file)
        print(f"加载审查数据文件: {file_path}")
        return pd.read_csv(file_path)

    def plot_review_states(self):
        """
        绘制审查状态分布
        """
        plt.figure(figsize=(10, 6))
        sns.countplot(data=self.review_df, x='state', palette='viridis')
        plt.title('Code Review States Distribution')
        plt.xlabel('Review State')
        plt.ylabel('Count')
        output_path = os.path.join(self.output_dir, "review_states_distribution.png")
        plt.savefig(output_path)
        plt.show()
        print(f"图像已保存到: {output_path}")

    def plot_reviewers_activity(self):
        """
        绘制审查者活动分布（前 10 名）
        """
        plt.figure(figsize=(12, 6))
        reviewer_counts = self.review_df['reviewer'].value_counts().head(10)
        sns.barplot(x=reviewer_counts.index, y=reviewer_counts.values, palette='magma')
        plt.title('Top 10 Reviewers by Activity')
        plt.xlabel('Reviewer')
        plt.ylabel('Number of Reviews')
        plt.xticks(rotation=45)
        output_path = os.path.join(self.output_dir, "top_reviewers_activity.png")
        plt.savefig(output_path)
        plt.show()
        print(f"图像已保存到: {output_path}")

    def plot_reviews_over_time(self):
        """
        绘制审查时间趋势（按月统计）
        """
        self.review_df['submitted_at'] = pd.to_datetime(self.review_df['submitted_at'])
        self.review_df['month'] = self.review_df['submitted_at'].dt.to_period('M')
        monthly_reviews = self.review_df.groupby('month').size()

        plt.figure(figsize=(12, 6))
        monthly_reviews.plot(kind='line', marker='o', color='orange')
        plt.title('Code Reviews Over Time')
        plt.xlabel('Month')
        plt.ylabel('Number of Reviews')
        plt.grid(True)
        output_path = os.path.join(self.output_dir, "reviews_over_time.png")
        plt.savefig(output_path)
        plt.show()
        print(f"图像已保存到: {output_path}")

    def plot_review_comments_length(self):
        """
        绘制审查评论长度分布
        """
        self.review_df['comment_length'] = self.review_df['body'].str.len()
        plt.figure(figsize=(10, 6))
        sns.histplot(self.review_df['comment_length'], bins=30, kde=True, color='purple')
        plt.title('Distribution of Review Comment Length')
        plt.xlabel('Comment Length')
        plt.ylabel('Frequency')
        output_path = os.path.join(self.output_dir, "review_comments_length_distribution.png")
        plt.savefig(output_path)
        plt.show()
        print(f"图像已保存到: {output_path}")

def main():
    data_dir = "D:/test/openfga_code_review_analysis"  # 审查数据目录
    visualizer = CodeReviewVisualizer(data_dir)

    print("显示审查状态分布...")
    visualizer.plot_review_states()

    print("显示审查者活动分布...")
    visualizer.plot_reviewers_activity()

    print("显示审查时间趋势...")
    visualizer.plot_reviews_over_time()

    print("显示审查评论长度分布...")
    visualizer.plot_review_comments_length()

if __name__ == "__main__":
    main()