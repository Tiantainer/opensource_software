import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# GitHub 仓库信息
GITHUB_API_URL = "https://github.com/Tiantainer/opensource_software"
REPO_OWNER = "Tiantianer"  # 替换为仓库拥有者
REPO_NAME = "your-repo-name"    # 替换为仓库名称
ACCESS_TOKEN = "your-github-token"  # 替换为你的 GitHub Access Token

# 获取 Issues 数据
def fetch_issues():
    issues = []
    page = 1

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    while True:
        url = f"{GITHUB_API_URL}/{REPO_OWNER}/{REPO_NAME}/issues?state=all&page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch issues:", response.status_code, response.text)
            break

        data = response.json()
        if not data:
            break

        issues.extend(data)
        page += 1

    return issues

# 数据处理
def process_issues_data(issues):
    created_dates = []
    closed_dates = []

    for issue in issues:
        # 排除 PR（PR 是特殊 Issue）
        if "pull_request" in issue:
            continue
        created_dates.append(issue["created_at"])
        if issue["closed_at"]:
            closed_dates.append(issue["closed_at"])

    # 转换为 DataFrame
    created_df = pd.DataFrame({"date": pd.to_datetime(created_dates), "type": "created"})
    closed_df = pd.DataFrame({"date": pd.to_datetime(closed_dates), "type": "closed"})

    # 合并数据
    all_data = pd.concat([created_df, closed_df], ignore_index=True)
    all_data["date"] = all_data["date"].dt.date  # 转换为日期格式（只保留年月日）
    return all_data

# 绘制时间趋势图
def plot_issue_trends(data):
    # 按日期和类型分组
    trends = data.groupby(["date", "type"]).size().unstack(fill_value=0)

    # 计算累计未关闭 Issue
    trends["open_issues"] = trends["created"].cumsum() - trends["closed"].cumsum()

    # 绘图
    plt.figure(figsize=(12, 6))
    plt.plot(trends.index, trends["created"], label="New Issues", color="blue", linestyle="--")
    plt.plot(trends.index, trends["closed"], label="Closed Issues", color="green", linestyle="-.")
    plt.plot(trends.index, trends["open_issues"], label="Open Issues", color="red", linewidth=2)

    plt.title("Issue Trends Over Time", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Number of Issues", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

# 主程序
if __name__ == "__main__":
    # 获取数据
    print("Fetching issues data from GitHub...")
    issues = fetch_issues()

    if not issues:
        print("No issues found. Exiting...")
    else:
        # 处理数据
        print("Processing data...")
        issue_data = process_issues_data(issues)

        # 绘制可视化
        print("Plotting issue trends...")
        plot_issue_trends(issue_data)
