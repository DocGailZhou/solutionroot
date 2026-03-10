# Supply Chain Data Generation Guide

Generates intelligent supplier management and inventory data with auto-scaling based on sales patterns. 

## Interactive PowerShell Workflow (Recommended)

**Simplest Method - Complete Business Dataset:**
```powershell
.\datagen.ps1
```

**What it does:**
- Interactive prompts for two separate date ranges:
  - **Sales period**: Default 2020-01-01 to 2026-03-31 (6+ years for analysis)
  - **Supply chain period**: Default 2025-01-01 to 2026-03-31 (recent operations)
- First generates sales data for long-term trend analysis
- Then auto-scales supply chain data based on recent sales volume only
- Creates comprehensive analytics dashboard (4-chart visualization)
- Copies all data to infra directories
- Complete business simulation with historical context

**Interactive Options:**
- **Sales data**: 6+ years of historical data for trend analysis
- **Supply chain**: Recent 15-month period for current operations scaling
- **Business growth**: Enabled by default (for realistic sales patterns)
- **Analytics graphs**: Enabled by default (revenue + supply chain dashboards)
- **Copy data**: Enabled by default (to infra/data directories)

## � Prerequisites

### Required Configuration Files
- **suppliers.json**: Located in `input/` directory - supplier master data and product relationships
- **warehouses.json**: Located in `input/` directory - warehouse locations, addresses, and operational details  

### Sales Data (Optional but Recommended)
For auto-scaling, ensure sales data exists in `output/[camping|kitchen|ski]/sales/` directories.

## Python Command Line (Advanced)

### Quick Examples

```bash
# Auto-scale (recommended): Analyzes existing sales data
python main_generate_supplychain.py --auto-scale --graph --copydata --no-display

# Custom date range with auto-scaling
python main_generate_supplychain.py -s 2025-01-01 -e 2026-03-31 --auto-scale --graph --copydata --no-display

# Manual parameters (if no sales data exists)
python main_generate_supplychain.py --num-orders 125 --num-transactions 2000 --graph --copydata --no-display

# Testing with smaller dataset
python main_generate_supplychain.py --auto-scale --num-orders 10 --num-transactions 50 --no-display
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--auto-scale` | **Auto-calculate parameters based on existing sales data (recommended)** |
| `-s`, `--start-date` | Start date (YYYY-MM-DD, default: 2025-01-01) |
| `-e`, `--end-date` | End date (YYYY-MM-DD, default: 2026-03-31) |
| `--graph` | Generate 4-chart analytics dashboard |
| `--no-display` | Save graphs without GUI windows (for automation) |
| `--copydata` | Copy generated files to infra/data/ directory |
| `--num-orders` | Number of purchase orders (default: 30, overridden by auto-scale) |
| `--num-transactions` | Number of inventory transactions (default: 500, overridden by auto-scale) |
| `--inventory-only` | Generate only inventory data (requires existing supplier data) |
| `--num-events` | Number of supply chain events (default: 15) |

## 🧠 Auto-Scaling Intelligence

### How Auto-Scale Works

**Sales Data Analysis Process:**
1. Scans `output/[camping|kitchen|ski]/sales/` directories for OrderLine CSV files
2. Loads and filters sales data by the specified date range
3. Counts total sales line items and orders across all product categories
4. Analyzes product-level sales velocity and demand patterns

**Parameter Calculation Logic:**

**Purchase Order Scaling:**
- Uses realistic ratio of ~1 purchase order per 400-500 sales line items
- Business logic: Most companies consolidate orders for efficiency
- Applies minimum of 20 orders and maximum of 200 orders
- Example: 50,504 line items ÷ 450 = 112 purchase orders

**Inventory Transaction Scaling:**
- Calculates 2-3x sales volume (receipts, adjustments, transfers, issues)
- Business logic: Multiple inventory movements per sale (receipt → putaway → pick → ship)
- Applies daily transaction caps (15 per day maximum) for realistic volume
- Uses date range duration for proper temporal distribution
- Example: 50,504 × 2.7 = 136,361 but capped at 455 days × 15 = 6,825 transactions

**Inventory Level Intelligence:**
- Each product's stock levels based on actual sales velocity from historical data
- Safety stock calculated as 2-4 weeks of average monthly sales per product
- Reorder points determined by supplier lead times plus safety stock
- Current stock levels vary realistically around reorder points
- Some products intentionally set to low-stock scenarios for realism

### Example Auto-Scale Results
```
📈 Sales Analysis: 50,504 line items from 18,669 orders (Camping, Kitchen, Ski)
📊 Calculated Parameters:
   • Purchase Orders: 112 (was default 30)
   • Inventory Transactions: 6,825 (was default 500) 
   • Daily Transaction Rate: ~15 transactions/day
   • Coverage: 455 days of business activity
✅ Using auto-calculated parameters for realistic business simulation
```

## 📁 Generated Files & Structure

### Output Directory Structure
```
output/
├── supplychain/
│   ├── Suppliers.csv
│   ├── ProductSuppliers.csv
│   └── SupplyChainEvents.csv
├── inventory/
│   ├── Warehouses.csv
│   ├── Inventory.csv
│   ├── PurchaseOrders.csv
│   ├── PurchaseOrderItems.csv
│   ├── InventoryTransactions.csv
│   └── DemandForecast.csv
├── sample_supplychain_data_summary.md
└── supply_chain_analytics_dashboard.png (with --graph)
```

### Infrastructure Copy (with --copydata)
```
../../infra/data/
├── supplychain/ (mirrors output structure)
└── inventory/ (mirrors output structure)
```

### File Contents

**Supplier Files:**
- **Suppliers.csv**: Supplier master data (SupplierID, Name, ContactInfo, LeadTime, etc.)
- **ProductSuppliers.csv**: Product-supplier relationships (ProductID, SupplierID, IsBackup, etc.)
- **SupplyChainEvents.csv**: Risk events and disruptions (EventID, EventType, ImpactLevel, etc.)

**Inventory Files:**
- **Warehouses.csv**: Master warehouse data (WarehouseID, DisplayName, Address, Phone, Manager, etc.)
- **Inventory.csv**: Current stock levels (ProductID, CurrentStock, ReorderPoint, SafetyStock, etc.)
- **PurchaseOrders.csv**: Purchase order headers (OrderID, SupplierID, OrderDate, Status, etc.)
- **PurchaseOrderItems.csv**: Purchase order line items (ItemID, OrderID, ProductID, Quantity, etc.)
- **InventoryTransactions.csv**: Stock movements (TransactionID, ProductID, Type, Quantity, Date, etc.)
- **DemandForecast.csv**: 3-month demand predictions (ProductID, ForecastDate, ForecastQuantity, etc.)

## 📊 Analytics Dashboard (--graph)

### Four-Chart Business Intelligence Dashboard

**Chart 1: Demand Forecast vs Recent Sales Reality**
- Compares 3-month demand forecasts with actual sales patterns
- Shows forecasting accuracy and seasonal trends
- Helps identify planning gaps and opportunities

**Chart 2: Warehouse Capacity Utilization**  
- Current inventory levels vs. maximum capacity
- High utilization (>70%) and critical capacity (>90%) indicators
- Helps identify storage constraints and expansion needs

**Chart 3: Inventory Health Status**
- Stock levels by product category (Camping, Kitchen, Ski)
- Safety stock vs. current stock analysis
- Low stock and overstock identification

**Chart 4: Supplier Performance Matrix**
- Risk score vs. reliability analysis
- Primary vs. backup supplier visualization
- Performance-based supplier selection insights

### Professional Output
- High-resolution PNG (150 DPI)
- Date-specific filenames: `supply_chain_analytics_dashboard.png`
- Clean, font-compatible charts (no emoji dependencies)
- Business-ready visualization for reports and presentations

## 🔗 Integration Workflow

### Standalone Supply Chain Generation
```bash
# Generate only supply chain data (requires existing sales data)
python main_generate_supplychain.py --auto-scale --graph --copydata --no-display
```

### Complete Business Dataset (Sales + Supply Chain)
```powershell
# Interactive orchestration (recommended)
.\datagen.ps1

# Manual two-phase generation:
python main_generate_sales.py -s 2025-01-01 -e 2026-03-31 --enable-growth --copydata --graph --no-display
