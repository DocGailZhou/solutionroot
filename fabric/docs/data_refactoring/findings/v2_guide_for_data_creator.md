# What I Fixed in the Sample Data & How You Can Use Copilot to Do It

---

## Hi! Here's a Simple Summary

I reviewed the sample data you created for the Supply Chain ontology in Fabric. The data was good — the tables, columns, and relationships were all there. But there were a few small structural issues that were causing problems when Fabric tried to generate the ontology.

I fixed everything, and below I explain:
1. What the issues were (simple explanation)
2. What I changed
3. A ready-to-use Copilot prompt you can use to check and fix any future dataset

---

## The 5 Main Issues I Found

### Issue 1: Same Column Name, Different Data Type

**What happened:**
Two tables both had a column called `Priority`:
- In **Warehouses** → it was a number (0.1, 0.2, 0.7)
- In **PurchaseOrders** → it was text ("High", "Medium", "Low")

**Why it's a problem:**
Fabric's ontology looks at column names across all tables. When it sees "Priority" in two places with different types, it gets confused and shows an error.

**What I did:**
- Warehouses: renamed to `WarehousePriority`
- PurchaseOrders: renamed to `OrderPriority`

**Rule:** If two tables have a column with the same name, they must have the same data type. Otherwise, give them different names.

---

### Issue 2: Product and Warehouse Names Were Copied Into Many Tables

**What happened:**
Columns like `ProductName`, `SupplierName`, `CategoryName` appeared in fact tables like PurchaseOrderItems, Inventory, and DemandForecast.

**Why it's a problem:**
The ontology sees these as separate properties in each table. It doesn't know that `ProductName` in PurchaseOrderItems is the same as `ProductName` in Product. This causes duplicate entities and broken navigation.

**What I did:**
Removed 18 copied columns from fact tables. Now each table only has the ID column (like `ProductID`), and the ontology follows the relationship to get the name from the Product table.

**Rule:** A column like `ProductName` should exist in only one place — the Product table. Other tables should only have `ProductID`.

---

### Issue 3: WarehouseID Was Text Instead of Number

**What happened:**
WarehouseID was "WH_100", "WH_200", "WH_500" (text strings).

**Why it's a problem:**
Text-based IDs create weak joins. The ontology works better with integer IDs because it can match them reliably across tables.

**What I did:**
Changed to simple numbers: 1, 2, 3. Updated all tables that reference WarehouseID.

**Rule:** Use integer IDs (1, 2, 3) not coded strings ("WH_100"). It's simpler and more reliable.

---

### Issue 4: Missing Tables That the Ontology Needed

**What happened:**
There was no Date dimension, no ProductLine table, and the SupplyChainEvents table was doing two jobs at once (event info + supplier impact).

**Why it's a problem:**
- Without a Date table, the ontology can't answer time-based questions
- Without ProductLine, there's no way to navigate the product hierarchy
- An overloaded table confuses the ontology about what the entity represents

**What I did:**
- Created `DimDate` (shared date dimension)
- Created `ProductLine` (3 rows: Camping, Kitchen, Ski)
- Split SupplyChainEvents into `SupplyChainEvents` + `SupplyChainEventImpacts`

**Rule:** Each table should represent one business concept. If a table is doing two things, split it.

---

### Issue 5: Warehouses Table Was Missing From Ontology

**What happened:**
Even though Warehouses was in the semantic model, the ontology generator skipped it.

**Why it's a problem:**
Warehouses had no numeric columns to measure (no SUM, no COUNT target). The ontology generator prioritizes tables that have something to measure.

**What I did:**
Added DAX measures in the semantic model:
- `Total Warehouses = COUNTROWS('inventory warehouses')`
- `Total Capacity = SUM('inventory warehouses'[MaxCapacity])`

**Rule:** Every table in your semantic model should have at least one measure. Even a simple COUNTROWS is enough.

---

## Quick Checklist for Future Datasets

Before generating an ontology, check these:

| ✅ Check | Question to Ask |
|---|---|
| No duplicate column names with different types | Do any two tables have a column with the same name but different types? |
| No copied data in fact tables | Are columns like Name, Description, Category only in dimension tables? |
| Integer IDs everywhere | Are all ID columns numbers (not text like "WH_100")? |
| One table = one concept | Does any table try to represent two different things? |
| Every table has a measure | Can I COUNT or SUM something in every table? |
| Date dimension exists | Is there a shared date table for time-based queries? |
| Consistent naming | Do all primary keys follow the pattern {TableName}ID? |

---

## Ready-to-Use Copilot Prompt

You can use this prompt with GitHub Copilot (in terminal or IDE) to check any future dataset. Just point it at your data folder:

---

**Prompt 1: Analyze my data (use this first to find issues)**

```
I have CSV files for a Microsoft Fabric semantic model that will be used to generate an ontology. 
Please analyze all my CSV files and check for these specific issues:

1. DUPLICATE COLUMN NAMES WITH DIFFERENT TYPES
   - Find any column name that appears in more than one CSV file
   - For each duplicate, check if the data types are different (e.g., one is numeric, other is text)
   - If found, suggest unique names for each

2. DENORMALIZED / COPIED COLUMNS
   - Find columns like ProductName, SupplierName, CategoryName that appear in fact tables
   - These should only exist in their home dimension table
   - Flag any column that looks like it was copied from another table
   - Suggest removing it and keeping only the ID reference

3. ID COLUMN DATA TYPES
   - Check all columns ending in "ID"
   - Flag any that contain text values instead of integers
   - Suggest converting to integer IDs

4. OVERLOADED TABLES
   - Check if any table has columns that belong to two different business concepts
   - If a table mixes metadata with transactional data, suggest splitting it

5. MISSING DIMENSIONS
   - Check if there is a Date/Calendar dimension table
   - Check if there are tables that could serve as dimensions but are missing
   - Look at the hierarchy — can you drill from high-level to detail?

6. PRIMARY KEY CONSISTENCY
   - Check if all tables have a clear primary key
   - Check if PK naming follows {TableName}ID pattern
   - Flag any inconsistencies

7. MEASURE READINESS
   - For each table, check if there is at least one numeric column that could be used for SUM, AVG, or COUNT
   - Flag tables that have NO measurable columns (these may be skipped by ontology generator)

For each issue found, give me:
- Table name
- Column name
- What's wrong (one sentence)
- Exact fix (what to rename/remove/add)

Group results by: Critical (will break ontology) → Medium (will cause problems) → Nice-to-have (best practice)

Output as a simple table format that is easy to read.
```

---

**Prompt 2: Fix all issues automatically (use this after Prompt 1 to apply all fixes)**

```
Now fix all the issues you found. Do the following:

1. CREATE FIXED CSV FILES
   - For every CSV file that has issues, create a corrected version
   - Save all fixed CSVs in a new folder called "fixed_data" 
   - Do NOT modify my original files

2. APPLY THESE FIXES:
   a. RENAME duplicate column names — if two tables share a column name with different types,
      rename them to be unique (e.g., Priority → WarehousePriority and OrderPriority)
   
   b. REMOVE denormalized columns — remove any column from fact tables that is just a copy
      of data from a dimension table (e.g., remove ProductName from PurchaseOrderItems,
      keep only ProductID)
   
   c. CONVERT text IDs to integers — if any ID column has text values like "WH_100",
      create a mapping and convert to integer (1, 2, 3). Update ALL tables that reference that ID.
   
   d. SPLIT overloaded tables — if a table mixes two concepts, split it into two tables
      with a foreign key linking them
   
   e. CREATE missing dimension tables:
      - Create a Date dimension (DateKey, FullDate, Year, Quarter, Month, MonthName, Day, DayOfWeek, WeekOfYear, IsWeekend)
        covering from the earliest date in the data to 6 months from today
      - Create any other missing dimension tables needed for proper hierarchy
   
   f. FIX primary key naming — rename to follow {TableName}ID pattern
   
   g. FIX bad data values — correct negative values that should not be negative,
      fix decimal formatting issues (like 3.0 → 3 for integer columns)

3. CREATE A CHANGELOG
   - Create a markdown file showing what changed in each table
   - Format: Table name | What changed | Why

4. CREATE FABRIC NOTEBOOKS
   - Create PySpark notebooks that will create these tables in a Fabric Lakehouse
   - Use schema notebooks (CREATE TABLE) and load notebooks (read CSV → insert into table)
   - Important Fabric rules:
     → Do NOT use ALTER TABLE ADD CONSTRAINT (not supported in Fabric)
     → Use .write.mode("append").insertInto() instead of MERGE INTO
     → Use explicit StructType schemas for any table with integer columns
     → Put %run commands alone in their own cell (no other code)

5. VERIFY
   - Print a summary showing: table name, column count before, column count after, rows
   - Flag any remaining issues

Do everything now. Create all files. Show me the summary when done.
```

---

## Summary of Changes (Numbers)

| What | Before (V1) | After (V2) |
|---|---|---|
| Total tables | 11 | 14 |
| New tables added | — | DimDate, ProductLine, SupplyChainEventImpacts |
| Columns removed (duplicates) | — | 18 removed |
| Columns renamed | — | 3 renamed |
| ID columns fixed (text → integer) | — | WarehouseID in 6 tables |
| Bad data values corrected | — | 404 rows fixed |
| Ontology result | Product missing, Warehouses missing, Priority error | All 14 entities working ✅ |

---

*If you have questions about any of these changes, happy to walk through them together!*
