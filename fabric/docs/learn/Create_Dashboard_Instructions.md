# Create Power BI Dashboard Using Semantic Model in Fabric

## Steps to Create Dashboard

### Using Fabric UI

1. Go to [app.fabric.microsoft.com](https://app.fabric.microsoft.com)
2. Navigate to your Fabric workspace
3. Find your semantic model: **"Supply Chain Analytics Model"**
4. Click on the semantic model name
5. Click **"Create report"** 
6. Add visuals from the **Data panel** on the right
7. Save report when finished: Click **File** → **Save**, Name it: "supply_dashboard"

## Sample Visuals

### 1. KPI Cards (Executive Overview)
**Card 1 - Total Products**
- Visual: Card
- Field: `Product[ProductID]` (shows count)

**Card 2 - Low Stock Alerts**  
- Visual: Card
- Field: `Inventory[InventoryID]`
- Filter: `Inventory[Status]` = "LowStock"

**Card 3 - Total Inventory Value**
- Visual: Card  
- Field: `Inventory[CurrentStock]` * `Product[ListPrice]` (create measure)

**Card 4 - Average Lead Time**
- Visual: Card
- Field: `Suppliers[LeadTimeDays]` (average)

### 2. Charts for Analysis

**Chart 1 - Inventory by Product Category**
- Visual: Stacked Column Chart
- X-axis: `Product[CategoryName]`  
- Y-axis: `Inventory[CurrentStock]` (sum)
- Legend: `Inventory[Status]`

**Chart 2 - Warehouse Stock Distribution** 
- Visual: Pie Chart
- Legend: `Inventory[WarehouseLocation]`
- Values: `Inventory[CurrentStock]` (sum)

**Chart 3 - Supplier Performance**
- Visual: Scatter Chart  
- X-axis: `Suppliers[LeadTimeDays]`
- Y-axis: `Suppliers[ReliabilityScore]`
- Size: Count of `ProductSuppliers[ProductID]`
- Legend: `Suppliers[SupplierType]`

**Chart 4 - Top 10 Products by Value**
- Visual: Horizontal Bar Chart
- Y-axis: `Product[ProductName]`  
- X-axis: `Product[ListPrice]` * `Inventory[CurrentStock]` (create measure)
- Filter: Top 10 by value

**Chart 5 - Inventory Status Overview**
- Visual: Donut Chart
- Legend: `Inventory[Status]` 
- Values: Count of `Inventory[InventoryID]`

### 3. Tables for Detailed Analysis

**Table 1 - Low Stock Report**
- Visual: Table
- Columns: 
  - `Product[ProductName]`
  - `Product[CategoryName]`  
  - `Inventory[CurrentStock]`
  - `Inventory[ReorderPoint]`
  - `Inventory[WarehouseLocation]`
- Filter: `Inventory[CurrentStock]` < `Inventory[ReorderPoint]`

**Table 2 - Supplier Directory**
- Visual: Table  
- Columns:
  - `Suppliers[SupplierName]`
  - `Suppliers[ProductCategory]`
  - `Suppliers[LeadTimeDays]`
  - `Suppliers[ReliabilityScore]`
  - `Suppliers[Location]`

**Table 3 - High-Value Products**
- Visual: Table
- Columns:
  - `Product[ProductName]`
  - `Product[ListPrice]`
  - `Product[StandardCost]`  
  - `Inventory[CurrentStock]`
- Filter: `Product[ListPrice]` > 200

### 4. Advanced Visuals

**Matrix 1 - Product Category vs Warehouse**
- Visual: Matrix
- Rows: `Product[CategoryName]`
- Columns: `Inventory[WarehouseLocation]`  
- Values: `Inventory[CurrentStock]` (sum)

**Gauge 1 - Inventory Health**
- Visual: Gauge
- Value: Count of `Inventory[Status]` = "Active" / Total Count
- Target: 90% (set as constant)

**Map 1 - Supplier Locations** 
- Visual: Map
- Location: `Suppliers[Location]`
- Size: Count of `ProductSuppliers[ProductID]`
- Color: `Suppliers[ReliabilityScore]` (average)

