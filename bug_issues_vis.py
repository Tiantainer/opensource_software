import pandas as pd
import matplotlib.pyplot as plt


def plot_bug_types(data_dir):
    """绘制Bug类型分布饼图"""
    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取数据
    bug_types = pd.read_csv(f"{data_dir}/bug_types.csv")

    # 创建饼图
    plt.figure(figsize=(10, 8))
    plt.pie(bug_types['Count'], labels=bug_types['Name'], autopct='%1.1f%%')
    plt.title('Bug类型分布')
    plt.show()


def plot_components(data_dir):
    """绘制组件分布饼图"""
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取数据
    components = pd.read_csv(f"{data_dir}/components.csv")

    # 创建饼图
    plt.figure(figsize=(10, 8))
    plt.pie(components['Count'], labels=components['Name'], autopct='%1.1f%%')
    plt.title('受影响组件分布')
    plt.show()



def plot_status(data_dir):
    """绘制Bug状态分布饼图"""
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取数据
    summary = pd.read_csv(f"{data_dir}/summary.csv")
    status_data = {'Open': summary['open_bugs'][0], 'Closed': summary['closed_bugs'][0]}

    # 创建饼图
    plt.figure(figsize=(10, 8))
    plt.pie(status_data.values(), labels=status_data.keys(), autopct='%1.1f%%')
    plt.title('Bug状态分布')
    plt.show()


def plot_monthly_trend(data_dir):
    """绘制月度趋势折线图"""
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取数据
    monthly_trend = pd.read_csv(f"{data_dir}/monthly_trend.csv")
    monthly_trend['Month'] = pd.to_datetime(monthly_trend['Name'])
    monthly_trend = monthly_trend.sort_values('Month')

    # 创建折线图
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_trend['Month'], monthly_trend['Count'], marker='o')
    plt.title('月度Bug趋势')
    plt.xlabel('月份')
    plt.ylabel('Bug数量')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_reporters(data_dir):
    """绘制报告者贡献柱状图（前10名）"""
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取数据
    reporters = pd.read_csv(f"{data_dir}/reporters.csv")
    top_reporters = reporters.nlargest(10, 'Count')

    # 创建柱状图
    plt.figure(figsize=(12, 6))
    plt.bar(top_reporters['Name'], top_reporters['Count'])
    plt.title('Top 10 Bug报告者')
    plt.xlabel('报告者')
    plt.ylabel('报告数量')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    data_dir = "D:/test/openfga_bug_analysis"

    # 绘制各个图表
    plot_bug_types(data_dir)
    plot_components(data_dir)
    plot_status(data_dir)
    plot_monthly_trend(data_dir)
    plot_reporters(data_dir)


if __name__ == "__main__":
    main()

