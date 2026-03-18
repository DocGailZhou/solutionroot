# Data Source Instructions - Fabric IQ Lakehouse

## Overview

This document provides specific instructions for querying and working with data sources in the Fabric IQ lakehouse. Follow these instructions to ensure optimal performance, data accuracy, and consistent results across all six domain schemas.

---

## General Query Guidelines

### 1. Schema and Table Naming Conventions

Always use fully qualified table names when writing queries:

```sql
-- Correct: schema-qualified names
SELECT * FROM customer.Customer
SELECT * FROM product.Product
SELECT * FROM sales.Order
SELECT * FROM finance.invoice
SELECT * FROM inventory.Inventory
SELECT * FROM supplychain.Suppliers

-- Avoid unqualified names (may cause ambiguity)
SELECT * FROM Customer   -- ambiguous
SELECT * FROM Order      -- ambiguous
```

**Note**: Finance table names are lowercase (`invoice`, `account`, `payment`) as defined in the schema. All other tables use PascalCase.

---

### 2. Performance Optimization Principles

- **Use specific column selection**: Avoid `SELECT *` for large result sets; name the columns you need
- **Apply filters early**: Use `WHERE` clauses to limit data before joining or aggregating
- **Filter on date or category columns**: These are the most effective filters for narrowing data
- **Aggregate before joining when possible**: Reduces the number of rows processed in joins
- **Use `LIMIT` for exploratory queries**: Avoid full table scans when exploring data

```sql
-- Efficient: filter early, select only needed columns
SELECT o.OrderDate, o.OrderTotal, o.OrderStatus
FROM sales.Order o
WHERE o.OrderDate >= '2025-01-01'
  AND o.OrderStatus = 'Completed'
LIMIT 100

-- Less efficient: no filter, all columns
SELECT * FROM sales.Order
```

---

### 3. Data Type Handling

- **STRING fields**: Use single quotes for literal values — `WHERE OrderStatus = 'Completed'`
- **DATE fields**: Use ISO format `YYYY-MM-DD` — `WHERE OrderDate >= '2025-06-01'`
- **DECIMAL fields**: Handle NULL values appropriately in calculations — use `COALESCE(field, 0)`
- **BOOLEAN fields**: Use `true` / `false` (lowercase) — `WHERE IsActive = true`
- **INT fields**: No quotes needed — `WHERE QuantityOrdered > 50`

---

## Domain-Specific Query Instructions

### Customer Domain Queries

#### Customer Segmentation
```sql
-- Customer count by type and relationship tier
SELECT 
    CustomerTypeId,
    CustomerRelationshipTypeId,
    COUNT(*) AS CustomerCount,
    SUM(CASE WHEN IsActive = true THEN 1 ELSE 0 END) AS ActiveCount
FROM customer.Customer
GROUP BY CustomerTypeId, CustomerRelationshipTypeId
ORDER BY CustomerCount DESC
```

#### Customer Demographics
```sql
-- Average age and gender breakdown for active customers
SELECT 
    Gender,
    CustomerRelationshipTypeId,
    COUNT(*) AS CustomerCount,
    ROUND(AVG(DATEDIFF(CURRENT_DATE(), DateOfBirth) / 365.0), 1) AS AvgAge
FROM customer.Customer
WHERE IsActive = true
  AND DateOfBirth IS NOT NULL
  AND Gender IS NOT NULL
GROUP BY Gender, CustomerRelationshipTypeId
ORDER BY CustomerCount DESC
```

#### Customer Location Distribution
```sql
-- Customer count by region
SELECT 
    Region,
    StateId,
    COUNT(*) AS LocationCount
FROM customer.Location
WHERE IsActive = true
GROUP BY Region, StateId
ORDER BY LocationCount DESC
```

---

### Product Domain Queries

#### Product Catalog Overview
```sql
-- Products by category with pricing summary
SELECT 
    CategoryName,
    COUNT(*) AS ProductCount,
    ROUND(AVG(ListPrice), 2) AS AvgListPrice,
    ROUND(AVG(StandardCost), 2) AS AvgStandardCost,
    ROUND(AVG(ListPrice - StandardCost), 2) AS AvgGrossMargin
FROM product.Product
WHERE ProductStatus = 'active'
  AND ListPrice > 0
  AND StandardCost > 0
GROUP BY CategoryName
ORDER BY AvgGrossMargin DESC
```

#### Active Products by Category
```sql
-- All active products with pricing
SELECT ProductName, BrandName, CategoryName, ListPrice, StandardCost, ProductStatus
FROM product.Product
WHERE ProductStatus = 'active'
  AND (SellEndDate IS NULL OR SellEndDate >= CURRENT_DATE())
ORDER BY CategoryName, ListPrice DESC
```

---

### Sales Domain Queries

#### Sales Performance Trend
```sql
-- Monthly order count and revenue
SELECT 
    YEAR(OrderDate) AS OrderYear,
    MONTH(OrderDate) AS OrderMonth,
    COUNT(*) AS OrderCount,
    ROUND(SUM(OrderTotal), 2) AS TotalRevenue,
    ROUND(AVG(OrderTotal), 2) AS AvgOrderValue
FROM sales.Order
WHERE OrderStatus = 'Completed'
GROUP BY YEAR(OrderDate), MONTH(OrderDate)
ORDER BY OrderYear DESC, OrderMonth DESC
```

#### Revenue by Product Category
```sql
-- Revenue breakdown by product category using order lines
SELECT 
    ol.ProductName,
    COUNT(DISTINCT o.OrderId) AS OrderCount,
    SUM(ol.Quantity) AS TotalUnitsSold,
    ROUND(SUM(ol.LineTotal), 2) AS TotalRevenue
FROM sales.Order o
JOIN sales.OrderLine ol ON o.OrderId = ol.OrderId
WHERE o.OrderStatus = 'Completed'
GROUP BY ol.ProductName
ORDER BY TotalRevenue DESC
LIMIT 20
```

#### Payment Method Analysis
```sql
-- Order volume and revenue by payment method
SELECT 
    PaymentMethod,
    COUNT(*) AS OrderCount,
    ROUND(SUM(OrderTotal), 2) AS TotalRevenue,
    ROUND(AVG(OrderTotal), 2) AS AvgOrderValue
FROM sales.Order
WHERE OrderStatus = 'Completed'
GROUP BY PaymentMethod
ORDER BY TotalRevenue DESC
```

---

### Finance Domain Queries

#### Invoice Status Summary
```sql
-- Outstanding vs paid invoice breakdown
SELECT 
    InvoiceStatus,
    COUNT(*) AS InvoiceCount,
    ROUND(SUM(TotalAmount), 2) AS TotalValue,
    ROUND(AVG(TotalAmount), 2) AS AvgInvoiceValue
FROM finance.invoice
GROUP BY InvoiceStatus
ORDER BY TotalValue DESC
```

#### Account Balance by Type and Status
```sql
-- Account balances grouped by type and status
SELECT 
    AccountType,
    AccountStatus,
    COUNT(*) AS AccountCount,
    ROUND(SUM(Balance), 2) AS TotalBalance,
    ROUND(AVG(Balance), 2) AS AvgBalance
FROM finance.account
GROUP BY AccountType, AccountStatus
ORDER BY AccountType, AccountStatus
```

#### Payment History
```sql
-- Monthly payment totals
SELECT 
    YEAR(PaymentDate) AS PaymentYear,
    MONTH(PaymentDate) AS PaymentMonth,
    COUNT(*) AS PaymentCount,
    ROUND(SUM(PaymentAmount), 2) AS TotalPayments,
    PaymentStatus
FROM finance.payment
GROUP BY YEAR(PaymentDate), MONTH(PaymentDate), PaymentStatus
ORDER BY PaymentYear DESC, PaymentMonth DESC
```

---

### Inventory Domain Queries

#### Current Stock Status
```sql
-- Stock status for all products and warehouses
SELECT 
    ProductName,
    ProductCategory,
    WarehouseLocation,
    CurrentStock,
    ReservedStock,
    AvailableStock,
    ReorderPoint,
    SafetyStockLevel,
    Status
FROM inventory.Inventory
ORDER BY ProductCategory, ProductName, WarehouseLocation
```

#### Products Needing Reorder
```sql
-- Products at or below reorder point
SELECT 
    ProductName,
    ProductCategory,
    WarehouseLocation,
    CurrentStock,
    ReorderPoint,
    SafetyStockLevel,
    Status
FROM inventory.Inventory
WHERE CurrentStock <= ReorderPoint
ORDER BY CurrentStock ASC
```

#### Purchase Order Status
```sql
-- Pending and in-transit purchase orders
SELECT 
    PurchaseOrderNumber,
    SupplierName,
    OrderDate,
    ExpectedDeliveryDate,
    ActualDeliveryDate,
    TotalOrderValue,
    Status,
    Priority
FROM inventory.PurchaseOrders
WHERE Status IN ('Pending', 'Shipped')
ORDER BY ExpectedDeliveryDate ASC
```

#### Inventory Transaction History
```sql
-- Recent inventory movements by product and warehouse
SELECT 
    ProductName,
    ProductCategory,
    WarehouseLocation,
    TransactionType,
    TransactionDate,
    Quantity,
    StockBefore,
    StockAfter,
    ReferenceNumber
FROM inventory.InventoryTransactions
WHERE TransactionDate >= '2025-10-01'
ORDER BY TransactionDate DESC
LIMIT 100
```

---

### Supply Chain Domain Queries

#### Supplier Network Overview
```sql
-- All suppliers with type, status, and reliability
SELECT 
    SupplierName,
    SupplierType,
    Status,
    ProductCategory,
    LeadTimeDays,
    ReliabilityScore,
    Location
FROM supplychain.Suppliers
ORDER BY SupplierType, ProductCategory
```

#### Active Disruption Events
```sql
-- All active or monitored supply chain disruptions
SELECT 
    EventName,
    DisruptionType,
    Severity,
    AlertLevel,
    Status,
    GeographicArea,
    StartDate,
    DeliveryDelay,
    CostIncrease,
    EstimatedRevenueImpact
FROM supplychain.SupplyChainEvents
WHERE Status IN ('Active', 'Monitoring')
ORDER BY 
    CASE Severity 
        WHEN 'Critical' THEN 1 
        WHEN 'High' THEN 2 
        WHEN 'Medium' THEN 3 
        ELSE 4 
    END
```

#### Product Sourcing Details
```sql
-- Supplier options per product with costs and lead times
SELECT 
    ps.ProductName,
    ps.ProductCategory,
    ps.SupplierName,
    s.SupplierType,
    ps.WholesaleCost,
    ps.MinOrderQuantity,
    ps.LeadTimeDays,
    s.ReliabilityScore,
    ps.Status
FROM supplychain.ProductSuppliers ps
JOIN supplychain.Suppliers s ON ps.SupplierID = s.SupplierID
WHERE ps.Status = 'Active'
ORDER BY ps.ProductCategory, ps.ProductName, s.SupplierType
```

---

## Cross-Domain Analytics

### Customer Revenue Analysis
```sql
-- Total revenue and order count by customer relationship tier
SELECT 
    c.CustomerRelationshipTypeId,
    c.CustomerTypeId,
    COUNT(DISTINCT c.CustomerId) AS CustomerCount,
    COUNT(DISTINCT o.OrderId) AS OrderCount,
    ROUND(SUM(o.OrderTotal), 2) AS TotalRevenue,
    ROUND(AVG(o.OrderTotal), 2) AS AvgOrderValue,
    ROUND(SUM(o.OrderTotal) / COUNT(DISTINCT c.CustomerId), 2) AS RevenuePerCustomer
FROM customer.Customer c
JOIN sales.Order o ON c.CustomerId = o.CustomerId
WHERE c.IsActive = true
  AND o.OrderStatus = 'Completed'
GROUP BY c.CustomerRelationshipTypeId, c.CustomerTypeId
ORDER BY TotalRevenue DESC
```

### Product Sales and Margin Analysis
```sql
-- Product revenue and margin from sales + product cost data
SELECT 
    p.CategoryName,
    p.ProductName,
    SUM(ol.Quantity) AS TotalUnitsSold,
    ROUND(SUM(ol.LineTotal), 2) AS TotalRevenue,
    ROUND(SUM(ol.Quantity * p.StandardCost), 2) AS TotalCost,
    ROUND(SUM(ol.LineTotal) - SUM(ol.Quantity * p.StandardCost), 2) AS GrossProfit,
    ROUND(
        (SUM(ol.LineTotal) - SUM(ol.Quantity * p.StandardCost)) * 100.0 / SUM(ol.LineTotal),
        2
    ) AS MarginPct
FROM product.Product p
JOIN sales.OrderLine ol ON p.ProductID = ol.ProductId
JOIN sales.Order o ON ol.OrderId = o.OrderId
WHERE o.OrderStatus = 'Completed'
  AND ol.LineTotal > 0
GROUP BY p.CategoryName, p.ProductName
ORDER BY GrossProfit DESC
LIMIT 20
```

### Sales to Finance Reconciliation
```sql
-- Match orders to invoices to confirm financial completeness
SELECT 
    o.OrderNumber,
    o.OrderDate,
    o.OrderTotal AS SalesOrderTotal,
    i.TotalAmount AS InvoicedAmount,
    i.InvoiceStatus,
    p.PaymentAmount,
    p.PaymentStatus
FROM sales.Order o
LEFT JOIN finance.invoice i ON o.OrderId = i.OrderId
LEFT JOIN finance.payment p ON i.InvoiceId = p.InvoiceId
WHERE o.OrderStatus = 'Completed'
ORDER BY o.OrderDate DESC
LIMIT 50
```

### Inventory vs Sales Demand
```sql
-- Compare current stock levels against recent sales velocity
SELECT 
    inv.ProductName,
    inv.ProductCategory,
    inv.WarehouseLocation,
    inv.CurrentStock,
    inv.ReorderPoint,
    inv.Status,
    COALESCE(recent.RecentUnitsSold, 0) AS UnitsLast30Days
FROM inventory.Inventory inv
LEFT JOIN (
    SELECT 
        ol.ProductName,
        SUM(ol.Quantity) AS RecentUnitsSold
    FROM sales.OrderLine ol
    JOIN sales.Order o ON ol.OrderId = o.OrderId
    WHERE o.OrderDate >= DATE_SUB(CURRENT_DATE(), 30)
      AND o.OrderStatus = 'Completed'
    GROUP BY ol.ProductName
) recent ON inv.ProductName = recent.ProductName
ORDER BY inv.ProductCategory, inv.CurrentStock ASC
```

---

## Data Access Best Practices

### 1. NULL Value Handling

Always account for nullable fields to avoid unexpected results:

```sql
-- Safe age calculation
SELECT 
    CustomerId,
    CASE 
        WHEN DateOfBirth IS NOT NULL 
        THEN ROUND(DATEDIFF(CURRENT_DATE(), DateOfBirth) / 365.0, 1)
        ELSE NULL 
    END AS AgeYears
FROM customer.Customer

-- Safe aggregation with optional fields
SELECT 
    COUNT(*) AS TotalCustomers,
    COUNT(SecondaryPhone) AS WithSecondaryPhone,
    COUNT(SecondaryEmail) AS WithSecondaryEmail
FROM customer.Customer

-- Replace NULL balance with 0 for summing
SELECT AccountType, ROUND(SUM(COALESCE(Balance, 0)), 2) AS TotalBalance
FROM finance.account
GROUP BY AccountType
```

---

### 2. Join Best Practices

```sql
-- Use INNER JOIN when the related record must exist
SELECT c.FirstName, c.LastName, o.OrderTotal
FROM customer.Customer c
INNER JOIN sales.Order o ON c.CustomerId = o.CustomerId
WHERE o.OrderStatus = 'Completed'

-- Use LEFT JOIN to include customers with no orders
SELECT c.FirstName, c.LastName, COUNT(o.OrderId) AS OrderCount
FROM customer.Customer c
LEFT JOIN sales.Order o ON c.CustomerId = o.CustomerId
    AND o.OrderStatus = 'Completed'
WHERE c.IsActive = true
GROUP BY c.FirstName, c.LastName
ORDER BY OrderCount DESC
```

---

### 3. Date Range Filtering

```sql
-- Specific date range (preferred for performance)
SELECT * FROM sales.Order
WHERE OrderDate >= '2025-01-01'
  AND OrderDate < '2026-01-01'
  AND OrderStatus = 'Completed'

-- Year-over-year comparison
SELECT 
    YEAR(OrderDate) AS OrderYear,
    ROUND(SUM(OrderTotal), 2) AS AnnualRevenue,
    COUNT(*) AS OrderCount
FROM sales.Order
WHERE OrderStatus = 'Completed'
GROUP BY YEAR(OrderDate)
ORDER BY OrderYear
```

---

### 4. Seasonal Analysis Template

```sql
-- Sales by season
SELECT 
    CASE 
        WHEN MONTH(OrderDate) IN (12, 1, 2) THEN 'Winter'
        WHEN MONTH(OrderDate) IN (3, 4, 5) THEN 'Spring'
        WHEN MONTH(OrderDate) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Fall'
    END AS Season,
    COUNT(*) AS OrderCount,
    ROUND(SUM(OrderTotal), 2) AS SeasonalRevenue,
    ROUND(AVG(OrderTotal), 2) AS AvgOrderValue
FROM sales.Order
WHERE OrderStatus = 'Completed'
GROUP BY 
    CASE 
        WHEN MONTH(OrderDate) IN (12, 1, 2) THEN 'Winter'
        WHEN MONTH(OrderDate) IN (3, 4, 5) THEN 'Spring'
        WHEN MONTH(OrderDate) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Fall'
    END
ORDER BY SeasonalRevenue DESC
```

---

## Common Query Templates

### Top N Analysis
```sql
SELECT 
    {dimension_field},
    COUNT(*) AS Frequency,
    ROUND(SUM({metric_field}), 2) AS Total,
    ROUND(AVG({metric_field}), 2) AS Average
FROM {schema}.{table}
WHERE {filter_conditions}
GROUP BY {dimension_field}
ORDER BY Total DESC
LIMIT {n}
```

### Time Series Aggregation
```sql
SELECT 
    YEAR({date_field}) AS Year,
    MONTH({date_field}) AS Month,
    COUNT(*) AS RecordCount,
    ROUND(SUM({amount_field}), 2) AS TotalAmount,
    ROUND(AVG({amount_field}), 2) AS AvgAmount
FROM {schema}.{table}
WHERE {date_field} >= '{start_date}'
  AND {optional_filter}
GROUP BY YEAR({date_field}), MONTH({date_field})
ORDER BY Year, Month
```

### Customer Segmentation Template
```sql
SELECT 
    {segmentation_field},
    COUNT(*) AS CustomerCount,
    SUM(CASE WHEN IsActive = true THEN 1 ELSE 0 END) AS ActiveCount,
    ROUND(SUM(CASE WHEN IsActive = true THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS ActivePct
FROM customer.Customer
GROUP BY {segmentation_field}
ORDER BY CustomerCount DESC
```

---

## Error Prevention Guidelines

### Common Pitfalls to Avoid

- **Division by zero**: Always check denominators — use `NULLIF(denominator, 0)` or `CASE WHEN`
- **String case sensitivity**: Use `UPPER()` or `LOWER()` for consistent comparisons on free-text fields
- **Finance table casing**: `finance.invoice`, `finance.account`, `finance.payment` are all lowercase
- **Status value casing**: Use exact casing — `'Completed'`, `'Active'`, `'Primary'` (title case)
- **Boolean comparisons**: Use `true` / `false` not `'True'` / `'False'`
- **Aggregation without GROUP BY**: Ensure all non-aggregated SELECT columns are in the GROUP BY

### Data Validation Checks

Before running complex analyses, validate data availability:

```sql
-- Check row counts across key tables
SELECT 'customer.Customer' AS TableName, COUNT(*) AS RowCount FROM customer.Customer
UNION ALL
SELECT 'sales.Order', COUNT(*) FROM sales.Order
UNION ALL
SELECT 'sales.OrderLine', COUNT(*) FROM sales.OrderLine
UNION ALL
SELECT 'finance.invoice', COUNT(*) FROM finance.invoice
UNION ALL
SELECT 'inventory.Inventory', COUNT(*) FROM inventory.Inventory
UNION ALL
SELECT 'supplychain.Suppliers', COUNT(*) FROM supplychain.Suppliers

-- Verify customer-to-order referential integrity
SELECT o.CustomerId, COUNT(*) AS OrphanOrders
FROM sales.Order o
LEFT JOIN customer.Customer c ON o.CustomerId = c.CustomerId
WHERE c.CustomerId IS NULL
GROUP BY o.CustomerId
```

---

## Business Context Guidelines

### Always Provide Business Meaning

When writing queries for users, comment the business intent:

```sql
-- Business Question: Which customer segments generate the highest revenue?
-- Helps prioritize marketing efforts and service resource allocation
SELECT 
    c.CustomerRelationshipTypeId AS Segment,
    COUNT(DISTINCT c.CustomerId) AS CustomerCount,
    ROUND(SUM(o.OrderTotal), 2) AS TotalRevenue,
    ROUND(SUM(o.OrderTotal) / COUNT(DISTINCT c.CustomerId), 2) AS RevenuePerCustomer
FROM customer.Customer c
JOIN sales.Order o ON c.CustomerId = o.CustomerId
WHERE c.IsActive = true
  AND o.OrderStatus = 'Completed'
GROUP BY c.CustomerRelationshipTypeId
ORDER BY TotalRevenue DESC
```

### Data Freshness Reference

| Domain | Update Frequency |
|--------|------------------|
| Customer | Daily batch |
| Product | Weekly batch |
| Sales (Orders) | Batch loaded |
| Finance (Invoices/Payments) | Batch loaded |
| Inventory | Batch loaded |
| Supply Chain | Batch loaded |

All data in this lakehouse is synthetically generated batch data. There is no real-time or streaming data in this environment.
