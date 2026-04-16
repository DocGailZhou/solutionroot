# Setting Up Table Relationships in Microsoft Fabric Semantic Model

> This guide walks through exactly how to set up the table relationships for the  
> Fabric IQ Supply Chain semantic model in the Microsoft Fabric web interface.

> **📅 Updated April 2026**: Expanded to include complete data model with Sales, Finance, Customer, and shared Date dimension relationships. Total relationships: 33 (DimDate connected across all schemas for unified time intelligence).

---

## What Are Table Relationships and Why Do They Matter?

A relationship tells the semantic model **how two tables are connected**. Without relationships, tables are isolated — you cannot slice inventory data by product category, or filter purchase orders by warehouse, because the model does not know they are related.

Think of relationships like this:  
- The **Product** table has one row per product  
- The **Inventory** table has many rows — one per product per warehouse  
- The relationship says: "for each product in Product, there can be many rows in Inventory"  
- This is called a **One-to-Many** relationship (written as `1 → *`)

When a user filters by "Camping" in a report, the relationship automatically applies that filter to Inventory, PurchaseOrderItems, DemandForecast, etc.

---

## Key Relationship Concepts Before You Start

### Cardinality (the "type" of relationship)

| Type | Meaning | Example |
|---|---|---|
| **One-to-Many** (1:*) | One row on the left matches many rows on the right | One Product → many Inventory rows |
| **Many-to-One** (*:1) | Same as above, just described from the other direction | Many Inventory rows → one Product |
| **One-to-One** (1:1) | Each row on the left matches exactly one on the right | Rare — usually means tables should be merged |
| **Many-to-Many** (*:*) | Avoid unless necessary — can cause confusing results | Not used in this model |

### Cross-filter Direction

| Setting | Meaning | When to use |
|---|---|---|
| **Single** | Filters flow one way only (from the "one" side to the "many" side) | Default — use for almost everything |
| **Both** | Filters flow in both directions | Only when you specifically need it — can cause performance issues |

**Rule of thumb for this model**: Use **Single** direction for all relationships. The filter always flows from the dimension/reference table (Product, Warehouses, Suppliers) **into** the fact/transaction table (Inventory, InventoryTransactions, PurchaseOrders).

---

## How to Navigate to the Semantic Model in Fabric

1. Go to your **Microsoft Fabric workspace** at [app.fabric.microsoft.com](https://app.fabric.microsoft.com)
2. In the workspace, find your **Semantic Model** item (it has a cube/dataset icon)
3. Click on it to open it
4. In the top menu, click **"Open data model"** — this opens the Model view where you manage relationships

You will see a canvas with all your tables displayed as boxes. If tables are stacked on top of each other, drag them apart to arrange them clearly.

---

## Recommended Canvas Layout

Before creating relationships, arrange your tables in this layout to make the diagram readable:

```
[Top row — Dimension/Reference tables]
  ProductCategory    Product    Warehouses    Suppliers

[Middle row — Bridge/Mapping tables]
  ProductSuppliers    SupplyChainEvents

[Bottom row — Fact/Transaction tables]
  Inventory    InventoryTransactions    PurchaseOrders    PurchaseOrderItems    DemandForecast
```

This layout visually shows that filters flow **downward** from reference tables into transactional tables.

---

## How to Create a Relationship — Step by Step

There are two ways to create a relationship in Fabric:

### Method A — Drag and Drop (Easiest)

1. On the canvas, find the **source table** (the "one" side — e.g., `Product`)
2. Click and hold the **field you want to join on** (e.g., `ProductID`)
3. Drag it onto the **destination table** (the "many" side — e.g., `Inventory`)
4. Drop it on the matching field (e.g., `ProductID`)
5. A line appears between the tables — the relationship is created
6. Verify the settings in the panel that appears (see "Verify Your Settings" below)

### Method B — Manual Dialog (More Control)

1. In the top menu, click **"Manage relationships"**
2. Click **"New relationship"**
3. In the dialog:
   - **From table**: select the "one" side table (e.g., `product_Product`)
   - **From column**: select the join field (e.g., `ProductID`)
   - **To table**: select the "many" side table (e.g., `inventory_Inventory`)
   - **To column**: select the matching field (e.g., `ProductID`)
   - **Cardinality**: select `One to many (1:*)`
   - **Cross filter direction**: select `Single`
   - **Make this relationship active**: check this box ✅
4. Click **Confirm**

### Verify Your Settings

After creating each relationship, click on the line between tables to verify:
- The `1` symbol appears on the Product/Warehouse/Supplier side
- The `*` symbol appears on the Inventory/Transaction side
- The arrow points from `1` toward `*`

---

## All Relationships to Create

Work through this list one relationship at a time. The **From** column is always the "one" side (the reference/dimension table).

### Group 1: Core Dimension Relationships

| # | Relationship Name | From Table | From Field | To Table | To Field | Cardinality | Direction |
|---|---|---|---|---|---|---|---|
| 1 | Product_ProductCategory | `product_ProductCategory` | `CategoryID` | `product_Product` | `ProductCategoryID` | One to Many | Single |
| 2 | ProductLine_Product | `product_ProductLine` | `ProductLineID` | `product_Product` | `ProductLineID` | One to Many | Single |

### Group 2: Customer → Sales Domain

| # | Relationship Name | From Table | From Field | To Table | To Field | Cardinality | Direction |
|---|---|---|---|---|---|---|---|
| 3 | Customer_Order | `customer_Customer` | `CustomerID` | `sales_Order` | `CustomerID` | One to Many | Single |
| 4 | Customer_CustomerAccount | `customer_Customer` | `CustomerID` | `customer_CustomerAccount` | `CustomerID` | One to Many | Single |
| 5 | CustomerAccount_Order | `customer_CustomerAccount` | `CustomerAccountID` | `sales_Order` | `CustomerAccountID` | One to Many | Single |
| 6 | Customer_Location | `customer_Customer` | `CustomerID` | `customer_Location` | `CustomerID` | One to Many | Single |
| 7 | CustomerRelationshipType_Customer | `customer_CustomerRelationshipType` | `CustomerRelationshipTypeID` | `customer_Customer` | `CustomerRelationshipTypeID` | One to Many | Single |

### Group 3: Product → Sales Domain

| # | Relationship Name | From Table | From Field | To Table | To Field | Cardinality | Direction |
|---|---|---|---|---|---|---|---|
| 8 | Product_OrderLine | `product_Product` | `ProductID` | `sales_OrderLine` | `ProductID` | One to Many | Single |
| 9 | Order_OrderLine | `sales_Order` | `OrderID` | `sales_OrderLine` | `OrderID` | One to Many | Single |
| 10 | Order_OrderPayment | `sales_Order` | `OrderID` | `sales_OrderPayment` | `OrderID` | One to Many | Single |

### Group 4: Sales → Finance Domain

| # | Relationship Name | From Table | From Field | To Table | To Field | Cardinality | Direction |
|---|---|---|---|---|---|---|---|
| 11 | Customer_Invoice | `customer_Customer` | `CustomerID` | `finance_invoice` | `CustomerID` | One to Many | Single |
| 12 | Order_Invoice | `sales_Order` | `OrderID` | `finance_invoice` | `OrderID` | One to Many | Single |
| 13 | Invoice_Payment | `finance_invoice` | `InvoiceID` | `finance_payment` | `InvoiceID` | One to Many | Single |
| 14 | CustomerAccount_Account | `customer_CustomerAccount` | `CustomerAccountID` | `finance_account` | `CustomerAccountID` | One to Many | Single |

### Group 5: Product → Inventory Domain

| # | Relationship Name | From Table | From Field | To Table | To Field | Cardinality | Direction |
|---|---|---|---|---|---|---|---|
| 15 | Product_Inventory | `product_Product` | `ProductID` | `inventory_Inventory` | `ProductID` | One to Many | Single |
| 16 | Product_InventoryTransactions | `product_Product` | `ProductID` | `inventory_InventoryTransactions` | `ProductID` | One to Many | Single |
| 17 | Product_PurchaseOrderItems | `product_Product` | `ProductID` | `inventory_PurchaseOrderItems` | `ProductID` | One to Many | Single |
| 18 | Product_DemandForecast | `product_Product` | `ProductID` | `inventory_DemandForecast` | `ProductID` | One to Many | Single |

---

### Group 6: Warehouses → Inventory Domain

| # | Relationship Name | From Table | From Field | To Table | To Field | Cardinality | Direction |
|---|---|---|---|---|---|---|---|
| 19 | Warehouses_Inventory | `inventory_Warehouses` | `WarehouseID` | `inventory_Inventory` | `WarehouseLocation` | One to Many | Single |
| 20 | Warehouses_InventoryTransactions | `inventory_Warehouses` | `WarehouseID` | `inventory_InventoryTransactions` | `WarehouseLocation` | One to Many | Single |
| 21 | Warehouses_PurchaseOrders | `inventory_Warehouses` | `WarehouseID` | `inventory_PurchaseOrders` | `DeliveryLocation` | One to Many | Single |

> **Note**: `WarehouseID` values in your data are `Main`, `Backup`, `Regional`. The `WarehouseLocation` and `DeliveryLocation` fields in the other tables use these same values as foreign keys.

---

### Group 7: Purchase Orders → Line Items

| # | Relationship Name | From Table | From Field | To Table | To Field | Cardinality | Direction |
|---|---|---|---|---|---|---|---|
| 22 | PurchaseOrders_PurchaseOrderItems | `inventory_PurchaseOrders` | `PurchaseOrderID` | `inventory_PurchaseOrderItems` | `PurchaseOrderID` | One to Many | Single |

---

### Group 8: Suppliers → Supply Chain Domain

| # | Relationship Name | From Table | From Field | To Table | To Field | Cardinality | Direction |
|---|---|---|---|---|---|---|---|
| 23 | Suppliers_PurchaseOrders | `supplychain_Suppliers` | `SupplierID` | `inventory_PurchaseOrders` | `SupplierID` | One to Many | Single |
| 24 | Suppliers_ProductSuppliers | `supplychain_Suppliers` | `SupplierID` | `supplychain_ProductSuppliers` | `SupplierID` | One to Many | Single |
| 25 | Suppliers_SupplyChainEvents | `supplychain_Suppliers` | `SupplierID` | `supplychain_SupplyChainEvents` | `SupplierID` | One to Many | Single |

> **Note**: `SupplyChainEvents.SupplierID` can be NULL (for general/market-wide events). This is fine — the relationship still works. NULL rows simply won't match any supplier and will appear as "blank" in reports.

---

### Group 9: Product → Supply Chain Domain

| # | Relationship Name | From Table | From Field | To Table | To Field | Cardinality | Direction |
|---|---|---|---|---|---|---|---|
| 26 | Product_ProductSuppliers | `product_Product` | `ProductID` | `supplychain_ProductSuppliers` | `ProductID` | One to Many | Single |

---

### Group 10: Date Dimension Relationships (Shared Across All Schemas)

| # | Relationship Name | From Table | From Field | To Table | To Field | Cardinality | Direction |
|---|---|---|---|---|---|---|---|
| 27 | DimDate_Order | `shared_DimDate` | `FullDate` | `sales_Order` | `OrderDate` | One to Many | Single |
| 28 | DimDate_Invoice | `shared_DimDate` | `FullDate` | `finance_invoice` | `InvoiceDate` | One to Many | Single |
| 29 | DimDate_InvoiceDueDate | `shared_DimDate` | `FullDate` | `finance_invoice` | `DueDate` | One to Many | Single |
| 30 | DimDate_CustomerEstablished | `shared_DimDate` | `FullDate` | `customer_Customer` | `CustomerEstablishedDate` | One to Many | Single |
| 31 | DimDate_InventoryTransactions | `shared_DimDate` | `FullDate` | `inventory_InventoryTransactions` | `TransactionDate` | One to Many | Single |
| 32 | DimDate_PurchaseOrders | `shared_DimDate` | `FullDate` | `inventory_PurchaseOrders` | `OrderDate` | One to Many | Single |
| 33 | DimDate_SupplyChainEvents | `shared_DimDate` | `FullDate` | `supplychain_SupplyChainEvents` | `EventDate` | One to Many | Single |

> **Note**: The shared.DimDate table serves as the central calendar dimension across ALL schemas, enabling consistent time-based analysis for sales, finance, customer, inventory, and supply chain operations. This ensures unified time intelligence reporting across the entire business model.

---

## Complete Relationship Diagram

After all 33 relationships are created, your model diagram should look like this:

```
                    shared.DimDate (Calendar) ←── SHARED ACROSS ALL SCHEMAS
                     │  │  │  │  │  │  │
                     │  │  │  │  │  │  └──→ SupplyChainEvents
                     │  │  │  │  │  └─────→ PurchaseOrders
                     │  │  │  │  └────────→ InventoryTransactions
                     │  │  │  └───────────→ Customer (EstablishedDate)
                     │  │  └──────────────→ Invoice (DueDate)
                     │  └─────────────────→ Invoice (InvoiceDate)
                     └────────────────────→ Order (OrderDate)
                                             │
Customer ←─ CustomerRelationshipType        ├──→ OrderLine ──→ Product ──→ ProductCategory
    │                                       │        │         │
    ├──→ CustomerAccount ──→ Order ─────────┘        │         └──→ ProductLine
    │        │                                       │         │
    └──→ Location                                    │         ├──→ Inventory ←── Warehouses
             │                                       │         │         │
Customer ────┴──→ Invoice ←─── Order                 │         ├──→ InventoryTransactions
    │              │                                 │         │
    └──→ Account   └──→ Payment                     │         ├──→ PurchaseOrderItems
                                                     │         │
                   Order ──→ OrderPayment           │         ├──→ DemandForecast
                                                     │         │
                                                     └──→ ProductSuppliers ←── Suppliers
                                                                   │               │
                                                                   │               ├──→ SupplyChainEvents
                                                                   │               │
                                                                   │               └──→ PurchaseOrders ──→ PurchaseOrderItems
                                                                   │
                                                                   └─── Warehouses
```

### Key Data Flow Patterns:
1. **Customer Journey**: Customer → Order → OrderLine → Product
2. **Financial Flow**: Order → Invoice → Payment
3. **Inventory Flow**: Product → Inventory → InventoryTransactions (with date tracking)
4. **Supply Chain Flow**: Supplier → PurchaseOrders → PurchaseOrderItems → Product
5. **Time Intelligence**: DimDate connects to ALL domains (Sales, Finance, Customer, Inventory, Supply Chain) for comprehensive cross-domain temporal analysis

---

## How to Check Your Relationships for Problems

### Check 1: Look for missing relationship lines
On the canvas, every table should have at least one line connecting it to another table. If any table is floating with no connections, it is isolated and will not filter correctly.

### Check 2: Verify the 1 and * symbols
Click on each relationship line. Confirm:
- `1` is on the dimension/reference side (Product, Warehouses, Suppliers, ProductCategory)
- `*` is on the fact/transaction side (Inventory, InventoryTransactions, PurchaseOrders, etc.)

If you see `*` on both sides, the relationship is Many-to-Many — this usually means the join field has duplicate values on the "one" side. Check that `ProductID` in `Product` is unique (no duplicate rows).

### Check 3: Check for inactive relationships
An **inactive relationship** appears as a **dashed line** instead of a solid line. Inactive relationships are not used by default. If you see a dashed line, click it and check the "Make this relationship active" setting.

### Check 4: Run a quick test in a report
Create a simple Matrix visual to test different domains:

**Test 1 - Sales Analysis:**
- Rows: `CustomerRelationshipTypeName` from `customer_CustomerRelationshipType`
- Columns: `ProductLineName` from `product_ProductLine`
- Values: `OrderTotal` from `sales_Order`

**Test 2 - Inventory Analysis:**
- Rows: `ProductCategory` from `product_ProductCategory`
- Values: `CurrentStock` from `inventory_Inventory`

**Test 3 - Cross-Domain Time Analysis:**
- Rows: `MonthName` from `shared_DimDate`
- Columns: Domain (manually group measures)
- Values: `OrderTotal` from `sales_Order`, `TotalAmount` from `finance_invoice`, `TransactionCount` from `inventory_InventoryTransactions`

**Test 4 - Supply Chain Timeline:**
- Rows: `QuarterName` from `shared_DimDate` 
- Values: `EventCount` from `supplychain_SupplyChainEvents`, `PurchaseOrderCount` from `inventory_PurchaseOrders`

If the relationships are working correctly:
- Test 1 should show sales totals broken down by customer type and product line
- Test 2 should show stock totals by Camping, Kitchen, and Ski categories
- Test 3 should show time-based trends across sales, finance, and inventory domains side-by-side
- Test 4 should show supply chain activity patterns over time

If all values appear in a single "blank" row, the related relationships are not working correctly.

---

## Troubleshooting Common Problems

### Problem: "A relationship already exists between these tables"
**Cause**: You already created this relationship, or Fabric auto-detected it.  
**Fix**: Click "Manage relationships" to review existing relationships and avoid duplicates.

### Problem: The `*` symbol appears on the wrong side
**Cause**: The field you chose as the "one" side has duplicate values (not truly unique).  
**Fix**: Check that `ProductID` in `product_Product` has no duplicate rows. Run this in the lakehouse SQL endpoint:
```sql
SELECT ProductID, COUNT(*) AS cnt
FROM product.Product
GROUP BY ProductID
HAVING COUNT(*) > 1
```
If any rows are returned, there are duplicates that need to be resolved.

### Problem: Warehouse relationship not working (`WarehouseID` → `WarehouseLocation`)
**Cause**: The values may not match exactly — e.g., `"Main"` vs `"main"` (case difference) or trailing spaces.  
**Fix**: Check the actual values with:
```sql
SELECT DISTINCT WarehouseID FROM inventory.Warehouses
SELECT DISTINCT WarehouseLocation FROM inventory.Inventory
```
Both should return exactly: `Main`, `Backup`, `Regional`.

### Problem: SupplierID relationship shows many blank rows
**Cause**: `SupplyChainEvents.SupplierID` is NULL for general events (expected behavior).  
**Fix**: This is normal. In reports, use a filter to exclude blank suppliers when you only want supplier-specific events.

### Problem: Relationship line is dashed (inactive)
**Cause**: Fabric allows only one active relationship between two tables. If you accidentally created two relationships between the same tables, the second one becomes inactive.  
**Fix**: Go to "Manage relationships", find the duplicate, and delete it.

---

## After All Relationships Are Set

Once all 33 relationships are in place:

1. **Save the model** — click Save in the top right
2. **Proceed to Step 2** of the semantic model guide: building your core measures
3. Reference file: [supplychain_semantic_model_extra.md](supplychain_semantic_model_extra.md)

---

## Quick Reference Checklist

Use this checklist to confirm all relationships are created:

**Core Dimensions (2 relationships):**
- [ ] ProductCategory → Product (CategoryID → ProductCategoryID)
- [ ] ProductLine → Product (ProductLineID → ProductLineID)

**Customer Domain (5 relationships):**
- [ ] Customer → Order (CustomerID → CustomerID)  
- [ ] Customer → CustomerAccount (CustomerID → CustomerID)
- [ ] CustomerAccount → Order (CustomerAccountID → CustomerAccountID)
- [ ] Customer → Location (CustomerID → CustomerID)
- [ ] CustomerRelationshipType → Customer (CustomerRelationshipTypeID → CustomerRelationshipTypeID)

**Sales Domain (3 relationships):**
- [ ] Product → OrderLine (ProductID → ProductID)
- [ ] Order → OrderLine (OrderID → OrderID)
- [ ] Order → OrderPayment (OrderID → OrderID)

**Finance Domain (4 relationships):**
- [ ] Customer → Invoice (CustomerID → CustomerID)
- [ ] Order → Invoice (OrderID → OrderID)
- [ ] Invoice → Payment (InvoiceID → InvoiceID)
- [ ] CustomerAccount → Account (CustomerAccountID → CustomerAccountID)

**Inventory Domain (4 relationships):**
- [ ] Product → Inventory (ProductID → ProductID)
- [ ] Product → InventoryTransactions (ProductID → ProductID)
- [ ] Product → PurchaseOrderItems (ProductID → ProductID)
- [ ] Product → DemandForecast (ProductID → ProductID)

**Warehouse Domain (3 relationships):**
- [ ] Warehouses → Inventory (WarehouseID → WarehouseLocation)
- [ ] Warehouses → InventoryTransactions (WarehouseID → WarehouseLocation)
- [ ] Warehouses → PurchaseOrders (WarehouseID → DeliveryLocation)

**Purchase Order Domain (1 relationship):**
- [ ] PurchaseOrders → PurchaseOrderItems (PurchaseOrderID → PurchaseOrderID)

**Supply Chain Domain (3 relationships):**
- [ ] Suppliers → PurchaseOrders (SupplierID → SupplierID)
- [ ] Suppliers → ProductSuppliers (SupplierID → SupplierID)
- [ ] Suppliers → SupplyChainEvents (SupplierID → SupplierID)

**Product-Supply Chain (1 relationship):**
- [ ] Product → ProductSuppliers (ProductID → ProductID)

**Date Dimension (7 relationships):**
- [ ] DimDate → Order (FullDate → OrderDate)
- [ ] DimDate → Invoice (FullDate → InvoiceDate)
- [ ] DimDate → Invoice (FullDate → DueDate)
- [ ] DimDate → Customer (FullDate → CustomerEstablishedDate)
- [ ] DimDate → InventoryTransactions (FullDate → TransactionDate)
- [ ] DimDate → PurchaseOrders (FullDate → OrderDate)
- [ ] DimDate → SupplyChainEvents (FullDate → EventDate)

**Total: 33 relationships, all One-to-Many, Single direction**
