# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "7bc5f01b-929f-4d7f-a7f4-165a36c3a7c5",
# META       "default_lakehouse_name": "miqdata",
# META       "default_lakehouse_workspace_id": "2948455a-3fb0-46d0-b1c3-2375575d3ee4",
# META       "known_lakehouses": [
# META         {
# META           "id": "7bc5f01b-929f-4d7f-a7f4-165a36c3a7c5"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Data Model for Customer and Product Dimentions. 
# 
# ## Schema Structure
# - **Customer Management (5 tables)**: 
# - Customer, Samples Ready: Customer_Samples.csv 
# - CustomerRelationshipType, Samples Ready: CustomerRelationshipType_samples.csv
# - CustomerTradeName, Samples Ready: CustomerTradeNames_Samples.csv
# - Location, Samples Ready: Location_Samples.csv
# - CustomerAccount, Samples Ready: CustomerAccount_Samples.csv


# MARKDOWN ********************


# CELL ********************

################################################################################################
# Schema Configuration - You can define different value here
################################################################################################

# Schema Configuration
SCHEMA_NAME = "customer"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}")
print(f"✅ {SCHEMA_NAME} schema ready!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


################################################################################################
# Customer Domain - Customer with Contact Info, Customer Accounts, Locations, etc. 5 Tables
################################################################################################

# 1. Create Customer table  
TABLE_NAME = "Customer"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    CustomerId STRING,
    CustomerTypeId STRING, --Individual, Business, Government
    CustomerRelationshipTypeId STRING,
    DateOfBirth DATE,
    CustomerEstablishedDate DATE,
    IsActive BOOLEAN,
    FirstName STRING,
    LastName STRING,
    Gender STRING,
    PrimaryPhone STRING,
    SecondaryPhone STRING,
    PrimaryEmail STRING,
    SecondaryEmail STRING,
    CreatedBy STRING
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")


# 2. Create CustomerTradeName table
TABLE_NAME = "CustomerTradeName"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    CustomerId STRING,
    CustomerTypeId STRING, --Individual, Business, Government
    TradeNameId STRING,   
    TradeName STRING,
    PeriodStartDate DATE,
    PeriodEndDate DATE,
    CustomerTradeNameNote STRING
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")


# 3. Create CustomerRelationshipType table
TABLE_NAME = "CustomerRelationshipType"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    CustomerRelationshipTypeId STRING,  -- Individual: Standard, Premium, VIP. Business: SMB, Premier, Partner. Government: Federal, State, Local.
    CustomerRelationshipTypeName STRING,
    CustomerRelationshipTypeDescription STRING
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")


# 4. Create Location table
TABLE_NAME = "Location"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    LocationId STRING,
    CustomerId STRING,
    LocationName STRING,
    IsActive BOOLEAN,
    AddressLine1 STRING,  -- "1000 Main St" 
    AddressLine2 STRING,  -- "Apt 5" or "Suite 200"
    City STRING,
    StateId STRING,
    ZipCode STRING,
    CountryId STRING,
    SubdivisionName STRING,
    Region STRING,        -- "Northeast", "West Coast", "Midwest"
    Latitude DECIMAL(10,7),
    Longitude DECIMAL(10,7),
    Note STRING
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")

# 5. Create CustomerAccount table
TABLE_NAME = "CustomerAccount"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    CustomerAccountId STRING,
    ParentAccountId STRING,
    CustomerAccountName STRING,
    CustomerId STRING,
    IsoCurrencyCode STRING
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
