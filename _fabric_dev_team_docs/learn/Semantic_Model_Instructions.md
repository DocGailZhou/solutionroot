# Building Semantic Model in Fabric Portal - Product, Inventory & Supply Chain

This guide walks through creating a semantic model in Microsoft Fabric using only the Product, Inventory, and Supply Chain domains from your lakehouse data.

---

## **Step 1: Create the Semantic Model**

### 1.1 Access Your Fabric Workspace
- Go to [app.fabric.microsoft.com](https://app.fabric.microsoft.com)
- Navigate to your workspace (the one containing `fabriciq_team_lake`)
- Ensure you're in **Data Engineering** or **Business Intelligence** experience

### 1.2 Create New Semantic Model
- Click **+ New** button in the top-left
- Select **Semantic model (default)** from the dropdown
- In the "Create a semantic model" dialog:
  - **Name**: Enter `Supply Chain Analytics Model` (or your preferred name)
  - **Data source**: Select **Lakehouse**
  - Click **Continue**

### 1.3 Connect to Your Lakehouse
- In the "Choose your lakehouse" dialog:
  - Select **fabriciq_team_lake** from the list
  - Click **Confirm**

---

## **Step 2: Select Tables and Import Data**

### 2.1 Choose Tables by Schema
You'll see a table selection interface. Select only these 11 tables from the 3 target domains:

**Product Domain (2 tables):**
- ☑️ `product.Product`
- ☑️ `product.ProductCategory`

**Inventory Domain (6 tables):**
- ☑️ `inventory.Warehouses`
- ☑️ `inventory.Inventory`
- ☑️ `inventory.InventoryTransactions`
- ☑️ `inventory.PurchaseOrders`
- ☑️ `inventory.PurchaseOrderItems`
- ☑️ `inventory.DemandForecast`

**Supply Chain Domain (3 tables):**
- ☑️ `supplychain.Suppliers`
- ☑️ `supplychain.ProductSuppliers`
- ☑️ `supplychain.SupplyChainEvents`

**Leave unchecked**: All `customer`, `sales`, and `finance` tables

### 2.2 Load the Tables
- Click **Load** to import all selected tables
- Wait for the loading process to complete (may take 1-2 minutes for 11 tables)

---

## **Step 3: Set Up the Data Model**

### 3.1 Access Relationship Management
In the Fabric portal model view:
- Look for **"Manage relationships"** button in the top ribbon/toolbar
- OR right-click on the canvas → **"Manage relationships"**
- This will open the relationships management dialog

### 3.2 Create New Relationship
In the Manage Relationships dialog:
1. Click **"New relationship"** or **"+ New"**
2. You'll see two dropdown menus for **From table** and **To table**
3. First dropdown: Select **Column** from the relevant table
4. Second dropdown: Select the **Related column** from the target table

### 3.3 Create These Relationships One by One
Work through these relationships in the Manage Relationships dialog:

**Relationship 1:**
- **From table**: `ProductCategory`
- **From column**: `CategoryID`
- **To table**: `Product` 
- **To column**: `ProductCategoryID`
- **Cardinality**: One to Many (1:m) - One category has many products
- Click **OK** or **Create**

**Relationship 2:**
- **From table**: `Product`
- **From column**: `ProductID`
- **To table**: `Inventory`
- **To column**: `ProductID`
- **Cardinality**: One to Many (1:m) - One product has inventory in multiple warehouses
- Click **OK**

**Relationship 3:**
- **From table**: `Product`
- **From column**: `ProductID`
- **To table**: `InventoryTransactions`
- **To column**: `ProductID`
- **Cardinality**: One to Many (1:m) - One product has many inventory transactions
- Click **OK**

**Relationship 4:**
- **From table**: `Product`
- **From column**: `ProductID`
- **To table**: `PurchaseOrderItems`
- **To column**: `ProductID`
- **Cardinality**: One to Many (1:m) - One product appears in many purchase order items
- Click **OK**

**Relationship 5:**
- **From table**: `Product`
- **From column**: `ProductID`
- **To table**: `DemandForecast`
- **To column**: `ProductID`
- **Cardinality**: One to Many (1:m) - One product has multiple forecast periods
- Click **OK**

**Relationship 6:**
- **From table**: `Warehouses`
- **From column**: `WarehouseID`
- **To table**: `Inventory`
- **To column**: `WarehouseLocation`
- **Cardinality**: One to Many (1:m) - One warehouse stores many products
- **Note**: `WarehouseID` values are "Main", "Backup", "Regional"
- Click **OK**

**Relationship 7:**
- **From table**: `Warehouses`
- **From column**: `WarehouseID`
- **To table**: `InventoryTransactions`
- **To column**: `WarehouseLocation`
- **Cardinality**: One to Many (1:m) - One warehouse has many transactions
- Click **OK**

**Relationship 8:**
- **From table**: `Warehouses`
- **From column**: `WarehouseID`
- **To table**: `PurchaseOrders`
- **To column**: `DeliveryLocation`
- **Cardinality**: One to Many (1:m) - One warehouse receives many purchase orders
- Click **OK**

**Relationship 9:**
- **From table**: `PurchaseOrders`
- **From column**: `PurchaseOrderID`
- **To table**: `PurchaseOrderItems`
- **To column**: `PurchaseOrderID`
- **Cardinality**: One to Many (1:m) - One purchase order has many line items
- Click **OK**

**Relationship 10:**
- **From table**: `Suppliers`
- **From column**: `SupplierID`
- **To table**: `PurchaseOrders`
- **To column**: `SupplierID`
- **Cardinality**: One to Many (1:m) - One supplier fulfills many purchase orders
- Click **OK**

**Relationship 11:**
- **From table**: `Suppliers`
- **From column**: `SupplierID`
- **To table**: `ProductSuppliers`
- **To column**: `SupplierID`
- **Cardinality**: One to Many (1:m) - One supplier provides many products
- Click **OK**

**Relationship 12:**
- **From table**: `Suppliers`
- **From column**: `SupplierID`
- **To table**: `SupplyChainEvents`
- **To column**: `SupplierID`
- **Cardinality**: One to Many (1:m) - One supplier can have many disruption events
- **Note**: Some events may have NULL SupplierID (general market events)
- Click **OK**

**Relationship 13:**
- **From table**: `Product`
- **From column**: `ProductID`
- **To table**: `ProductSuppliers`
- **To column**: `ProductID`
- **Cardinality**: One to Many (1:m) - One product can have multiple suppliers
- Click **OK**

### 3.4 Verify Your Relationships
After creating all relationships:
- In the Manage Relationships dialog, you should see all 13 relationships listed
- Check that **Active** column shows "Yes" for all relationships
- **Cardinality** should show "One to Many" for all relationships
- Click **Close** to return to the model view

---

## **Step 4: Configure Data Model Properties**

### 4.1 Create Date Table
Since we removed sales tables, create a date table for time-based analysis:
- Right-click in empty canvas space → **New table**
- Enter this DAX formula:
```dax
DateTable = 
ADDCOLUMNS(
    CALENDAR(DATE(2022,1,1), DATE(2026,12,31)),
    "Year", YEAR([Date]),
    "Month", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMMM"),
    "Quarter", "Q" & QUARTER([Date]),
    "Weekday", WEEKDAY([Date]),
    "WeekdayName", FORMAT([Date], "dddd")
)
```
- Right-click the new DateTable → **Mark as date table**
- Choose **"Date"** as the date column

### 4.2 Connect DateTable to Transaction Date Fields  
Create relationships between your DateTable and date fields using **"Manage relationships"** → **"New relationship"**:

| **Relationship** | **From Table** | **From Column** | **To Table** | **To Column** | **Status** | **Notes** |
|---|---|---|---|---|---|---|
| **1: Inventory Transactions** | DateTable | Date | InventoryTransactions | TransactionDate | ✅ Active | Core time intelligence |
| **2: Purchase Orders** | DateTable | Date | PurchaseOrders | OrderDate | ✅ Active | Order trends over time |
| **3: Demand Forecast** | DateTable | Date | DemandForecast | ForecastDate | ❌ Skip | **Ambiguous paths error***  |
| **4: Supply Chain Events** | DateTable | Date | SupplyChainEvents | StartDate | ✅ Active | Event timeline analysis |

**Ambiguous Paths Issue:** DemandForecast creates multiple relationship paths between InventoryTransactions and Product:

- Direct: InventoryTransactions → Product  
- Indirect: InventoryTransactions → DateTable → DemandForecast → Product

**Recommendation:** Skip this relationship to avoid model conflicts. The core time intelligence works with relationships 1, 2, and 4.

**Verify Date Relationships:**
- In Manage Relationships dialog, you should see 3 active date relationships
- DateTable now connects to your key time-based transaction tables

---

## **Step 5: Format Data and Create Measures**

### 5.1 Set Data Types and Formats
**Currency Fields:**
- Select `product_Product.ListPrice`, `product_Product.StandardCost` 
- Set **Data Type** = `Decimal number` 
- Set **Format** = `Currency ($)`
- Select `inventory_Inventory.AverageCost`, `supplychain_ProductSuppliers.WholesaleCost`
- Set **Data Type** = `Decimal number`
- Set **Format** = `Currency ($)`

---

## **Step 6: Create Core Business Measures**

### 6.1 Add Key Performance Measures
Create each measure individually by clicking the three dots (...) on the **Inventory** table → **New measure**:

**Inventory Health Measures** (create one at a time):
```dax
Total Current Stock = SUM(Inventory[CurrentStock])
```
```dax
Total Available Stock = SUM(Inventory[AvailableStock])
```
```dax
Total Reserved Stock = SUM(Inventory[ReservedStock])
```
```dax
Stock Fill Rate % = DIVIDE([Total Available Stock], [Total Current Stock], 0) * 100
```
```dax
Low Stock Items = COUNTROWS(FILTER(Inventory, Inventory[CurrentStock] < Inventory[ReorderPoint]))
```

**Supply Chain Measures** (click three dots (...) on **Suppliers** table → **New measure** for each):
```dax
Active Suppliers = COUNTROWS(FILTER(Suppliers, Suppliers[Status] = "Active"))
```
```dax
Average Reliability Score = AVERAGE(Suppliers[ReliabilityScore])
```
```dax
Active Disruptions = COUNTROWS(FILTER(SupplyChainEvents, SupplyChainEvents[Status] = "Active"))
```
```dax
Average Lead Time Days = AVERAGE(ProductSuppliers[LeadTimeDays])
```

**Product Performance Measures** (click three dots (...) on **Product** table → **New measure** for each):
```dax
Total Products = COUNTROWS(Product)
```
```dax
Active Products = COUNTROWS(FILTER(Product, Product[ProductStatus] = "active"))
```
```dax
Average Product Cost = AVERAGE(Product[StandardCost])
```
```dax
Product Categories = DISTINCTCOUNT(ProductCategory[CategoryName])
```

**Warehouse Efficiency Measures** (click three dots (...) on **Warehouses** table → **New measure** for each):

```dax
Total Warehouses = COUNTROWS(Warehouses)
```
```dax
Total Warehouse Capacity = SUM(Warehouses[MaxCapacity])
```
```dax
Warehouse Utilization % = DIVIDE([Total Current Stock], [Total Warehouse Capacity], 0) * 100
```

---

## **Step 7: Save and Configure Access**

### 7.1 Save Your Model
- Your semantic model **auto-saves** in Fabric - no manual save needed
- The model is now available in your Fabric workspace

### 7.2 Set Refresh Schedule
- In your workspace, find your semantic model
- Click **...** → **Settings** → **Scheduled refresh** (Note: For this project we do not set refresh schedule)
- Configure to match your lakehouse data update schedule
- Since this is Direct Lake mode, refresh may not be needed

### 7.3 Grant Permissions
- Click **...** on your semantic model → **Manage permissions**
- Add users/groups who need to build reports
- Set appropriate permission levels (Read, Build, etc.)

---

## **Expected Results**

After completing this setup, you'll have:

**✅ Data Model Structure:**
- 11 tables from 3 business domains
- 13 properly configured relationships
- Date table for time intelligence
- Hidden technical fields for clean user experience

**✅ Business Measures:**
- 15+ KPIs covering inventory health, supply chain risk, product performance
- Organized in logical display folders
- Proper formatting (currency, percentage, etc.)

**✅ Ready for Analytics:**
- Connect Power BI Desktop or create Fabric reports
- Build dashboards for inventory management
- Analyze supply chain performance and risk
- Track product lifecycle and performance

---

## **Next Steps**

1. **Create Reports**: Build Power BI reports using this semantic model
2. **Add Time Intelligence**: Connect DateTable to transaction dates for trend analysis  
3. **Advanced Measures**: Add more complex calculations (inventory turnover, supplier scorecards)
4. **Row-Level Security**: Implement if users need filtered data access

**Troubleshooting**: If relationships don't work, verify that join fields have matching values and data types between tables.