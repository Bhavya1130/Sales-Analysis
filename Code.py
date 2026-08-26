import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", None)

df = pd.read_csv("AusApparalSales4thQrt2020.csv")

print(df.shape)
display(df.head())
print(df.columns.tolist())
print(df.dtypes)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print(df.isna().sum())
print(df.notna().sum())
print("Duplicate Rows:", df.duplicated().sum())

df = df.drop_duplicates()

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df["unit"] = pd.to_numeric(df["unit"], errors="coerce")

df = df.dropna(subset=["date", "sales", "unit"])
df = df[(df["sales"] >= 0) & (df["unit"] >= 0)]

print("Final Dataset Shape:", df.shape)

scaler = MinMaxScaler()

df[["sales_normalized", "unit_normalized"]] = scaler.fit_transform(
    df[["sales", "unit"]]
)

display(df.head())

sales_stats = df["sales"].agg(["mean", "median", "std", "min", "max"])
unit_stats = df["unit"].agg(["mean", "median", "std", "min", "max"])

display(sales_stats)
display(unit_stats)

print("Sales Mode:", df["sales"].mode().tolist())
print("Unit Mode:", df["unit"].mode().tolist())

group_sales = (
    df.groupby("group")["sales"]
    .sum()
    .sort_values(ascending=False)
)

group_units = (
    df.groupby("group")["unit"]
    .sum()
    .sort_values(ascending=False)
)

display(group_sales)
display(group_units)

highest_group = group_sales.idxmax()
lowest_group = group_sales.idxmin()

print("Highest Sales Group:", highest_group)
print("Lowest Sales Group:", lowest_group)

state_sales = (
    df.groupby("state")["sales"]
    .sum()
    .sort_values(ascending=False)
)

state_units = (
    df.groupby("state")["unit"]
    .sum()
    .sort_values(ascending=False)
)

display(state_sales)
display(state_units)

highest_state = state_sales.idxmax()
lowest_state = state_sales.idxmin()

print("Highest Sales State:", highest_state)
print("Lowest Sales State:", lowest_state)

state_group_sales = (
    df.groupby(["state", "group"])["sales"]
    .sum()
    .reset_index()
)

state_group_pivot = pd.pivot_table(
    df,
    values="sales",
    index="state",
    columns="group",
    aggfunc="sum"
)

display(state_group_sales)
display(state_group_pivot)

df["day"] = df["date"].dt.day
df["day_name"] = df["date"].dt.day_name()
df["week"] = df["date"].dt.isocalendar().week.astype(int)
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.month_name()
df["quarter"] = df["date"].dt.quarter

daily_report = (
    df.groupby("date")
    .agg(sales=("sales", "sum"), units=("unit", "sum"))
    .reset_index()
)

weekly_report = (
    df.groupby("week")
    .agg(sales=("sales", "sum"), units=("unit", "sum"))
    .reset_index()
)

monthly_report = (
    df.groupby(["month", "month_name"])
    .agg(sales=("sales", "sum"), units=("unit", "sum"))
    .reset_index()
    .sort_values("month")
)

quarterly_report = (
    df.groupby("quarter")
    .agg(sales=("sales", "sum"), units=("unit", "sum"))
    .reset_index()
)

display(daily_report)
display(weekly_report)
display(monthly_report)
display(quarterly_report)

if "time" in df.columns:
    df["time"] = df["time"].astype(str).str.strip().str.title()

    time_sales = (
        df.groupby("time")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    display(time_sales)

    if not time_sales.empty:
        max_sales = time_sales.idxmax()
        min_sales = time_sales.idxmin()

        print("Highest Sales Time:", max_sales)
        print("Lowest Sales Time:", min_sales)

plt.figure(figsize=(10, 6))
sns.histplot(df["sales"], kde=True, bins=30)
plt.title("Distribution of Sales")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df["unit"], kde=True, bins=30)
plt.title("Distribution of Units Sold")
plt.xlabel("Units")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(10, 5))
sns.boxplot(x=df["sales"])
plt.title("Box Plot of Sales")
plt.xlabel("Sales")
plt.show()

plt.figure(figsize=(10, 5))
sns.boxplot(x=df["unit"])
plt.title("Box Plot of Units Sold")
plt.xlabel("Units")
plt.show()

plt.figure(figsize=(12, 6))
sns.barplot(
    data=df,
    x="state",
    y="sales",
    estimator="sum",
    errorbar=None
)
plt.title("State-wise Sales")
plt.xlabel("State")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(
    data=df,
    x="group",
    y="sales",
    estimator="sum",
    errorbar=None
)
plt.title("Group-wise Sales")
plt.xlabel("Group")
plt.ylabel("Total Sales")
plt.show()

plt.figure(figsize=(14, 7))
sns.barplot(
    data=df,
    x="state",
    y="sales",
    hue="group",
    estimator="sum",
    errorbar=None
)
plt.title("State-wise Sales by Group")
plt.xlabel("State")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(14, 7))
sns.barplot(
    data=state_group_sales,
    x="group",
    y="sales",
    hue="state",
    errorbar=None
)
plt.title("Group-wise Sales Across States")
plt.xlabel("Group")
plt.ylabel("Total Sales")
plt.show()

plt.figure(figsize=(12, 7))
sns.heatmap(
    state_group_pivot,
    annot=True,
    fmt=".0f",
    cmap="YlGnBu"
)
plt.title("State-wise and Group-wise Sales")
plt.xlabel("Group")
plt.ylabel("State")
plt.show()

plt.figure(figsize=(14, 6))
sns.lineplot(
    data=daily_report,
    x="date",
    y="sales",
    marker="o"
)
plt.title("Daily Sales")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(12, 6))
sns.barplot(
    data=weekly_report,
    x="week",
    y="sales",
    errorbar=None
)
plt.title("Weekly Sales")
plt.xlabel("Week")
plt.ylabel("Sales")
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(
    data=monthly_report,
    x="month_name",
    y="sales",
    errorbar=None
)
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(8, 5))
sns.barplot(
    data=quarterly_report,
    x="quarter",
    y="sales",
    errorbar=None
)
plt.title("Quarterly Sales")
plt.xlabel("Quarter")
plt.ylabel("Sales")
plt.show()

if "time" in df.columns:
    time_order = ["Morning", "Afternoon", "Evening", "Night"]

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=df,
        x="time",
        y="sales",
        order=[x for x in time_order if x in df["time"].unique()],
        estimator="sum",
        errorbar=None
    )
    plt.title("Sales by Time of Day")
    plt.xlabel("Time of Day")
    plt.ylabel("Total Sales")
    plt.show()

state_sales_percentage = (
    state_sales / state_sales.sum() * 100
).round(2)

group_sales_percentage = (
    group_sales / group_sales.sum() * 100
).round(2)

display(state_sales_percentage)
display(group_sales_percentage)

display(state_sales.head(5))
display(state_sales.tail(5))

correlation = df[["sales", "unit"]].corr()

plt.figure(figsize=(7, 5))
sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)
plt.title("Sales and Units Correlation")
plt.show()

print("Highest Revenue State:", highest_state)
print("Lowest Revenue State:", lowest_state)
print("Highest Revenue Group:", highest_group)
print("Lowest Revenue Group:", lowest_group)

if "time" in df.columns and not time_sales.empty:
    print("Highest Sales Time:", max_sales)
    print("Lowest Sales Time:", min_sales)

