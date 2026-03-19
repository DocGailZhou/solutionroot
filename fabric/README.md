# Fabric Setup and Pipeline Run Guide

This guide walks through the full process from cloning the repo to running the Fabric pipeline and validating results.

## Prerequisites

- Microsoft Fabric access with permission to create a workspace, lakehouse, and notebooks
- Git installed on your machine
- This repository available locally

## Step 1. Create Fabric workspace and lakehouse

1. Create a new Fabric workspace.
2. In that workspace, create a Lakehouse. Example name: `miqdata`.
3. Open the lakehouse and make sure you can see the `Files` section.

## Step 2. Upload the `data` subfolder to the lakehouse

1. From this repo, locate `fabric/infra/data`.
2. In Fabric Lakehouse, go to `Files`.
3. Upload the full `data` folder (not individual files one by one).

After upload, your lakehouse path should look like:

- `Files/data/customer`
- `Files/data/product`
- `Files/data/camping`
- `Files/data/kitchen`
- `Files/data/ski`
- `Files/data/<product_line>/sales` (for example `Files/data/camping/sales`)
- `Files/data/<product_line>/finance` (for example `Files/data/camping/finance`)
- `Files/data/inventory`
- `Files/data/supplychain`

Important: notebook loaders use paths like `Files/data/customer`, `Files/data/product`, and `Files/data/<product_line>/<domain>`. If folder names change, load steps will fail.

## Step 4. Upload notebooks to Fabric

1. In your Fabric workspace, create a folder named `notebooks`.
2. Upload all notebooks from `fabric/src/fabric/notebooks`.
3. Include notebook files from subfolders as well:
   - `data_management`
   - `data_processing`
   - `schema`

At minimum, confirm these notebooks exist after upload:

- `main_pipeline.ipynb`
- `create_scheme_tables`
- `load_data_all_tables`

## Step 5. Attach lakehouse and run the pipeline

1. Open `main_pipeline.ipynb` in Fabric.
2. Attach the lakehouse you created (for example `miqdata`) to the notebook session.
3. Run the notebook top-to-bottom.

If you made changes to the notebooks or data, you can review and execute `update_pipeline.ipynb` 

1. Optional cleanup (commented by default):
   - `#%run truncate_all_tables`
   - `#%run drop_all_tables`
2. Schema and table creation:
   - `%run create_scheme_tables`
3. Data load into all tables:
   - `%run load_data_all_tables`

## Step 6. Expected output and validation

During a successful run, you should see messages similar to:

```text
All schemas and tables created successfully!
Customer schema: 5 tables, <n> records loaded
Product schema: 2 tables, <n> records loaded
Sales schema: 3 tables, <n> records loaded
Finance schema: 3 tables, <n> records loaded
Inventory schema: 6 tables, <n> records loaded
Supplychain schema: 3 tables, <n> records loaded
```

Final expected state:

- 6 schemas created: `customer`, `product`, `sales`, `finance`, `inventory`, `supplychain`
- 22 total tables created and populated
- Data loaded from `Files/data/...` into corresponding lakehouse tables

## Common issues

- `Path not found` errors: confirm `Files/data/...` folder structure matches exactly.
- Notebook reference errors on `%run`: verify all required notebooks were uploaded.
- Table already exists or duplicate-data scenarios: use the optional cleanup cells and rerun.