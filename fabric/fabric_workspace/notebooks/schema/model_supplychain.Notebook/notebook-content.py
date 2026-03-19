# Fabric notebook source


# MARKDOWN ********************

# # Supply Chain Data Model - Suppliers & Disruptions
# 
# ## Schema Structure
# - **Suppliers Table**: Master data for product suppliers/distributors with backup relationships
# - **ProductSuppliers Table**: Links products to suppliers with pricing and terms
# - **SupplyChainEvents Table**: Consolidated disruption events and their impacts (merged from 2 tables)
# - Supports Primary/Backup supplier hierarchies and streamlined disruption analysis

# CELL ********************

################################################################################################
# Schema Configuration - You can define different value here
################################################################################################

# Schema Configuration
SCHEMA_NAME = "supplychain"
spark.sql(f"CREATE DATABASE IF NOT EXISTS {SCHEMA_NAME}")
print(f"✅ {SCHEMA_NAME} schema ready!")

# CELL ********************

################################################################################################
# Supply Chain Domain - Suppliers and Product-Supplier Mapping Tables
################################################################################################

# CELL ********************

# Create all Supply Chain tables - Suppliers, ProductSuppliers, and SupplyChainEvents

# 1. Create Suppliers table
TABLE_NAME = "Suppliers"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    SupplierID INT,
    SupplierName STRING,
    SupplierType STRING,  -- Primary, Backup, Emergency
    Status STRING,        -- Active, Disrupted, Inactive  
    ProductCategory STRING, -- Camping, Kitchen, Ski, Multi
    PrimarySupplierID INT,  -- NULL for primary suppliers
    LeadTimeDays INT,     -- Standard delivery time
    ReliabilityScore INT, -- 0-100 performance rating
    Location STRING,      -- City, Country
    ContactEmail STRING,  -- Primary contact
    CreatedBy STRING,     -- System user
    CreatedDate TIMESTAMP -- Record creation
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")

# 2. Create ProductSuppliers mapping table
TABLE_NAME = "ProductSuppliers"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    ProductSupplierID INT,
    ProductID INT,            -- Links to existing Product table
    ProductName STRING,       -- Denormalized for usability
    ProductCategory STRING,   -- Camping, Kitchen, Ski
    SupplierID INT,          -- Links to Suppliers table
    SupplierName STRING,     -- Denormalized for usability
    SupplierProductCode STRING, -- Supplier's internal SKU
    WholesaleCost DECIMAL(10,2), -- Cost per unit
    MinOrderQuantity INT,    -- Minimum order size
    MaxOrderQuantity INT,    -- Maximum order size (NULL = no limit)
    LeadTimeDays INT,        -- Product-specific lead time
    Status STRING,           -- Active, Discontinued
    CreatedBy STRING,        -- System user
    CreatedDate TIMESTAMP    -- Record creation
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")

# 3. Create SupplyChainEvents consolidated table
# Combines disruption events and their impacts in single table
TABLE_NAME = "SupplyChainEvents"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    EventID INT,
    DisruptionType STRING,     -- Weather, Political, Economic, Pandemic, Transport, Supplier
    EventName STRING,          -- Short descriptive name
    Description STRING,        -- Detailed description
    Severity STRING,           -- Low, Medium, High, Critical
    Status STRING,             -- Active, Monitoring, Resolved
    StartDate DATE,            -- When disruption began
    EndDate DATE,              -- When disruption resolved (NULL if ongoing)
    GeographicArea STRING,     -- Affected region/country
    IndustryImpact STRING,     -- Outdoor, Retail, Manufacturing, Logistics
    PredictedDuration INT,     -- Expected duration in days
    ActualDuration INT,        -- Actual duration in days (NULL if ongoing)
    AlertLevel STRING,         -- Green, Yellow, Orange, Red
    ReportedBy STRING,         -- Who reported the disruption
    -- Impact Details (nullable for general events)
    ImpactType STRING,         -- SupplierDown, DelayedShipment, PriceIncrease, ProductUnavailable
    SupplierID INT,            -- Which supplier affected (NULL if general)
    SupplierName STRING,       -- Denormalized for usability
    ProductID INT,             -- Which product affected (NULL if all supplier products)
    ProductName STRING,        -- Denormalized for usability
    ProductCategory STRING,    -- Camping, Kitchen, Ski (NULL if all categories)
    ImpactSeverity STRING,     -- Low, Medium, High, Critical
    ExpectedDelayDays INT,     -- Additional lead time due to disruption
    CostImpactPercent DECIMAL(5,2), -- Price increase percentage
    AvailabilityImpact STRING, -- Available, Limited, Unavailable
    MitigationAction STRING,   -- Alternative supplier, expedited shipping, etc.
    ImpactStartDate DATE,      -- When this specific impact began
    ImpactEndDate DATE,        -- When this specific impact resolved
    EstimatedLoss DECIMAL(12,2), -- Financial impact estimate
    Notes STRING,              -- Additional context and impact details
    CreatedBy STRING,          -- System user
    CreatedDate TIMESTAMP      -- Record creation
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")

print("\n🎉 All Supply Chain tables created successfully!")
