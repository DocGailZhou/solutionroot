# Smart Data Generation Suite

### ✨ Auto-Scale Supply Chain Parameters
The supply chain generator now automatically calculates optimal parameters based on your sales data!

```bash
python main_generate_supplychain.py --auto-scale -s 2025-01-01 -e 2026-03-31
```

**What the --auto-scale does:**

- Analyzes existing sales data from `output/` directory
- Calculates optimal purchase orders (~1 PO per 400-500 line items)  
- Scales inventory transactions (2-3x sales volume)
- Displays calculated vs default parameters
- Uses intelligent date range filtering

### 🎯 PowerShell Orchestration Script
The PowerShell script handles the complete workflow automatically:

## PowerShell Script (Recommended)
**`datagen.ps1`**

```powershell
# Interactive mode (prompts for dates)
.\datagen.ps1

# Direct execution  
.\datagen.ps1 -StartDate "2025-01-01" -EndDate "2026-03-31"

# Full feature execution
.\datagen.ps1 -StartDate "2025-01-01" -EndDate "2026-03-31" -EnableGrowth -GenerateGraphs -CopyData
```

## Workflow
1. **Sales Generation**: Creates comprehensive sales data across all categories
2. **Auto-Scale Analysis**: Analyzes sales volume and calculates optimal supply chain parameters  
3. **Supply Chain Generation**: Creates inventory, purchase orders, and transactions scaled to sales
4. **Integration**: Links sales patterns with supply chain operations

## Example Output
```
🚀 Auto-scaling enabled - analyzing existing sales data...
────────────────────────────────────────────────────────────────
📈 Sales Analysis: 50,504 line items from 18,669 orders (Camping, Kitchen, Ski)
📊 Calculated Parameters:
   • Purchase Orders: 112 (was 30)
   • Inventory Transactions: 6,825 (was 500)
✅ Using auto-calculated parameters
```

## Manual Override
You can still use manual parameters if needed:
```bash
python main_generate_supplychain.py -s 2025-01-01 -e 2026-03-31 --num-orders 50 --num-transactions 800
```

## Benefits
- **Realistic Scaling**: Supply chain data matches actual sales volume
- **Time Saving**: No manual parameter calculation needed
- **Integrated Workflow**: One command generates complete business dataset  
- **Intelligent Defaults**: Falls back gracefully when sales data is not available
- **Date Consistency**: Ensures sales and supply chain data use same date range