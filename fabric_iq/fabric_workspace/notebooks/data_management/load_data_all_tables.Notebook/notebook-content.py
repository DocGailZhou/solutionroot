# Fabric notebook source


# MARKDOWN ********************

# # Load All Data 
# 
# ## Overview
# This notebook orchestrates the loading of all CSV data files into Delta tables for the business data platform.
# 
# **Execution Order**: Foundational domains first (customer, product) → Business processes (sales, finance) → Operations (inventory, supplychain)
# 
# **Prerequisites**: 
# - Fabric lakehouse properly configured
# - PySpark session active

# MARKDOWN ********************

# ## Prepare Clean Environment
# 
# **⚠️ Warning**: Uncomment the line below only if you want to completely reload all data.
# 
# **Recommendation**: Run selectively for development/testing environments only.

# CELL ********************

# %run truncate_all_tables

# MARKDOWN ********************

# ### Load data for customer domain

# CELL ********************

%run load_customer

# MARKDOWN ********************

# ### Load data for product domain

# CELL ********************

%run load_product

# MARKDOWN ********************

# ### Load data for sales domain 

# CELL ********************

%run load_sales

# MARKDOWN ********************

# ### Load data for finance domain

# CELL ********************

%run load_finance

# MARKDOWN ********************

# ### Load data for inventory domain

# CELL ********************

%run load_inventory

# MARKDOWN ********************

# ### Load data for supplychain domain

# CELL ********************

%run load_supplychain
