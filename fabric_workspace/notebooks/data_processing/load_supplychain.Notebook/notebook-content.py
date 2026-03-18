# Fabric notebook source


# MARKDOWN ********************

# # Supply Chain Data Loading
# 
# This notebook loads all supply chain-related CSV files from the lakehouse Files/data/supplychain directory into Delta tables.
# 
# ## Tables to Load:
# 1. **Suppliers** - Master supplier data with backup relationships and performance metrics
# 2. **ProductSuppliers** - Product-supplier mappings with pricing and order parameters
# 3. **SupplyChainEvents** - Supply chain disruption events and impact tracking

# CELL ********************

# Setup and Configuration
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Schema Configuration
SCHEMA_NAME = "supplychain"
DATA_PATH = "Files/data/supplychain"

# Ensure schema exists
spark.sql(f"CREATE DATABASE IF NOT EXISTS {SCHEMA_NAME}")
print(f"✅ Loading '{SCHEMA_NAME}' schema from: {DATA_PATH}")

# CELL ********************

# 1. Load Suppliers Table
suppliers_df = spark.read.csv(f"{DATA_PATH}/Suppliers.csv", header=True, inferSchema=True)
suppliers_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.Suppliers")
suppliers_count = suppliers_df.count()

# CELL ********************

# 2. Load ProductSuppliers Table
product_suppliers_df = spark.read.csv(f"{DATA_PATH}/ProductSuppliers.csv", header=True, inferSchema=True)
product_suppliers_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.ProductSuppliers")
product_suppliers_count = product_suppliers_df.count()

# CELL ********************

# 3. Load SupplyChainEvents Table
supply_chain_events_df = spark.read.csv(f"{DATA_PATH}/SupplyChainEvents.csv", header=True, inferSchema=True)
supply_chain_events_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{SCHEMA_NAME}.SupplyChainEvents")
events_count = supply_chain_events_df.count()

# CELL ********************

# Summary
total_records = suppliers_count + product_suppliers_count + events_count
print(f"✅ Supplychain schema: 3 tables, {total_records:,} records loaded")
