# Sales & Finance Data Generation Guide

Generates realistic sales and finance data for three business domains: Camping 🏕️, Kitchen 🍳, and Ski ⛷️.

## Interactive PowerShell Workflow (Recommended)

**Simplest Method - Just Run:**
```powershell
.\datagen.ps1
```

**What it does:**

- Interactive prompts with smart defaults (2025-01-01 to 2026-03-31)
- Generates sales data for all domains
- Auto-scales supply chain data based on sales volume
- Creates analytics graphs automatically
- Copies data to infra directories
- One-stop complete business dataset generation

**Interactive Options:**
- **Default dates**: 15-month period (full 2025 + Q1 2026)
- **Business growth**: Enabled by default (Press Enter)
- **Analytics graphs**: Enabled by default (Press Enter)
- **Copy data**: Enabled by default (Press Enter)

## Python Command Line (Advanced)

### Quick Examples

```bash
# Full example with all features (default dates)
python main_generate_sales.py --enable-growth --copydata --graph --no-display

# Custom date range with growth patterns
python main_generate_sales.py -s 2025-01-01 -e 2026-03-31 --enable-growth --graph --copydata --no-display

# Single domain for testing
python main_generate_sales.py --camping-only --graph --no-display

# Minimal dataset
python main_generate_sales.py -s 2025-11-01 -e 2025-12-31
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-s`, `--start-date` | Start date (YYYY-MM-DD, default: 2025-01-01) |
| `-e`, `--end-date` | End date (YYYY-MM-DD, default: 2026-03-31) |
| `--camping-only` | Generate only camping domain data |
| `--kitchen-only` | Generate only kitchen domain data |
| `--ski-only` | Generate only ski domain data |
| `--enable-growth` | Enable business growth patterns and market events |
| `--graph` | Generate monthly revenue trend graph |
| `--no-display` | Save graphs without GUI windows (for automation) |
| `--copydata` | Copy generated files to infra/data/ directory |

## 📁 Generated Files & Structure

### Output Directory Structure
```
output/
├── camping/
│   ├── sales/
│   │   ├── Order_Samples_Camping.csv
│   │   ├── OrderLine_Samples_Camping.csv
│   │   └── OrderPayment_Samples_Camping.csv
│   └── finance/
│       ├── Invoice_Samples_Camping.csv
│       ├── Payment_Samples_Camping.csv
│       └── Account_Samples_Camping.csv
├── kitchen/
│   ├── sales/ (same structure)
│   └── finance/ (same structure)
├── ski/
│   ├── sales/ (same structure)
│   └── finance/ (same structure)
├── sample_sales_data_summary.md
└── revenue_trend_graph.png (with --graph)
```

### Infrastructure Copy (with --copydata)
```
../../infra/data/
├── customer/          # Customer-related CSV files
├── product/           # Product-related CSV files
├── camping/           # Generated camping data (mirrors output structure)
├── kitchen/           # Generated kitchen data (mirrors output structure)
├── ski/               # Generated ski data (mirrors output structure)
├── inventory/         # Inventory and warehouse data
├── supplychain/       # Supply chain data
└── *.md              # Summary reports
```

### File Contents

**Sales Files:**
- **Order_Samples_*.csv**: Order headers (OrderID, CustomerID, OrderDate, OrderTotal, etc.)
- **OrderLine_Samples_*.csv**: Order line items (LineID, OrderID, ProductID, Quantity, UnitPrice, etc.)
- **OrderPayment_Samples_*.csv**: Payment records (PaymentID, OrderID, PaymentDate, Amount, etc.)

**Finance Files:**
- **Invoice_Samples_*.csv**: Invoice headers (InvoiceID, CustomerID, InvoiceDate, TotalAmount, etc.)
- **Payment_Samples_*.csv**: Payment transactions (PaymentID, InvoiceID, PaymentDate, Amount, etc.)
- **Account_Samples_*.csv**: Customer accounts (AccountID, CustomerID, Balance, CreditLimit, etc.)

## 📈 Business Growth Patterns (--enable-growth)

**Three-Phase Growth Simulation:**
- **Phase 1 (Months 1-5)**: Stable baseline business
- **Phase 2 (Months 6-10)**: Moderate growth with market expansion
- **Phase 3 (Months 11-15)**: Accelerated growth with optimization

**Market Events:**
- Black Friday sales spikes (November)
- Christmas holiday patterns (December)
- New Year promotions (January)
- Seasonal variations by domain

**Growth Effects:**
- Order volume increases over time
- Average order values grow
- Customer base expansion
- Seasonal purchasing patterns
