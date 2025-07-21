import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = r"C:\Users\LENOVO\Desktop\E-Commerce Revenue Analysis\E-Commerce-Revenue-Analysis\Data.csv"
df = pd.read_csv(file_path)

# Display first few rows to understand the data
print("First 5 Rows of the Dataset:\n", df.head())

# Check for missing values
missing_values = df.isnull().sum()
print("\nMissing Values in Each Column:\n", missing_values)

# Check for duplicate rows
duplicate_rows = df.duplicated().sum()
print("\nNumber of Duplicate Rows:", duplicate_rows)

# Display dataset information
df.info()

# Step 1: Revenue Calculation and Grouping
# Convert Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Drop rows with invalid dates (if any)
df = df.dropna(subset=['Date'])

# Calculate revenue per transaction
df['Revenue'] = df['Price'] * df['Quantity']

# Group revenue by CustomerNo
df_grouped = df.groupby('CustomerNo')['Revenue'].sum().reset_index()

# Sort customers by total revenue in descending order
df_grouped = df_grouped.sort_values(by='Revenue', ascending=False)

# Display top 10 high-revenue customers
print("\nTop 10 High-Revenue Customers:\n", df_grouped.head(10))

# Step 2: Monthly Revenue Analysis
df['Year-Month'] = df['Date'].dt.to_period('M')

# Group by Year-Month and sum the revenue
monthly_revenue = df.groupby('Year-Month')['Revenue'].sum().reset_index()

# Convert Year-Month to string format for better plotting
monthly_revenue['Year-Month'] = monthly_revenue['Year-Month'].astype(str)

# Display Monthly Revenue
print("\nMonthly Revenue Trends:\n", monthly_revenue)

# Plot the Monthly Revenue Trend
plt.figure(figsize=(12, 6))
plt.plot(monthly_revenue['Year-Month'], monthly_revenue['Revenue'], marker='o', linestyle='-', color='b')

# Formatting the plot
plt.xticks(rotation=45)  # Rotate x-axis labels
plt.xlabel("Year-Month")
plt.ylabel("Revenue")
plt.title("Monthly Revenue Trends")
plt.grid(True)

# Show the plot
plt.show()

# Step 3: Customer Segmentation
# Define revenue categories
def categorize_revenue(revenue):
    if revenue <= 1000:
        return 'Low'
    elif 1001 <= revenue <= 5000:
        return 'Medium'
    elif 5001 <= revenue <= 10000:
        return 'High'
    else:
        return 'Very High'

# Apply categorization to create a new column
df_grouped['Revenue_Category'] = df_grouped['Revenue'].apply(categorize_revenue)

# Display to verify
print("\nCustomer Segmentation:\n", df_grouped.head())

# Count customers in each revenue category
category_counts = df_grouped['Revenue_Category'].value_counts()

# Calculate percentage
category_percentages = (category_counts / category_counts.sum()) * 100

# Print the percentage of customers in each category
print("\nCustomer Segmentation Percentage:\n", category_percentages)

# Plot customer segmentation
plt.figure(figsize=(8, 5))
category_counts.plot(kind='bar', color=['blue', 'orange', 'green', 'red'])
plt.xlabel("Revenue Category")
plt.ylabel("Number of Customers")
plt.title("Customer Segmentation by Revenue Category")
plt.xticks(rotation=0)
plt.show()

# Step 4: Bar Plot for Top 10 High-Revenue Customers
plt.figure(figsize=(10, 5))
plt.bar(df_grouped['CustomerNo'].head(10), df_grouped['Revenue'].head(10), color='purple')
plt.xlabel("Customer No")
plt.ylabel("Total Revenue")
plt.title("Top 10 High-Revenue Customers")
plt.xticks(rotation=45)
plt.show()
