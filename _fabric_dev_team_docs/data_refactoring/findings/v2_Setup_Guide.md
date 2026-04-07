# Fabric Setup Guide for V2 (Fixed Model)

> Follow these steps to deploy the **V2 fixed semantic model** to Microsoft Fabric.
> This mirrors the [original guide](https://github.com/DocGailZhou/solutionroot/blob/main/fabric/Guide_for_Manually_Setup_Fabric_Lakehouse.md) but uses the corrected CSVs and notebooks.

## Prerequisites

- Microsoft Fabric access with permission to create a workspace, lakehouse, and notebooks
- Git installed on your machine
- This repository available locally
- The `findings/v2/` folder from this repo

---

## Step 1. Create Fabric Workspace and Lakehouse

1. Create a new Fabric workspace.
2. In that workspace, create a Lakehouse. Example name: `miqdata`.
3. Open the lakehouse and make sure you can see the `Files` section.

---

## Step 2. Upload the V2 `data` Folder to the Lakehouse

1. From this repo, locate **`findings/v2/data`**.
2. In Fabric Lakehouse, go to `Files`.
3. Upload the full `data` folder.

After upload, your lakehouse path should look like:

```
Files/data/product/
    ├── Product.csv
    ├── ProductCategory.csv
    └── ProductLine.csv              ← NEW in V2

Files/data/inventory/
    ├── Warehouses.csv               ← WarehouseID now INT (1, 2, 3)
    ├── Inventory.csv                ← Denormalized columns removed
    ├── InventoryTransactions.csv    ← Negative StockAfter fixed
    ├── PurchaseOrders.csv           ← WarehouseID replaces DeliveryLocation
    ├── PurchaseOrderItems.csv       ← Denormalized columns removed
    └── DemandForecast.csv           ← WarehouseID added

Files/data/supplychain/
    ├── Suppliers.csv
    ├── ProductSuppliers.csv         ← Denormalized columns removed
    ├── SupplyChainEvents.csv        ← Split: event metadata only
    └── SupplyChainEventImpacts.csv  ← NEW: impacts with populated SupplierIDs
```

> **Note:** V2 focuses on the supply chain domain (product, inventory, supplychain schemas).
> If you also need customer, sales, and finance schemas, upload those from the original
> `fabric/infra/data/` folder alongside the V2 data.

---

## Step 3. Upload V2 Notebooks to Fabric

1. In your Fabric workspace, create a folder named `notebooks` with subfolders:
   - `schema`
   - `data_processing`

2. Upload **all notebooks** from `findings/v2/notebooks/`:

   | Notebook | Location | What It Does |
   |----------|----------|-------------|
   | **`run_pipeline.ipynb`** | `notebooks/` | **Orchestrator** — runs everything in the correct order |
   | `model_shared_dimensions.ipynb` | `notebooks/schema/` | Creates `shared.DimDate` + populates dynamically |
   | `model_product.ipynb` | `notebooks/schema/` | Creates ProductLine, ProductCategory, Product |
   | `model_supplychain.ipynb` | `notebooks/schema/` | Creates Suppliers, ProductSuppliers, Events, EventImpacts |
   | `model_inventory.ipynb` | `notebooks/schema/` | Creates Warehouses, Inventory, Txns, POs, Forecast |
   | `load_product.ipynb` | `notebooks/data_processing/` | Loads ProductLine → ProductCategory → Product |
   | `load_supplychain.ipynb` | `notebooks/data_processing/` | Loads Suppliers → ProductSuppliers → Events → Impacts |
   | `load_inventory.ipynb` | `notebooks/data_processing/` | Loads Warehouses → Inventory → Txns → POs → Forecast |

---

## Step 4. Attach Lakehouse and Run the Pipeline

1. Open **`run_pipeline.ipynb`** in Fabric.
2. Attach the lakehouse you created (e.g., `miqdata`) to the notebook session.
3. Click **Run All**.

That's it! The orchestrator runs all 7 notebooks in the correct FK dependency order:

```
Step 1/7  →  shared.DimDate (schema + auto-populate with dates through today + 6 months)
Step 2/7  →  product schema (ProductLine, ProductCategory, Product)
Step 3/7  →  supplychain schema (Suppliers, ProductSuppliers, Events, EventImpacts)
Step 4/7  →  inventory schema (Warehouses, Inventory, Txns, POs, Forecast)
Step 5/7  →  load product data
Step 6/7  →  load supplychain data
Step 7/7  →  load inventory data
   ↓
📊 Final validation — prints row counts for all 14 tables
```

> **Compared to V1** which also used a single `main_pipeline.ipynb`, V2's orchestrator
> adds validation (row counts, PK checks) and uses `MERGE INTO` so it's safe to re-run.

---

## Step 5. Expected Output and Validation

During a successful run, you should see messages similar to:

```text
✅ shared.DimDate populated: 3106 rows (2018-01-01 to 2026-10-02)
   Includes 6 months of future dates for prediction model

✅ product.ProductLine: 3 rows loaded
✅ product.ProductCategory: 30 rows loaded
✅ product.Product: 60 rows loaded

✅ supplychain.Suppliers: 5 rows loaded
✅ supplychain.ProductSuppliers: 75 rows loaded
✅ supplychain.SupplyChainEvents: 15 rows loaded
✅ supplychain.SupplyChainEventImpacts: 22 rows loaded

✅ inventory.Warehouses: 3 rows loaded
✅ inventory.Inventory: 81 rows loaded
✅ inventory.InventoryTransactions: 4545 rows loaded
✅ inventory.PurchaseOrders: 115 rows loaded
✅ inventory.PurchaseOrderItems: 350 rows loaded
✅ inventory.DemandForecast: 420 rows loaded
```

Final expected state:

| Schema | Tables | Total Rows |
|--------|--------|-----------|
| `shared` | 1 (DimDate) | ~3,106 |
| `product` | 3 (ProductLine, ProductCategory, Product) | 93 |
| `supplychain` | 4 (Suppliers, ProductSuppliers, Events, EventImpacts) | 117 |
| `inventory` | 6 (Warehouses, Inventory, InvTxns, POs, POItems, Forecast) | 5,514 |
| **Total** | **14 tables** | **~8,830 rows** |

---

## Step 6. Generate Ontology

Once all tables are loaded and validated:

1. Go to your Fabric workspace
2. Open the ontology tool and point it at your lakehouse
3. The PK/FK constraints defined in schema notebooks will enable **auto-discovery** of:
   - Entity types (one per table)
   - Relationships (from FK constraints)
   - Hierarchies (ProductLine → ProductCategory → Product)
   - Time intelligence (via DimDate joins)

---

## Key Differences from Original Guide

| Aspect | Original (V1) | This Guide (V2) |
|--------|--------------|-----------------|
| **How to run** | Run `main_pipeline.ipynb` | Run `run_pipeline.ipynb` (same single-notebook experience) |
| Tables | 22 across 6 schemas | 14 supply chain tables + DimDate |
| Constraints | Zero PK/FK | All tables have PK + FK constraints |
| Warehouse IDs | String (WH_100, WH_200) | Integer (1, 2, 3) |
| Load strategy | `mode("overwrite")` | `MERGE INTO` (upsert, safe re-run) |
| Validation | None | Null PK checks, dedup checks, row count checks |
| Date dimension | Missing | Dynamic DimDate (2018 → today + 6 months) |
| Denormalization | ProductName/Category in 8 tables | Removed — use JOINs |
| SupplyChainEvents | Overloaded (event + impact mixed) | Split into Events + EventImpacts |
| Event SupplierIDs | 100% NULL | All populated |

---

## Common Issues

| Issue | Solution |
|-------|---------|
| `Path not found` errors | Confirm `Files/data/product`, `Files/data/inventory`, `Files/data/supplychain` folder structure |
| `MERGE INTO` fails | Run schema notebooks first to create tables before loading |
| FK constraint errors | Run notebooks in the exact order shown in Step 4 |
| DimDate needs more future dates | Re-run `model_shared_dimensions.ipynb` — it dynamically extends to today + 6 months |
| Need customer/sales/finance data | Upload from original `fabric/infra/data/` and use original notebooks for those schemas |

---

## Re-running / Updating Data

The V2 notebooks use `MERGE INTO` (upsert), so re-running is safe:
- Existing rows are updated
- New rows are inserted
- No data is destroyed

To regenerate DimDate with an extended prediction window, simply re-run `model_shared_dimensions.ipynb`.
