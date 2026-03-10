# Sales & Finance Data Generation Guide

Generates realistic sales and finance data for three business domains: Camping 🏕️, Kitchen 🍳, and Ski ⛷️.

## Quick Start

**Default Generation (1 year of data ending today):**
```bash
python main_generate_sales.py --enable-growth --graph --copydata --no-display
```

**Historical Data (6+ years):**

```bash
python main_generate_sales.py -s 2020-01-01 -e 2026-03-31 --enable-growth --graph --copydata --no-display
```

## Command Examples

```bash
# Historical data (6+ years)
python main_generate_sales.py -s 2020-01-01 -e 2026-03-31 --enable-growth --copydata --graph --no-display

# Single domain for testing
python main_generate_sales.py --camping-only --graph --no-display
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-s`, `--start-date` | Start date (YYYY-MM-DD, default: 1 year ago from today) |
| `-e`, `--end-date` | End date (YYYY-MM-DD, default: today) |
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
└── *.md              # Summary reports
```
