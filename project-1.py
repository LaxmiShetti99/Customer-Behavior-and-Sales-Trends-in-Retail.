import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("shopping_trends.csv")

# Quick overview
print(df.info())
print(df.describe())
print(df.describe(include="all"))
print(df.isnull().sum())

# Normalize column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Rename specific column
df.rename(columns={"purchase_amount_(usd)": "purchase_amount"}, inplace=True)

# Final check
print( df.columns)

#creating a new column age_group
age_bins = [0, 18, 25, 35, 50, 65, 100]  
age_labels = ["Teen", "Young Adult", "Adult", "Middle Age", "Senior", "Elder"]
df["age_group"] = pd.cut(df["age"], bins=age_bins, labels=age_labels, right=False)

# Final check
print(df[["age", "age_group"]].head())

# Define mapping from frequency text to days
frequency_map = {
    'fortnightly':14,
    'weekly': 7,
    'monthly':30,
    'quarterly':90,
    'bi-weekly':14,
    'annually':365,
    'every 3 months':90
}

# Create purchase_frequency_days column
df["purchase_frequency_days"] = df["frequency_of_purchases"].str.lower().map(frequency_map)

# Check result
print(df[["frequency_of_purchases", "purchase_frequency_days"]].head())

# Checking discount and promo code data
print(df[['discount_applied','promo_code_used']].head())

# Check if ALL rows are equal
print((df["discount_applied"] == df["promo_code_used"]).all())
df = df.drop('promo_code_used',axis=1)
print(df.columns)

# Visualization Section
#1 Age distribution
plt.figure(figsize=(8,5))
sns.countplot(x="age_group", data=df, order=age_labels, color="lightgreen")
plt.title("Age Group Distribution")
plt.xlabel("Age Group")
plt.ylabel("Counts")
plt.show()

#2 Purchase amount distribution
plt.figure(figsize=(8,5))
sns.histplot(df["purchase_amount"], bins=20, kde=True, color="orange")
plt.title("Purchase Amount Distribution")
plt.xlabel("Purchase Amount")
plt.ylabel("Frequency")
plt.show()

#3 Gender vs Purchase Amount
plt.figure(figsize=(8,5))
sns.boxplot(x="gender", y="purchase_amount", data=df,color="lightgreen")
plt.title("Purchase Amount by Gender")
plt.show()

#4 Frequency of purchase by Category and Gender
gender_colors = {
    "Male": "black",
    "Female": "pink"}

plt.figure(figsize=(8,5))
sns.countplot(x="category", hue="gender", data=df, palette=gender_colors)
plt.title("Purchase Frequency by Category and Gender")
plt.xlabel("Category")
plt.ylabel("Count")
plt.xticks(rotation=0)   # keep labels straight
plt.legend(title="Gender")
plt.show()

#5 Correlation Heatmap 
plt.figure(figsize=(10,8))
sns.heatmap(
    df.corr(numeric_only=True),
    annot=True,
    cmap="coolwarm",
    annot_kws={"size":12})   

plt.title("Correlation Heatmap", fontsize=16)   
plt.xticks(fontsize=12)                         
plt.yticks(fontsize=12)                         
plt.show()


#6 Dominance of category in each location
import seaborn as sns
category_counts = df.groupby(["location","category"]).size().unstack(fill_value=0)
plt.figure(figsize=(8,5))
sns.heatmap(category_counts, annot=True, cmap="YlGnBu", fmt="d")

plt.title("Purchases by Location and Category")
plt.xlabel("Category")
plt.ylabel("Location")
plt.show()

#7 Average spending per location
location_counts = df["location"].value_counts()
plt.figure(figsize=(8,5))
sns.barplot(y=location_counts.index, x=location_counts.values, palette="Set2")
plt.title("Purchases by Location")
plt.xlabel("Count")
plt.ylabel("Location")
plt.show()


#8 Top Spenders
top_spenders = df.groupby("customer_id")["purchase_amount"].sum().sort_values(ascending=False).head(10)
print("Top 10 Spenders:\n", top_spenders)

plt.figure(figsize=(8,5))
top_spenders.plot(kind="bar", color="teal")

plt.title("Top 10 Customers by Total Spending", fontsize=16)
plt.xlabel("Customer ID", fontsize=14)
plt.ylabel("Total Purchase Amount", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()


#9 Category Profitability
category_profit = df.groupby("category")["purchase_amount"].mean().sort_values(ascending=False)
print("Average Purchase Amount per Category:\n", category_profit)

plt.figure(figsize=(8,5))
category_profit.plot(kind="bar", color="purple")

plt.title("Average Spending per Category", fontsize=16)
plt.xlabel("Category", fontsize=14)
plt.ylabel("Avg Purchase Amount", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()


#10 Subscription Impact
subscription_impact = df.groupby("subscription_status")["purchase_amount"].mean()
print("Average Spending by Subscription Status:\n", subscription_impact)

plt.figure(figsize=(6,4))
subscription_impact.plot(kind="bar", color="green")

plt.title("Average Spending: Subscribers vs Non-Subscribers", fontsize=14)
plt.xlabel("Subscription Status", fontsize=12)
plt.ylabel("Avg Purchase Amount", fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()


#11. Seasonality Check
season_sales = df.groupby("season")["purchase_amount"].sum().sort_values(ascending=False)
print("Total Sales by Season:\n", season_sales)
plt.figure(figsize=(8,5))
season_sales.plot(kind="bar", color="orange")

plt.title("Total Sales by Season", fontsize=14)
plt.xlabel("Season", fontsize=14)
plt.ylabel("Total Purchase Amount", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()


#12 Review Impact
plt.figure(figsize=(8,5))
sns.scatterplot(x="review_rating", y="purchase_amount", data=df, alpha=0.6)
plt.title("Review Rating vs Purchase Amount")
plt.xlabel("Review Rating")
plt.ylabel("Purchase Amount")
plt.show()

correlation = df["review_rating"].corr(df["purchase_amount"])
print("Correlation between Review Rating and Purchase Amount:", correlation)


# Export the cleaned dataset to a new CSV
df.to_csv("shopping_trends_cleaned.csv", index=False)

# Print confirmation
print("Cleaned dataset has been exported as 'shopping_trends_cleaned.csv'")


#connection of Python to Mysql command Line
import mysql.connector

conn = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"   # create this in CLI first: CREATE DATABASE mydb;
)
cursor = conn.cursor()
print("Connection successful!")

# Exported the CSV data into Mysql command line
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:8laxmi992003@localhost/retail_sales")

df = pd.read_csv("shopping_trends_cleaned.csv")
df.to_sql("sales_data", con=engine, if_exists="replace", index=False)

print("CSV loaded into MySQL table 'sales_data'")


#SQL QUERIES
import mysql.connector
import pandas as pd
conn = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",   
    database="your_database")

#Q1 What is the total revenue generated my male and female customers?
query = """
SELECT gender, SUM(purchase_amount) AS revenue
FROM sales_data
GROUP BY gender;
"""
df = pd.read_sql(query, conn)
print(df)

#Q2 Which customer used discount but still spent more than the average purchase amount?
query = """
SELECT customer_id, purchase_amount
FROM sales_data
WHERE discount_applied='Yes' and purchase_amount>(SELECT AVG(purchase_amount) from sales_data);"""
df = pd.read_sql(query,conn)
print(df)

#Q3 Which are the top5 products with the highest average review rating?
query = """
SELECT item_purchased, ROUND(AVG(review_rating), 2) AS Average_Product_Rating
FROM sales_data
GROUP BY item_purchased
ORDER BY AVG(review_rating) DESC LIMIT 5;""" 
df = pd.read_sql(query, conn)
print(df)

#Q4 Compare the average purchase amount between Standard and Express Shipping
query = """
SELECT shipping_type,
ROUND (AVG(purchase_amount),2)
FROM sales_data
WHERE shipping_type in ('Standard','Express')
GROUP BY shipping_type;"""
df = pd.read_sql(query, conn)
print(df)

#Q5 Do subscribed customers spend more? Compare average spend and total revenue between subscribed and non-subscribed customers
query = """
SELECT subscription_status,
COUNT(customer_id) as total_customers,
ROUND(AVG(purchase_amount),2) as average_spend,
ROUND(SUM(purchase_amount),2) as total_revenue
FROM sales_data
GROUP BY subscription_status
ORDER BY total_revenue DESC, average_spend DESC;"""
df = pd.read_sql(query, conn)
print(df)

#Q6 Which 5 products have the highest percentage of purchases with discoung applied?
query = """
SELECT item_purchased,ROUND(100 * SUM(CASE WHEN discount_applied='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS discount_rate
FROM sales_data
GROUP BY item_purchased
ORDER BY discount_rate DESC
LIMIT 5;"""
df = pd.read_sql(query, conn)
print(df)

#Q7 Segment customers into new, returning and loyal based on their total number of previous purchases and show the count of each segment
query = """
WITH customer_type AS (
    SELECT customer_id,
           previous_purchases,
           CASE
               WHEN previous_purchases = 1 THEN 'New'
               WHEN previous_purchases BETWEEN 2 AND 10 THEN 'Returning'
               ELSE 'Loyal'
           END AS customer_segment
    FROM sales_data)
SELECT customer_segment,
       COUNT(*) AS Number_of_customers
FROM customer_type
GROUP BY customer_segment;"""
df = pd.read_sql(query, conn)
print(df)

#Q8 What are the top 3 most purchased products within each category
query = """
WITH item_counts AS (
    SELECT 
        category,
        item_purchased,
        COUNT(customer_id) AS total_orders,
        ROW_NUMBER() OVER (
            PARTITION BY category 
            ORDER BY COUNT(customer_id) DESC
        ) AS item_rank
    FROM sales_data
    GROUP BY category, item_purchased)
SELECT 
    item_rank,
    category,
    item_purchased,
    total_orders
FROM item_counts
WHERE item_rank <= 3
ORDER BY category, item_rank;"""
df = pd.read_sql(query, conn)
print(df)

#Q9 Are customers who are repeat buyers (more than 5 previous purchases) are likely to subscribe?
query = """
SELECT subscription_status,
COUNT(customer_id) AS repeat_buyers
FROM sales_data
WHERE previous_purchases>5
GROUP BY subscription_status;"""
df = pd.read_sql(query, conn)
print(df)

#Q10 What is the revenue contribution of each age group
query = """
SELECT age_group,
SUM(purchase_amount) as total_revenue
FROM sales_data
GROUP BY age_group
ORDER BY total_revenue DESC;"""
df = pd.read_sql(query, conn)
print(df)


conn.close()
print("Connection closed")




