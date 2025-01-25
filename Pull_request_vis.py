import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


class PRVisualizer:
    def __init__(self, data_dir, output_dir):
        """
        初始化可视化器
        :param data_dir: 包含PR数据的目录
        :param output_dir: 保存图片的目录
        """
        self.data_dir = data_dir
        self.output_dir = output_dir

        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)

        # 读取数据文件
        self.pr_details = pd.read_csv(os.path.join(data_dir, 'open_pr_details.csv'))
        self.summary = pd.read_csv(os.path.join(data_dir, 'summary.csv'))
        self.authors = pd.read_csv(os.path.join(data_dir, 'authors.csv'))
        self.labels = pd.read_csv(os.path.join(data_dir, 'labels.csv'))

        # 设置绘图样式
        plt.style.use('seaborn')
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False

    def show_pr_age_distribution(self):
        """显示PR年龄分布"""
        plt.figure(figsize=(12, 6))
        sns.histplot(data=self.pr_details, x='age_days', bins=20)
        plt.title('PR Age Distribution')
        plt.xlabel('Age (days)')
        plt.ylabel('Count')
        plt.savefig(os.path.join(self.output_dir, 'pr_age_distribution.png'))  # 保存图片
        plt.show()

    def show_author_distribution(self):
        """显示作者分布"""
        plt.figure(figsize=(10, 10))
        data = self.authors.sort_values('Count', ascending=False)
        plt.pie(data['Count'], labels=data['Name'], autopct='%1.1f%%')
        plt.title('PR Authors Distribution')
        plt.savefig(os.path.join(self.output_dir, 'author_distribution.png'))  # 保存图片
        plt.show()

    def show_label_distribution(self):
        """显示标签分布"""
        plt.figure(figsize=(12, 6))
        data = self.labels.sort_values('Count', ascending=True)
        sns.barplot(x='Count', y='Name', data=data)
        plt.title('PR Labels Distribution')
        plt.xlabel('Count')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'label_distribution.png'))  # 保存图片
        plt.show()

    def show_pr_size_distribution(self):
        """显示PR大小分布"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # 文件变更分布
        sns.histplot(data=self.pr_details, x='changed_files', bins=20, ax=ax1)
        ax1.set_title('Files Changed Distribution')
        ax1.set_xlabel('Number of Files')

        # 代码行变更分布
        sns.histplot(data=self.pr_details, x='additions', bins=20, ax=ax2, color='green')
        sns.histplot(data=self.pr_details, x='deletions', bins=20, ax=ax2, color='red', alpha=0.5)
        ax2.set_title('Code Changes Distribution')
        ax2.set_xlabel('Number of Lines')
        ax2.legend(['Additions', 'Deletions'])
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'pr_size_distribution.png'))  # 保存图片
        plt.show()

    def show_review_activity(self):
        """显示评审活动分布"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # 评论数分布
        sns.boxplot(data=self.pr_details, y='review_comments', ax=ax1)
        ax1.set_title('Review Comments Distribution')
        ax1.set_ylabel('Number of Review Comments')

        # 评论数随时间变化
        self.pr_details['created_at'] = pd.to_datetime(self.pr_details['created_at'])
        sns.scatterplot(data=self.pr_details, x='created_at', y='review_comments', ax=ax2)
        ax2.set_title('Review Comments Over Time')
        ax2.set_xlabel('Creation Date')
        ax2.set_ylabel('Number of Review Comments')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'review_activity.png'))  # 保存图片
        plt.show()

    def show_timeline(self):
        """显示PR创建时间线"""
        plt.figure(figsize=(15, 8))

        # 转换时间并排序
        self.pr_details['created_at'] = pd.to_datetime(self.pr_details['created_at'])
        timeline_data = self.pr_details.sort_values('created_at')

        # 绘制累积图
        plt.plot(timeline_data['created_at'], range(1, len(timeline_data) + 1), marker='o')
        plt.title('PR Creation Timeline')
        plt.xlabel('Creation Date')
        plt.ylabel('Cumulative Number of PRs')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'pr_timeline.png'))  # 保存图片
        plt.show()

    def show_changes_heatmap(self):
        """显示变更热力图"""
        plt.figure(figsize=(12, 8))

        # 准备数据
        changes_data = self.pr_details.pivot_table(
            index='author',
            values=['changed_files', 'additions', 'deletions', 'review_comments'],
            aggfunc='sum'
        )

        # 绘制热力图
        sns.heatmap(changes_data, annot=True, fmt='.0f', cmap='YlOrRd')
        plt.title('PR Changes Heatmap')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'changes_heatmap.png'))  # 保存图片
        plt.show()


def main():
    # 设置数据目录和输出目录
    repo = "openfga"
    data_dir = f"D:/test/{repo}_open_pr_analysis"
    output_dir = f"D:/test/{repo}_visualization_output"

    # 创建可视化器
    visualizer = PRVisualizer(data_dir, output_dir)

    # 显示每个图表并保存
    print("\n显示PR年龄分布...")
    visualizer.show_pr_age_distribution()

    print("\n显示作者分布...")
    visualizer.show_author_distribution()

    print("\n显示标签分布...")
    visualizer.show_label_distribution()

    print("\n显示PR大小分布...")
    visualizer.show_pr_size_distribution()

    print("\n显示评审活动...")
    visualizer.show_review_activity()

    print("\n显示时间线...")
    visualizer.show_timeline()

    print("\n显示变更热力图...")
    visualizer.show_changes_heatmap()


if __name__ == "__main__":
    main()
