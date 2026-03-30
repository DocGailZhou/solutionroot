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
DateTable = CALENDAR(
    DATE(2022, 1, 1),
    DATE(2026, 12, 31)
)
```
- Right-click the new DateTable → **Mark as date table**
- Connect DateTable to transaction date fields if needed

### 4.2 Set Data Types and Formats
**Currency Fields:**
- Select `product_Product.ListPrice`, `product_Product.StandardCost` 
- Set **Format** = `Currency ($)` and **Decimal places** = `2`
- Select `inventory_Inventory.AverageCost`, `supplychain_ProductSuppliers.WholesaleCost`
- Set **Format** = `Currency ($)` and **Decimal places** = `2`

**Percentage Fields:**
- Select `supplychain_Suppliers.ReliabilityScore`
- Set **Format** = `Percentage` and **Decimal places** = `1`

### 4.3 Hide Technical Fields
Hide ID/GUID fields from report view:
- Select each ID column: `ProductID`, `WarehouseID`, `SupplierID`, `PurchaseOrderID`
- Right-click → **Hide in report view**

---

## **Step 5: Create Core Business Measures**

### 5.1 Add Key Performance Measures
Right-click any table in the Fields pane → **New measure**, then enter:

**Inventory Health Measures:**
```dax
Total Current Stock = SUM(inventory_Inventory[CurrentStock])
Total Available Stock = SUM(inventory_Inventory[AvailableStock])
Total Reserved Stock = SUM(inventory_Inventory[ReservedStock])
Stock Fill Rate % = DIVIDE([Total Available Stock], [Total Current Stock], 0) * 100
Low Stock Items = COUNTROWS(FILTER(inventory_Inventory, inventory_Inventory[CurrentStock] < inventory_Inventory[ReorderPoint]))
```

**Supply Chain Measures:**
```dax
Active Suppliers = COUNTROWS(FILTER(supplychain_Suppliers, supplychain_Suppliers[Status] = "Active"))
Average Reliability Score = AVERAGE(supplychain_Suppliers[ReliabilityScore])
Active Disruptions = COUNTROWS(FILTER(supplychain_SupplyChainEvents, supplychain_SupplyChainEvents[Status] = "Active"))
Average Lead Time Days = AVERAGE(supplychain_ProductSuppliers[LeadTimeDays])
```

**Product Performance Measures:**
```dax
Total Products = COUNTROWS(product_Product)
Active Products = COUNTROWS(FILTER(product_Product, product_Product[ProductStatus] = "active"))
Average Product Cost = AVERAGE(product_Product[StandardCost])
Product Categories = DISTINCTCOUNT(product_ProductCategory[CategoryName])
```

**Warehouse Efficiency Measures:**
```dax
Total Warehouses = COUNTROWS(inventory_Warehouses)
Total Warehouse Capacity = SUM(inventory_Warehouses[MaxCapacity])
Warehouse Utilization % = DIVIDE([Total Current Stock], [Total Warehouse Capacity], 0) * 100
```

---

## **Step 6: Organize and Validate Model**

### 6.1 Create Display Folders
Organize measures into logical groups:
- Select inventory measures → Properties → **Display folder** = `"Inventory Analytics"`
- Select supply chain measures → **Display folder** = `"Supply Chain Analytics"`
- Select product measures → **Display folder** = `"Product Analytics"`
- Select warehouse measures → **Display folder** = `"Warehouse Analytics"`

### 6.2 Test the Model
Create a validation report to test relationships:
- Add a **Matrix** visual
- **Rows**: `product_ProductCategory[CategoryName]`
- **Values**: `[Total Current Stock]`, `[Active Suppliers]`
- Verify data appears and makes business sense

### 6.3 Validate Relationships
In **Model** view, check that:
- All relationship lines show `1` on one side and `*` on the other
- No relationships are dashed (inactive)
- All tables are connected to the model (no orphaned tables)

---

## **Step 7: Save and Configure Access**

### 7.1 Save Your Model
- Click **File** → **Save** to save your semantic model
- The model is now available in your Fabric workspace

### 7.2 Set Refresh Schedule
- In your workspace, find your semantic model
- Click **...** → **Settings** → **Scheduled refresh**
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