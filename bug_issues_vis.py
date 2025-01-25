import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_bug_types(data_dir):
    """绘制Bug类型分布饼图"""
    try:
        # 设置中文显示
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 读取数据
        bug_types = pd.read_csv(f"{data_dir}/bug_types.csv")
        print("Bug类型数据：")
        print(bug_types)

        # 创建饼图
        plt.figure(figsize=(10, 8))
        plt.pie(bug_types['Count'], labels=bug_types['Name'], autopct='%1.1f%%', startangle=140)
        plt.title('Bug类型分布', pad=20)
        plt.savefig(f"{data_dir}/bug_types_pie.png")  # 保存图片
        plt.show()
    except Exception as e:
        print(f"绘制Bug类型分布饼图时出错: {e}")

def plot_components(data_dir):
    """绘制受影响组件分布饼图"""
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 读取数据
        components = pd.read_csv(f"{data_dir}/components.csv")
        print("受影响组件数据：")
        print(components)

        # 创建饼图
        plt.figure(figsize=(10, 8))
        plt.pie(components['Count'], labels=components['Name'], autopct='%1.1f%%', startangle=140)
        plt.title('受影响组件分布', pad=20)
        plt.savefig(f"{data_dir}/components_pie.png")  # 保存图片
        plt.show()
    except Exception as e:
        print(f"绘制受影响组件分布饼图时出错: {e}")

def plot_status(data_dir):
    """绘制Bug状态分布饼图"""
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 读取数据
        summary = pd.read_csv(f"{data_dir}/summary.csv")
        status_data = {'Open': summary['open_bugs'][0], 'Closed': summary['closed_bugs'][0]}
        print("Bug状态数据：")
        print(status_data)

        # 创建饼图
        plt.figure(figsize=(10, 8))
        plt.pie(status_data.values(), labels=status_data.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Bug状态分布', pad=20)
        plt.savefig(f"{data_dir}/status_pie.png")  # 保存图片
        plt.show()
    except Exception as e:
        print(f"绘制Bug状态分布饼图时出错: {e}")

def plot_monthly_trend(data_dir):
    """绘制月度Bug趋势折线图"""
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 读取数据
        monthly_trend = pd.read_csv(f"{data_dir}/monthly_trend.csv")
        monthly_trend['Month'] = pd.to_datetime(monthly_trend['Name'])
        monthly_trend = monthly_trend.sort_values('Month')
        print("月度Bug趋势数据：")
        print(monthly_trend)

        # 创建折线图
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_trend['Month'], monthly_trend['Count'], marker='o', linestyle='-', color='b')
        plt.title('月度Bug趋势', pad=20)
        plt.xlabel('月份')
        plt.ylabel('Bug数量')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{data_dir}/monthly_trend_line.png")  # 保存图片
        plt.show()
    except Exception as e:
        print(f"绘制月度Bug趋势折线图时出错: {e}")

def plot_reporters(data_dir):
    """绘制报告者贡献柱状图（前10名）"""
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 读取数据
        reporters = pd.read_csv(f"{data_dir}/reporters.csv")
        top_reporters = reporters.nlargest(10, 'Count')
        print("报告者数据：")
        print(top_reporters)

        # 创建柱状图
        plt.figure(figsize=(12, 6))
        plt.bar(top_reporters['Name'], top_reporters['Count'], color='skyblue')
        plt.title('Top 10 Bug报告者', pad=20)
        plt.xlabel('报告者')
        plt.ylabel('报告数量')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{data_dir}/top_reporters_bar.png")  # 保存图片
        plt.show()
    except Exception as e:
        print(f"绘制报告者贡献柱状图时出错: {e}")

def plot_bug_severity(data_dir):
    """绘制Bug严重程度分布条形图"""
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 读取数据
        severity = pd.read_csv(f"{data_dir}/severity.csv")
        print("Bug严重程度数据：")
        print(severity)

        # 创建条形图
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Count', y='Name', data=severity, palette='viridis')
        plt.title('Bug严重程度分布', pad=20)
        plt.xlabel('数量')
        plt.ylabel('严重程度')
        plt.tight_layout()
        plt.savefig(f"{data_dir}/severity_bar.png")  # 保存图片
        plt.show()
    except Exception as e:
        print(f"绘制Bug严重程度分布条形图时出错: {e}")

def main():
    data_dir = "D:/test/openfga_bug_analysis"

    # 绘制各个图表
    plot_bug_types(data_dir)
    plot_components(data_dir)
    plot_status(data_dir)
    plot_monthly_trend(data_dir)
    plot_reporters(data_dir)
    plot_bug_severity(data_dir)

if __name__ == "__main__":
    main()
