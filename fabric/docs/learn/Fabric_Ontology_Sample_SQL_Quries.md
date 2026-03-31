# Technical Query Examples for Fabric Ontology

This document provides the technical SQL query implementations that correspond to the natural language queries in the Fabric Ontology. These examples show how the semantic layer translates business questions into executable queries against your lakehouse.

## Query Implementation Examples

### 1. Current Stock Levels for Camping Products

**Natural Language**: "What's the current inventory level for camping products?"

**Generated SQL**:
```sql
SELECT 
    p.ProductName,
    p.ProductCategory,
    w.WarehouseName,
    w.Location,
    i.CurrentStock,
    i.ReorderPoint,
    i.LastUpdated
FROM inventory.inventory i
    INNER JOIN product.product p ON i.ProductID = p.ProductID
    INNER JOIN inventory.warehouses w ON i.WarehouseLocation = w.WarehouseName
WHERE p.ProductCategory = 'Camping'
    AND i.CurrentStock > 0
ORDER BY p.ProductName, w.WarehouseName
```

### 2. Low Stock Alerts

**Natural Language**: "Which products have inventory below the reorder point?"

**Generated SQL**:
```sql
SELECT 
    p.ProductName,
    p.ProductCategory,
    w.WarehouseName,
    i.CurrentStock,
    i.ReorderPoint,
    (i.ReorderPoint - i.CurrentStock) AS UnitsNeeded,
    CASE 
        WHEN i.CurrentStock = 0 THEN 'OUT OF STOCK'
        WHEN i.CurrentStock <= (i.ReorderPoint * 0.5) THEN 'CRITICAL'
        ELSE 'LOW STOCK'
    END AS AlertLevel
FROM inventory.inventory i
    INNER JOIN product.product p ON i.ProductID = p.ProductID
    INNER JOIN inventory.warehouses w ON i.WarehouseLocation = w.WarehouseName
WHERE i.CurrentStock < i.ReorderPoint
ORDER BY AlertLevel, (i.ReorderPoint - i.CurrentStock) DESC
```

### 3. Supplier Performance Analysis

**Natural Language**: "What's the average lead time for each supplier?"

**Generated SQL**:
```sql
SELECT 
    s.SupplierName,
    s.ContactInfo,
    COUNT(po.PurchaseOrderID) AS TotalOrders,
    AVG(DATEDIFF(day, po.OrderDate, po.DeliveryDate)) AS AvgLeadTimeDays,
    MIN(DATEDIFF(day, po.OrderDate, po.DeliveryDate)) AS MinLeadTimeDays,
    MAX(DATEDIFF(day, po.OrderDate, po.DeliveryDate)) AS MaxLeadTimeDays,
    COUNT(CASE WHEN po.DeliveryDate <= po.ExpectedDeliveryDate THEN 1 END) * 100.0 / COUNT(*) AS OnTimePercentage
FROM supplychain.suppliers s
    INNER JOIN inventory.purchaseorders po ON s.SupplierName = po.SupplierName
WHERE po.DeliveryDate IS NOT NULL
    AND po.OrderDate >= DATEADD(month, -12, GETDATE())
GROUP BY s.SupplierName, s.ContactInfo
ORDER BY AvgLeadTimeDays
```

### 4. Product Sourcing Overview

**Natural Language**: "Which suppliers can provide kitchen products?"

**Generated SQL**:
```sql
SELECT 
    s.SupplierName,
    s.ContactInfo,
    s.LeadTimeDays,
    ps.IsPrimarySupplier,
    COUNT(p.ProductID) AS KitchenProductCount,
    STRING_AGG(p.ProductName, ', ') AS AvailableProducts
FROM supplychain.suppliers s
    INNER JOIN supplychain.productsuppliers ps ON s.SupplierName = ps.SupplierName
    INNER JOIN product.product p ON ps.ProductID = p.ProductID
WHERE p.ProductCategory = 'Kitchen'
GROUP BY s.SupplierName, s.ContactInfo, s.LeadTimeDays, ps.IsPrimarySupplier
ORDER BY ps.IsPrimarySupplier DESC, s.LeadTimeDays
```

### 5. Supply Chain Disruption Impact

**Natural Language**: "Show recent supply chain disruption events and their impact"

**Generated SQL**:
```sql
SELECT 
    sce.EventDate,
    sce.EventType,
    sce.Description,
    sce.SeverityLevel,
    sce.ProductCategory,
    s.SupplierName,
    s.ContactInfo,
    -- Impact analysis
    COUNT(DISTINCT ps.ProductID) AS AffectedProducts,
    SUM(i.CurrentStock) AS TotalImpactedInventory,
    AVG(i.CurrentStock) AS AvgStockLevel
FROM supplychain.supplychainevents sce
    LEFT JOIN supplychain.suppliers s ON sce.SupplierID = s.SupplierID
    LEFT JOIN supplychain.productsuppliers ps ON s.SupplierName = ps.SupplierName
    LEFT JOIN inventory.inventory i ON ps.ProductID = i.ProductID
WHERE sce.EventDate >= DATEADD(month, -6, GETDATE())
    AND sce.SeverityLevel IN ('High', 'Critical')
GROUP BY sce.EventDate, sce.EventType, sce.Description, sce.SeverityLevel, 
         sce.ProductCategory, s.SupplierName, s.ContactInfo
ORDER BY sce.EventDate DESC, sce.SeverityLevel DESC
```

### 6. Demand Forecasting Analysis

**Natural Language**: "What's the forecasted demand for ski products next quarter?"

**Generated SQL**:
```sql
SELECT 
    p.ProductName,
    p.ProductCategory,
    df.ForecastDate,
    df.PredictedDemand,
    df.ConfidenceLevel,
    i.CurrentStock,
    CASE 
        WHEN i.CurrentStock >= df.PredictedDemand THEN 'Sufficient Stock'
        WHEN i.CurrentStock >= (df.PredictedDemand * 0.7) THEN 'Monitor Stock'
        ELSE 'Reorder Required'
    END AS StockStatus
FROM inventory.demandforecast df
    INNER JOIN product.product p ON df.ProductID = p.ProductID
    LEFT JOIN inventory.inventory i ON p.ProductID = i.ProductID
WHERE p.ProductCategory = 'Ski'
    AND df.ForecastDate BETWEEN GETDATE() AND DATEADD(month, 3, GETDATE())
    AND df.ConfidenceLevel >= 80
ORDER BY df.ForecastDate, df.PredictedDemand DESC
```

### 7. End-to-End Supply Chain View

**Natural Language**: "Show me the complete supply chain flow for Product ID 'CAMP_TENT_001'"

**Generated SQL**:
```sql
-- Product Information
SELECT 'Product Info' AS DataType,
    p.ProductID,
    p.ProductName,
    p.ProductCategory,
    p.Price,
    pc.CategoryDescription
FROM product.product p
    LEFT JOIN product.productcategory pc ON p.ProductCategory = pc.CategoryName
WHERE p.ProductID = 'CAMP_TENT_001'

UNION ALL

-- Current Inventory
SELECT 'Current Inventory' AS DataType,
    i.ProductID,
    CONCAT(w.WarehouseName, ' (', w.Location, ')') AS Details,
    CAST(i.CurrentStock AS VARCHAR(50)) AS Value1,
    CAST(i.ReorderPoint AS VARCHAR(50)) AS Value2,
    CAST(i.LastUpdated AS VARCHAR(50)) AS Value3
FROM inventory.inventory i
    INNER JOIN inventory.warehouses w ON i.WarehouseLocation = w.WarehouseName
WHERE i.ProductID = 'CAMP_TENT_001'

UNION ALL

-- Supplier Information  
SELECT 'Suppliers' AS DataType,
    ps.ProductID,
    s.SupplierName AS Details,
    CASE WHEN ps.IsPrimarySupplier = 1 THEN 'Primary' ELSE 'Backup' END AS Value1,
    CAST(s.LeadTimeDays AS VARCHAR(50)) AS Value2,
    s.ContactInfo AS Value3
FROM supplychain.productsuppliers ps
    INNER JOIN supplychain.suppliers s ON ps.SupplierName = s.SupplierName
WHERE ps.ProductID = 'CAMP_TENT_001'

ORDER BY DataType, Details
```

### 8. Purchase Order Planning

**Natural Language**: "Which products should we order based on current inventory and demand forecast?"

**Generated SQL**:
```sql
WITH InventorySummary AS (
    SELECT 
        i.ProductID,
        SUM(i.CurrentStock) AS TotalCurrentStock,
        MAX(i.ReorderPoint) AS MaxReorderPoint
    FROM inventory.inventory i
    GROUP BY i.ProductID
),
DemandSummary AS (
    SELECT 
        df.ProductID,
        SUM(df.PredictedDemand) AS TotalForecastedDemand
    FROM inventory.demandforecast df
    WHERE df.ForecastDate BETWEEN GETDATE() AND DATEADD(month, 3, GETDATE())
        AND df.ConfidenceLevel >= 75
    GROUP BY df.ProductID
),
SupplierInfo AS (
    SELECT 
        ps.ProductID,
        s.SupplierName,
        s.LeadTimeDays,
        ps.IsPrimarySupplier
    FROM supplychain.productsuppliers ps
        INNER JOIN supplychain.suppliers s ON ps.SupplierName = s.SupplierName
    WHERE ps.IsPrimarySupplier = 1
)
SELECT 
    p.ProductName,
    p.ProductCategory,
    ISNULL(inv.TotalCurrentStock, 0) AS CurrentStock,
    ISNULL(inv.MaxReorderPoint, 0) AS ReorderPoint,
    ISNULL(dem.TotalForecastedDemand, 0) AS Q3ForecastDemand,
    sup.SupplierName,
    sup.LeadTimeDays,
    -- Calculation for suggested order quantity
    CASE 
        WHEN ISNULL(inv.TotalCurrentStock, 0) < ISNULL(inv.MaxReorderPoint, 0) THEN 
            GREATEST(
                (ISNULL(inv.MaxReorderPoint, 0) - ISNULL(inv.TotalCurrentStock, 0)),
                (ISNULL(dem.TotalForecastedDemand, 0) - ISNULL(inv.TotalCurrentStock, 0))
            )
        WHEN ISNULL(inv.TotalCurrentStock, 0) < ISNULL(dem.TotalForecastedDemand, 0) THEN
            (ISNULL(dem.TotalForecastedDemand, 0) - ISNULL(inv.TotalCurrentStock, 0))
        ELSE 0
    END AS SuggestedOrderQuantity,
    -- Priority classification
    CASE 
        WHEN ISNULL(inv.TotalCurrentStock, 0) = 0 THEN 'URGENT - OUT OF STOCK'
        WHEN ISNULL(inv.TotalCurrentStock, 0) < ISNULL(inv.MaxReorderPoint, 0) THEN 'HIGH - Below Reorder Point'
        WHEN ISNULL(inv.TotalCurrentStock, 0) < ISNULL(dem.TotalForecastedDemand, 0) THEN 'MEDIUM - Below Forecast'
        ELSE 'LOW - Adequate Stock'
    END AS OrderPriority
FROM product.product p
    LEFT JOIN InventorySummary inv ON p.ProductID = inv.ProductID
    LEFT JOIN DemandSummary dem ON p.ProductID = dem.ProductID
    LEFT JOIN SupplierInfo sup ON p.ProductID = sup.ProductID
WHERE CASE 
        WHEN ISNULL(inv.TotalCurrentStock, 0) < ISNULL(inv.MaxReorderPoint, 0) THEN 
            GREATEST(
                (ISNULL(inv.MaxReorderPoint, 0) - ISNULL(inv.TotalCurrentStock, 0)),
                (ISNULL(dem.TotalForecastedDemand, 0) - ISNULL(inv.TotalCurrentStock, 0))
            )
        WHEN ISNULL(inv.TotalCurrentStock, 0) < ISNULL(dem.TotalForecastedDemand, 0) THEN
            (ISNULL(dem.TotalForecastedDemand, 0) - ISNULL(inv.TotalCurrentStock, 0))
        ELSE 0
    END > 0
ORDER BY 
    CASE OrderPriority
        WHEN 'URGENT - OUT OF STOCK' THEN 1
        WHEN 'HIGH - Below Reorder Point' THEN 2
        WHEN 'MEDIUM - Below Forecast' THEN 3
        ELSE 4
    END,
    SuggestedOrderQuantity DESC
```

## Key SQL Conventions Applied

Based on your lakehouse schema:

1. **Schema Naming**: All lowercase (`product`, `inventory`, `supplychain`)
2. **Reserved Keywords**: `sales.[order]` requires brackets
3. **ID Columns**: UpperCase pattern (`ProductID`, `CustomerID`, `SupplierID`)
4. **Boolean Fields**: Use `= 1` / `= 0` instead of `= true` / `= false`
5. **Join Patterns**: Following established FK relationships
6. **Nullable FKs**: LEFT JOINs for `supplychainevents.SupplierID`

## Performance Considerations

1. **Indexing**: Ensure indexes on frequently joined columns (`ProductID`, `SupplierID`, etc.)
2. **Date Filtering**: Use SARGable predicates for date ranges
3. **Aggregations**: Consider materialized views for complex aggregations
4. **Partitioning**: Consider partitioning by date for large transaction tables

## Integration with Fabric Ontology

These SQL queries demonstrate how the semantic layer:
- Translates natural language to precise SQL
- Handles join relationships automatically
- Applies business logic (reorder calculations, priority classifications)
- Provides consistent column naming and formatting
- Ensures data quality through proper filtering and validation