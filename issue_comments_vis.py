import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class IssueCommentVisualizer:
    def __init__(self, data_dir, output_dir):
        """
        初始化可视化器
        :param data_dir: 包含 Issue 评论数据的目录
        :param output_dir: 保存生成图片的目录
        """
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.comments_df = pd.read_csv(os.path.join(data_dir, "issue_comments.csv"))
        self.commenters_df = pd.read_csv(os.path.join(data_dir, "commenters.csv"))
        self.monthly_df = pd.read_csv(os.path.join(data_dir, "comments_by_month.csv"))
        self.hourly_df = pd.read_csv(os.path.join(data_dir, "comments_by_hour.csv"))

    def plot_commenters_activity(self):
        """
        绘制评论者活动分布（前 10 名）
        """
        plt.figure(figsize=(12, 6))
        top_commenters = self.commenters_df.nlargest(10, 'Count')
        sns.barplot(x='Commenter', y='Count', data=top_commenters, palette='viridis')
        plt.title('Top 10 Commenters by Activity')
        plt.xlabel('Commenter')
        plt.ylabel('Number of Comments')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 保存图片
        output_path = os.path.join(self.output_dir, "top_commenters_activity.png")
        plt.savefig(output_path)
        print(f"图片已保存到：{output_path}")
        
        plt.show()

    def plot_monthly_comments(self):
        """
        绘制月度评论趋势
        """
        plt.figure(figsize=(12, 6))
        self.monthly_df['Month'] = pd.to_datetime(self.monthly_df['Month'])
        plt.plot(self.monthly_df['Month'], self.monthly_df['Count'], marker='o', color='orange')
        plt.title('Monthly Issue Comments Trend')
        plt.xlabel('Month')
        plt.ylabel('Number of Comments')
        plt.grid(True)
        plt.tight_layout()
        
        # 保存图片
        output_path = os.path.join(self.output_dir, "monthly_comments_trend.png")
        plt.savefig(output_path)
        print(f"图片已保存到：{output_path}")
        
        plt.show()

    def plot_hourly_comments(self):
        """
        绘制小时评论分布
        """
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Hour', y='Count', data=self.hourly_df, palette='coolwarm')
        plt.title('Hourly Issue Comments Distribution')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Comments')
        plt.grid(True)
        plt.tight_layout()
        
        # 保存图片
        output_path = os.path.join(self.output_dir, "hourly_comments_distribution.png")
        plt.savefig(output_path)
        print(f"图片已保存到：{output_path}")
        
        plt.show()

def main():
    data_dir = "D:/test/openfga_issue_comments_analysis"
    output_dir = "D:/test/output"  # 设置保存图片的目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 如果目录不存在，则创建
    
    visualizer = IssueCommentVisualizer(data_dir, output_dir)

    print("显示评论者活动分布...")
    visualizer.plot_commenters_activity()

    print("显示月度评论趋势...")
    visualizer.plot_monthly_comments()

    print("显示小时评论分布...")
    visualizer.plot_hourly_comments()

if __name__ == "__main__":
    main()