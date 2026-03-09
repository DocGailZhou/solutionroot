# Quick Run Examples 

## Prerequisites  
Ensure configuration files exist in `input/` directory:
- `suppliers.json` - Supplier master data
- `warehouses.json` - Warehouse locations and details

```bash
# Program location
cd datagen\src\data_generator
```

## PowerShell Orchestrator (Runs Both Sequentially and Automatically)

**Interactive Mode** - Simplest approach:

```powershell
cd datagen\src\data_generator
.\datagen.ps1
```

## Run Separate Processes 

### Sales and Finance Data 
```bash
python main_generate_sales.py -s 2025-01-01 -e 2026-03-31 --enable-growth --copydata --graph --no-display
```

### Supply Chain Data Options

**Auto-Scale (Recommended)** - Analyzes sales data automatically:

```bash
python main_generate_supplychain.py -s 2025-01-01 -e 2026-03-31 --auto-scale --copydata --graph --no-display
```

**Manual Parameters** - If you want to produce independent data without sales history:
```bash
python main_generate_supplychain.py -s 2025-01-01 -e 2026-03-31 --num-orders 125 --num-transactions 2000 --copydata --graph --no-display
```

