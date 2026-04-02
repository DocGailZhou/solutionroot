# What Changed in Each Table (V1 → V2)

> **Why we made changes:** The original sample data had issues that prevented Microsoft Fabric from correctly building the ontology (the knowledge graph that powers the Data Agent). Below is a simple table-by-table breakdown of what was changed and why.

---

## 1. Product

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Added `ProductLineID` column | ❌ Not present | ✅ Links to ProductLine table | Product needs to know which line it belongs to (Camping, Kitchen, Ski) |
| Removed `IsoCurrencyCode` | Had "USD" in every row | ❌ Removed | Same value in every row adds no useful information |
| Removed `CategoryName` | Category name was copied here | ❌ Removed | This info already lives in ProductCategory table — duplicating it causes confusion |
| Fixed date formats | Inconsistent date strings | ✅ Proper DATE format | Ontology needs consistent date formats to work |

---

## 2. ProductCategory

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Renamed `CategoryID` → `ProductCategoryID` | CategoryID | ProductCategoryID | Naming must follow the pattern `{TableName}ID` so Fabric can auto-detect relationships |
| Added `ProductLineID` column | ❌ Not present | ✅ Links to ProductLine table | Creates the hierarchy: ProductLine → Category → Product |
| Removed `ParentCategoryID` | Had a self-referencing ID | ❌ Removed | Replaced by the cleaner ProductLineID hierarchy |
| Removed `BrandName`, `BrandLogoUrl` | Present but unused | ❌ Removed | Not relevant to supply chain ontology |

---

## 3. ProductLine ⭐ NEW TABLE

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Created new table | ❌ Did not exist | ✅ 3 rows: Camping, Kitchen, Ski | Needed as a top-level dimension for product hierarchy |

---

## 4. Warehouses

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Changed `WarehouseID` from text to number | "WH_100", "WH_200", "WH_500" | 1, 2, 3 | Text IDs create weak joins — numbers are more reliable for relationships |
| Renamed `Priority` → `WarehousePriority` | Column called "Priority" (numeric: 0.1, 0.2, 0.7) | `WarehousePriority` | PurchaseOrders also had a "Priority" column but as text ("High", "Low"). Same name + different types = ontology error |
| Added measures in semantic model | No measures | `Total Warehouses`, `Total Capacity` | Ontology generator skips tables that have no measurable data |

---

## 5. Inventory

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Changed `WarehouseID` from text to number | "WH_100" etc. | 1, 2, 3 | Must match the Warehouses table format |
| Removed `WarehouseLocation` | Had warehouse name as text | ❌ Removed | This info lives in the Warehouses table — look it up via WarehouseID |
| Removed `ProductName`, `ProductCategory` | Product details were copied here | ❌ Removed | This info lives in the Product table — duplicating causes ontology confusion |
| Removed `AvailableStock` | Was a calculated field | ❌ Removed | Can be derived from other columns — stored calculations cause data conflicts |

---

## 6. InventoryTransactions

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Changed `WarehouseID` from text to number | "WH_100" etc. | 1, 2, 3 | Must match the Warehouses table format |
| Fixed 404 negative `StockAfter` values | Had values like -15, -32 | ✅ Minimum is now 0 | Stock cannot be negative — bad data leads to wrong query results |

---

## 7. PurchaseOrders

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Renamed `Priority` → `OrderPriority` | Column called "Priority" (text: "High", "Medium", "Low") | `OrderPriority` | Conflicted with Warehouses numeric "Priority" — same name, different type breaks ontology |
| Changed `DeliveryLocation` → `WarehouseID` (number) | Had warehouse name as text | ✅ Integer WarehouseID | Creates a proper relationship to the Warehouses table |
| Removed `SupplierName` | Supplier name was copied here | ❌ Removed | This info lives in the Suppliers table |

---

## 8. PurchaseOrderItems

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Removed `PurchaseOrderNumber` | Order number was copied here | ❌ Removed | Already in PurchaseOrders table — look it up via PurchaseOrderID |
| Removed `ProductName`, `ProductCategory` | Product details were copied here | ❌ Removed | Already in Product table |

---

## 9. DemandForecast

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Added `WarehouseID` column | ❌ Not present | ✅ Links to Warehouses table | Forecasts need to be tied to a specific warehouse |
| Removed denormalized columns | Had product/category names copied in | ❌ Removed | Already in dimension tables |

---

## 10. Suppliers

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Fixed `PrimarySupplierID` data type | Was "3.0" (decimal text) | ✅ "3" (clean integer) | Decimal formatting causes type mismatch issues |
| No other changes | — | — | Table was already well-structured |

---

## 11. ProductSuppliers (Bridge Table)

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Removed denormalized columns | Had product/supplier names copied in | ❌ Removed | This table only needs the two IDs (ProductID + SupplierID) to link Product ↔ Supplier |

---

## 12. SupplyChainEvents

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Split into two tables | One big table with event info AND supplier impact info mixed together | ✅ Now just event metadata | A single table was trying to do two jobs — describe the event AND track its impact on each supplier |

---

## 13. SupplyChainEventImpacts ⭐ NEW TABLE

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Created new table | ❌ Did not exist | ✅ 22 rows tracking per-supplier impact | Each row = one event's impact on one supplier. Links to both Events and Suppliers tables |
| Populated `SupplierID` | Was NULL in V1 event rows | ✅ Properly assigned | Without SupplierID, the ontology cannot connect events to suppliers |

---

## 14. DimDate ⭐ NEW TABLE

| What Changed | Before (V1) | After (V2) | Why |
|---|---|---|---|
| Created new table | ❌ Did not exist | ✅ ~3,100 rows (2018 to 6 months ahead) | A shared date dimension is essential for any time-based questions ("last month", "this quarter") |

---

## Simple Summary

| Category | Count |
|---|---|
| Tables in V1 | 11 |
| Tables in V2 | 14 (3 new tables added) |
| Columns removed (duplicates) | 18 |
| Columns renamed | 3 |
| Columns added | 4 |
| Data fixes (bad values) | 404 rows corrected |
| Ontology issues resolved | Product missing ✅, Warehouses missing ✅, Priority conflict ✅ |

---

## The 3 Golden Rules for Ontology-Ready Data

1. **One fact, one place** — Don't copy ProductName into every table. Let the ontology follow the relationships to find it.

2. **Same name = same type** — If two tables have a column called "Priority", they must be the same data type. Otherwise, rename them.

3. **Every table needs something to count** — Pure lookup tables (like Warehouses) need at least one measure (like Total Capacity) or the ontology generator may skip them.

---

*Prepared for Supply Chain Ontology project — V1 to V2 data remediation.*
