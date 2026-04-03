PS C:\Repos\Code\Explore\solutionroot\fabric\src\datagen> git pull origin main
remote: Enumerating objects: 46, done.
remote: Counting objects: 100% (46/46), done.
remote: Compressing objects: 100% (39/39), done.
remote: Total 44 (delta 5), reused 43 (delta 5), pack-reused 0 (from 0)
Unpacking objects: 100% (44/44), 188.16 KiB | 666.00 KiB/s, done.
From https://github.com/DocGailZhou/solutionroot
 * branch            main       -> FETCH_HEAD
   2048973..0736c16  main       -> origin/main
   Updating 2048973..0736c16
   Fast-forward
    .../findings/v2/data/inventory/DemandForecast.csv  |  421 ++
    fabric/findings/v2/data/inventory/Inventory.csv    |   82 +
    .../v2/data/inventory/InventoryTransactions.csv    | 4546 ++++++++++++++++++++
    .../v2/data/inventory/PurchaseOrderItems.csv       |  351 ++
    .../findings/v2/data/inventory/PurchaseOrders.csv  |  116 +
    fabric/findings/v2/data/inventory/Warehouses.csv   |    4 +
    .../product/ProductCategory_Samples_Camping.csv    |    9 +
    .../product/ProductCategory_Samples_Combined.csv   |   31 +
    .../product/ProductCategory_Samples_Kitchen.csv    |   13 +
    .../data/product/ProductCategory_Samples_Ski.csv   |   11 +
    fabric/findings/v2/data/product/ProductLine.csv    |    4 +
    .../v2/data/product/Product_Samples_Camping.csv    |   21 +
    .../v2/data/product/Product_Samples_Combined.csv   |   61 +
    .../v2/data/product/Product_Samples_Kitchen.csv    |   16 +
    .../v2/data/product/Product_Samples_Ski.csv        |   26 +
    .../v2/data/supplychain/ProductSuppliers.csv       |   76 +
    fabric/findings/v2/data/supplychain/Suppliers.csv  |    6 +
    .../data/supplychain/SupplyChainEventImpacts.csv   |   23 +
    .../v2/data/supplychain/SupplyChainEvents.csv      |   16 +
    .../v2/notebooks/data_processing/load_date.ipynb   |  125 +
    .../notebooks/data_processing/load_inventory.ipynb |  295 ++
    .../notebooks/data_processing/load_product.ipynb   |  169 +
    .../data_processing/load_supplychain.ipynb         |  203 +
    fabric/findings/v2/notebooks/run_pipeline.ipynb    |  235 +
    .../findings/v2/notebooks/schema/model_date.ipynb  |   75 +
    .../v2/notebooks/schema/model_inventory.ipynb      |  253 ++
    .../v2/notebooks/schema/model_product.ipynb        |  132 +
    .../v2/notebooks/schema/model_supplychain.ipynb    |  168 +
    fabric/findings/v2_Setup_Guide.md                  |  191 +
    fabric/findings/v2_guide_for_data_creator.md       |  247 ++
    fabric/findings/v2_tablewise_changes.md            |  161 +
    31 files changed, 8087 insertions(+)
    create mode 100644 fabric/findings/v2/data/inventory/DemandForecast.csv
    create mode 100644 fabric/findings/v2/data/inventory/Inventory.csv
    create mode 100644 fabric/findings/v2/data/inventory/InventoryTransactions.csv
    create mode 100644 fabric/findings/v2/data/inventory/PurchaseOrderItems.csv
    create mode 100644 fabric/findings/v2/data/inventory/PurchaseOrders.csv
    create mode 100644 fabric/findings/v2/data/inventory/Warehouses.csv
    create mode 100644 fabric/findings/v2/data/product/ProductCategory_Samples_Camping.csv
    create mode 100644 fabric/findings/v2/data/product/ProductCategory_Samples_Combined.csv
    create mode 100644 fabric/findings/v2/data/product/ProductCategory_Samples_Kitchen.csv
    create mode 100644 fabric/findings/v2/data/product/ProductCategory_Samples_Ski.csv
    create mode 100644 fabric/findings/v2/data/product/ProductLine.csv
    create mode 100644 fabric/findings/v2/data/product/Product_Samples_Camping.csv
    create mode 100644 fabric/findings/v2/data/product/Product_Samples_Combined.csv
    create mode 100644 fabric/findings/v2/data/product/Product_Samples_Kitchen.csv
    create mode 100644 fabric/findings/v2/data/product/Product_Samples_Ski.csv
    create mode 100644 fabric/findings/v2/data/supplychain/ProductSuppliers.csv
    create mode 100644 fabric/findings/v2/data/supplychain/Suppliers.csv
    create mode 100644 fabric/findings/v2/data/supplychain/SupplyChainEventImpacts.csv
    create mode 100644 fabric/findings/v2/data/supplychain/SupplyChainEvents.csv
    create mode 100644 fabric/findings/v2/notebooks/data_processing/load_date.ipynb
    create mode 100644 fabric/findings/v2/notebooks/data_processing/load_inventory.ipynb
    create mode 100644 fabric/findings/v2/notebooks/data_processing/load_product.ipynb
    create mode 100644 fabric/findings/v2/notebooks/data_processing/load_supplychain.ipynb
    create mode 100644 fabric/findings/v2/notebooks/run_pipeline.ipynb
    create mode 100644 fabric/findings/v2/notebooks/schema/model_date.ipynb
    create mode 100644 fabric/findings/v2/notebooks/schema/model_inventory.ipynb
    create mode 100644 fabric/findings/v2/notebooks/schema/model_product.ipynb
    create mode 100644 fabric/findings/v2/notebooks/schema/model_supplychain.ipynb
    create mode 100644 fabric/findings/v2_Setup_Guide.md
    create mode 100644 fabric/findings/v2_guide_for_data_creator.md
    create mode 100644 fabric/findings/v2_tablewise_changes.md