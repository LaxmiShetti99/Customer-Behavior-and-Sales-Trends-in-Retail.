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
