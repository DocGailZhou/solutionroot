# Fabric notebook source


# MARKDOWN ********************

# # Inventory Data Loading
# 
# This notebook loads all inventory-related CSV files from the lakehouse Files/data/inventory directory into Delta tables.
# 
# ## Tables to Load:
# 1. **Warehouses** - Distribution centers and storage facilities with operational details
# 2. **Inventory** - Current stock levels and warehouse information
# 3. **InventoryTransactions** - All stock movements and adjustments
# 4. **PurchaseOrders** - Purchase order headers with supplier information
# 5. **PurchaseOrderItems** - Purchase order line items with product details
# 6. **DemandForecast** - Predictive analytics for future demand planning

# CELL ********************

# Setup and Configuration
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Schema Configuration
SCHEMA_NAME = "inventory"
DATA_PATH = "Files/data/inventory"

# Ensure schema exists
spark.sql(f"CREATE DATABASE IF NOT EXISTS {SCHEMA_NAME}")
print(f"✅ Loading '{SCHEMA_NAME}' schema from: {DATA_PATH}")

# CELL ********************

# 1. Load Warehouses Table
warehouses_df = spark.read.csv(f"{DATA_PATH}/Warehouses.csv", header=True, inferSchema=True)
warehouses_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.Warehouses")
warehouses_count = warehouses_df.count()

# CELL ********************

# 2. Load Inventory Table
inventory_df = spark.read.csv(f"{DATA_PATH}/Inventory.csv", header=True, inferSchema=True)
inventory_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.Inventory")
inventory_count = inventory_df.count()

# CELL ********************

# 3. Load InventoryTransactions Table
transactions_df = spark.read.csv(f"{DATA_PATH}/InventoryTransactions.csv", header=True, inferSchema=True)
transactions_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.InventoryTransactions")
transactions_count = transactions_df.count()

# CELL ********************

# 4. Load PurchaseOrders Table
orders_df = spark.read.csv(f"{DATA_PATH}/PurchaseOrders.csv", header=True, inferSchema=True)
orders_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.PurchaseOrders")
orders_count = orders_df.count()

# CELL ********************

# 5. Load PurchaseOrderItems Table
order_items_df = spark.read.csv(f"{DATA_PATH}/PurchaseOrderItems.csv", header=True, inferSchema=True)
order_items_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.PurchaseOrderItems")
order_items_count = order_items_df.count()

# CELL ********************

# 6. Load DemandForecast Table
forecast_df = spark.read.csv(f"{DATA_PATH}/DemandForecast.csv", header=True, inferSchema=True)
forecast_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.DemandForecast")
forecast_count = forecast_df.count()

# CELL ********************

# Summary
total_records = warehouses_count + inventory_count + transactions_count + orders_count + order_items_count + forecast_count
print(f"✅ Inventory schema: 6 tables, {total_records:,} records loaded")
