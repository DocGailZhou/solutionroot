# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # Sales Data Loading
# 
# This notebook loads all sales-related CSV files from three product line directories into Delta tables.
# 
# ## Data Sources:
# - **Camping**: Files/data/sales/camping/
# - **Kitchen**: Files/data/sales/kitchen/
# - **Ski**: Files/data/sales/ski/
# 
# ## Tables to Load:
# 1. **Order** - Order headers from all three product lines
# 2. **OrderLine** - Order line items from all three product lines  
# 3. **OrderPayment** - Payment information from all three product lines

# CELL ********************

# Setup and Configuration
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Schema Configuration
SCHEMA_NAME = "sales"
BASE_PATH = "Files/data/sales"

# Product line paths
PRODUCT_LINES = ['camping', 'kitchen', 'ski']

# Ensure schema exists
spark.sql(f"CREATE DATABASE IF NOT EXISTS {SCHEMA_NAME}")
print(f"✅ Loading '{SCHEMA_NAME}' schema from {len(PRODUCT_LINES)} product lines: {', '.join(PRODUCT_LINES)}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 1. Load Order Table from All Product Lines
order_dfs = []
for product_line in PRODUCT_LINES:
    order_df = spark.read.csv(f"{BASE_PATH}/{product_line}/Order_Samples_{product_line.title()}.csv", header=True, inferSchema=True)
    order_dfs.append(order_df)

# Union all order dataframes
combined_orders_df = order_dfs[0]
for df in order_dfs[1:]:
    combined_orders_df = combined_orders_df.union(df)

combined_orders_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.Order")
orders_count = combined_orders_df.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 2. Load OrderLine Table from All Product Lines
orderline_dfs = []
for product_line in PRODUCT_LINES:
    orderline_df = spark.read.csv(f"{BASE_PATH}/{product_line}/OrderLine_Samples_{product_line.title()}.csv", header=True, inferSchema=True)
    orderline_dfs.append(orderline_df)

# Union all orderline dataframes
combined_orderlines_df = orderline_dfs[0]
for df in orderline_dfs[1:]:
    combined_orderlines_df = combined_orderlines_df.union(df)

combined_orderlines_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.OrderLine")
orderlines_count = combined_orderlines_df.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 3. Load OrderPayment Table from All Product Lines
orderpayment_dfs = []
for product_line in PRODUCT_LINES:
    # Handle different file naming conventions
    if product_line == "camping":
        file_name = "OrderPayment_Camping.csv"
    elif product_line == "kitchen":
        file_name = "OrderPayment_Kitchen.csv" 
    else:  # ski
        file_name = "OrderPayment_Ski.csv"
    
    orderpayment_df = spark.read.csv(f"{BASE_PATH}/{product_line}/{file_name}", header=True, inferSchema=True)
    orderpayment_dfs.append(orderpayment_df)

# Union all order payment dataframes
combined_payments_df = orderpayment_dfs[0]
for df in orderpayment_dfs[1:]:
    combined_payments_df = combined_payments_df.union(df)

combined_payments_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.OrderPayment")
payments_count = combined_payments_df.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Summary
total_records = orders_count + orderlines_count + payments_count
print(f"✅ Sales schema: 3 tables, {total_records:,} records loaded")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
