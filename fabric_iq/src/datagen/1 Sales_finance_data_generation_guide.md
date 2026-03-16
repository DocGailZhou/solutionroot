# Sales & Finance Data Generation Guide

Generates realistic sales and finance data for three business domains: Camping 🏕️, Kitchen 🍳, and Ski ⛷️.

## Command Examples

```bash
# Historical data (6+ years)
python main_generate_sales.py -s 2020-01-01 -e 2026-03-31 --enable-growth --copydata --graph --no-display

# Standard business period
python main_generate_sales.py -s 2025-01-01 -e 2026-04-30 --enable-growth --graph --copydata

```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-s`, `--start-date` | **Required**: Start date (YYYY-MM-DD) |
| `-e`, `--end-date` | **Required**: End date (YYYY-MM-DD) |
| `--camping-only` | Generate only camping domain data |
| `--kitchen-only` | Generate only kitchen domain data |
| `--ski-only` | Generate only ski domain data |
| `--enable-growth` | Enable business growth patterns and market events |
| `--graph` | Generate monthly revenue trend graph |
| `--no-display` | Save graphs without GUI windows (for automation) |
| `--copydata` | Copy generated files to infra/data/ directory |



## 📁 Generated Files & Structure

### Output Directory Structure

output/
├── finance/
│ ├── camping/
│ ├── kitchen/
│ └── ski/
├── sales/
│ ├── camping/
│ ├── kitchen/
│ └── ski/
├── sample_sales_data_summary.md
└── revenue_trend_graph.png (with --graph)
