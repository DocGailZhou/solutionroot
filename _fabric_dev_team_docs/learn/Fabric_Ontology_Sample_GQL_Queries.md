# Fabric Ontology GQL Sample Queries

This document provides Graph Query Language (GQL) sample queries for your Fabric Ontology. These queries leverage the graph relationships between Product, Inventory, and Supply Chain nodes to answer business questions using graph traversal patterns.
## ⚡ **Simple Queries for Quick Start** 

**Important**: Fabric Ontology is in preview and may have performance limitations. The queries in this section are optimized for reliability and speed.

### **Query 1: List Products by Category** (Safe, Fast)
```gql
MATCH (product:Product)
WHERE product.category = 'Camping'
RETURN product.name, product.price
LIMIT 10
```
**Why it's fast**: Single node query, simple property filter, limited results.

### **Query 2: Check Inventory Levels** (Safe, Fast)  
```gql
MATCH (inventory:Inventory)
WHERE inventory.currentStock < inventory.reorderPoint
RETURN inventory.productID, inventory.currentStock, inventory.reorderPoint
LIMIT 5
```
**Why it's fast**: Single node query, simple comparison, small result set.

### **Query 3: Simple Supplier List** (Safe, Fast)
```gql
MATCH (supplier:Supplier)
WHERE supplier.leadTimeDays < 15
RETURN supplier.name, supplier.leadTimeDays, supplier.contactInfo
LIMIT 8
```
**Why it's fast**: Single node query, no complex relationships.

### **Query 4: Basic Product-Inventory Join** (Safe, 2-Table Join Only)
```gql
MATCH (product:Product)-[:STOCKED_IN]->(inventory:Inventory)
WHERE product.category = 'Kitchen' 
AND inventory.currentStock > 0
RETURN product.name, inventory.currentStock
LIMIT 10
```
**Why it's safe**: Simple 1-hop relationship, filtered results.

### **Query 5: Recent Purchase Orders** (Safe, Date Limited)
```gql
MATCH (po:PurchaseOrder)
WHERE po.orderDate >= date('2026-03-01')
RETURN po.purchaseOrderID, po.supplierName, po.orderDate
LIMIT 10
```
**Why it's fast**: Single table, recent data only, limited results.

### **⚠️ Performance Guidelines for Preview**
- **Always use LIMIT**: Never run queries without LIMIT (use 5-20 max)
- **Avoid deep traversals**: Stick to 1-2 hops maximum
- **Filter early**: Use WHERE clauses to reduce data early
- **Avoid aggregations**: Skip COUNT, SUM, AVG in complex queries
- **Use specific dates**: Include date ranges to limit data scope
- **Test incrementally**: Start with LIMIT 1, then increase

---
## Graph Model Overview

Your ontology contains these primary node types and relationships:

```
(Product)-[:BELONGS_TO]->(ProductCategory)
(Product)-[:STOCKED_IN]->(Inventory)-[:LOCATED_AT]->(Warehouse)
(Product)-[:SUPPLIED_BY]->(Supplier)
(Supplier)-[:PROVIDES]->(Product)-[:HAS_FORECAST]->(DemandForecast)
(PurchaseOrder)-[:ORDERS]->(Product)
(InventoryTransaction)-[:AFFECTS]->(Inventory)
```

---

## Basic Graph Navigation Queries

### 1. Product Category Exploration
**Business Question**: "Show me all camping products and their warehouse locations"

```gql
MATCH (category:ProductCategory {name: 'Camping'})
      <-[:BELONGS_TO]-(product:Product)
      -[:STOCKED_IN]->(inventory:Inventory)
      -[:LOCATED_AT]->(warehouse:Warehouse)
WHERE inventory.currentStock > 0
RETURN product.name, 
       inventory.currentStock, 
       warehouse.name,
       warehouse.location
ORDER BY product.name, warehouse.name
```

### 2. Multi-Hop Supplier Network
**Business Question**: "Find all products that Kitchen Pro Ltd supplies and their current stock levels"

```gql
MATCH (supplier:Supplier {name: 'Kitchen Pro Ltd'})
      -[:SUPPLIES]->(product:Product)
      -[:STOCKED_IN]->(inventory:Inventory)
      -[:LOCATED_AT]->(warehouse:Warehouse)
RETURN supplier.name,
       product.name,
       product.category,
       inventory.currentStock,
       inventory.reorderPoint,
       warehouse.name
ORDER BY inventory.currentStock
```

---

## Path-Based Analysis Queries

### 3. Supply Chain Path Analysis
**Business Question**: "Trace the complete supply chain path for a specific product"

```gql
MATCH path = (supplier:Supplier)
             -[:SUPPLIES]->(product:Product {productID: 'CAMP_TENT_001'})
             -[:STOCKED_IN]->(inventory:Inventory)
             -[:LOCATED_AT]->(warehouse:Warehouse)
OPTIONAL MATCH (product)-[:HAS_FORECAST]->(forecast:DemandForecast)
OPTIONAL MATCH (po:PurchaseOrder)-[:ORDERS]->(product)
WHERE po.orderDate >= date('2026-01-01')
RETURN path,
       supplier.name AS supplierName,
       supplier.leadTimeDays,
       inventory.currentStock,
       warehouse.location,
       forecast.predictedDemand,
       po.orderDate AS recentOrderDate
```

### 4. Cross-Category Supplier Discovery
**Business Question**: "Which suppliers provide products across multiple categories?"

```gql
MATCH (supplier:Supplier)-[:SUPPLIES]->(product:Product)
      -[:BELONGS_TO]->(category:ProductCategory)
WITH supplier, COLLECT(DISTINCT category.name) AS categories
WHERE SIZE(categories) > 1
MATCH (supplier)-[:SUPPLIES]->(product:Product)
RETURN supplier.name,
       supplier.contactInfo,
       categories,
       COUNT(product) AS totalProducts
ORDER BY SIZE(categories) DESC, totalProducts DESC
```

---

## Aggregation and Analytics Queries

### 5. Warehouse Performance Analysis
**Business Question**: "Compare inventory performance across warehouses"

```gql
MATCH (warehouse:Warehouse)<-[:LOCATED_AT]-(inventory:Inventory)
      <-[:STOCKED_IN]-(product:Product)
WITH warehouse,
     SUM(inventory.currentStock) AS totalStock,
     COUNT(DISTINCT product) AS productVariety,
     AVG(inventory.currentStock) AS avgStockPerProduct,
     COUNT(CASE WHEN inventory.currentStock < inventory.reorderPoint THEN 1 END) AS lowStockItems
RETURN warehouse.name,
       warehouse.location,
       totalStock,
       productVariety,
       avgStockPerProduct,
       lowStockItems,
       ROUND(100.0 * lowStockItems / productVariety) AS lowStockPercentage
ORDER BY lowStockPercentage, totalStock DESC
```

### 6. Supplier Risk Assessment
**Business Question**: "Identify suppliers with high-risk dependency patterns"

```gql
MATCH (supplier:Supplier)-[:SUPPLIES]->(product:Product)
      -[:STOCKED_IN]->(inventory:Inventory)
WITH supplier,
     COUNT(DISTINCT product) AS productCount,
     SUM(inventory.currentStock) AS totalInventoryValue,
     AVG(supplier.leadTimeDays) AS avgLeadTime
OPTIONAL MATCH (supplier)<-[:AFFECTED_BY]-(event:SupplyChainEvent)
WHERE event.eventDate >= date('2026-01-01')
WITH supplier, productCount, totalInventoryValue, avgLeadTime,
     COUNT(event) AS recentEvents,
     MAX(event.severityLevel) AS maxSeverity
RETURN supplier.name,
       productCount,
       totalInventoryValue,
       avgLeadTime,
       recentEvents,
       maxSeverity,
       CASE 
         WHEN recentEvents > 2 AND maxSeverity = 'Critical' THEN 'HIGH RISK'
         WHEN recentEvents > 1 OR avgLeadTime > 20 THEN 'MEDIUM RISK'
         ELSE 'LOW RISK'
       END AS riskLevel
ORDER BY 
  CASE riskLevel WHEN 'HIGH RISK' THEN 1 WHEN 'MEDIUM RISK' THEN 2 ELSE 3 END,
  recentEvents DESC
```

---

## Pattern Matching Queries

### 7. Circular Dependency Detection
**Business Question**: "Find products that might create supply chain circular dependencies"

```gql
MATCH (product1:Product)-[:SUPPLIED_BY]->(supplier:Supplier)
      -[:SUPPLIES]->(product2:Product)
WHERE product1 <> product2
AND product1.category = product2.category
MATCH (product2)-[:STOCKED_IN]->(inventory1:Inventory),
      (product1)-[:STOCKED_IN]->(inventory2:Inventory)
WHERE inventory1.warehouseLocation = inventory2.warehouseLocation
RETURN product1.name AS sourceProduct,
       product2.name AS suppliedProduct,
       supplier.name,
       product1.category,
       inventory1.warehouseLocation
```

### 8. Alternative Sourcing Paths
**Business Question**: "Find alternative suppliers for products currently facing supply issues"

```gql
MATCH (event:SupplyChainEvent {severityLevel: 'Critical'})
      -[:AFFECTS]->(supplier:Supplier)
      -[:SUPPLIES]->(product:Product)
MATCH (product)-[:SUPPLIED_BY]->(altSupplier:Supplier)
WHERE altSupplier <> supplier
AND NOT (event)-[:AFFECTS]->(altSupplier)
RETURN product.name,
       product.category,
       supplier.name AS affectedSupplier,
       altSupplier.name AS alternativeSupplier,
       altSupplier.leadTimeDays,
       event.description AS issue
ORDER BY product.category, altSupplier.leadTimeDays
```

---

## Temporal and Forecasting Queries

### 9. Demand-Supply Gap Analysis
**Business Question**: "Compare forecasted demand with current inventory and supplier capacity"

```gql
MATCH (product:Product)-[:HAS_FORECAST]->(forecast:DemandForecast)
WHERE forecast.forecastDate >= date('2026-04-01') 
AND forecast.forecastDate <= date('2026-06-30')
MATCH (product)-[:STOCKED_IN]->(inventory:Inventory)
MATCH (product)-[:SUPPLIED_BY]->(supplier:Supplier)
WITH product,
     SUM(forecast.predictedDemand) AS totalForecastedDemand,
     SUM(inventory.currentStock) AS totalCurrentStock,
     MIN(supplier.leadTimeDays) AS shortestLeadTime
WHERE totalForecastedDemand > totalCurrentStock
RETURN product.name,
       product.category,
       totalForecastedDemand,
       totalCurrentStock,
       (totalForecastedDemand - totalCurrentStock) AS shortfall,
       shortestLeadTime,
       CASE 
         WHEN shortestLeadTime > 30 THEN 'HIGH URGENCY'
         WHEN shortestLeadTime > 14 THEN 'MEDIUM URGENCY'
         ELSE 'LOW URGENCY'
       END AS urgencyLevel
ORDER BY shortfall DESC, shortestLeadTime DESC
```

### 10. Purchase Order Optimization
**Business Question**: "Optimize purchase orders based on supplier efficiency and inventory needs"

```gql
MATCH (product:Product)-[:STOCKED_IN]->(inventory:Inventory)
WHERE inventory.currentStock < inventory.reorderPoint
MATCH (product)-[:SUPPLIED_BY]->(supplier:Supplier)
OPTIONAL MATCH (supplier)-[:FULFILLED]->(po:PurchaseOrder)
WHERE po.orderDate >= date('2026-01-01')
WITH product, inventory, supplier,
     AVG(po.fulfillmentDays) AS avgFulfillmentDays,
     COUNT(po) AS orderHistory
WHERE orderHistory IS NULL OR avgFulfillmentDays IS NOT NULL
WITH product, inventory, supplier,
     COALESCE(avgFulfillmentDays, supplier.leadTimeDays) AS effectiveLeadTime,
     (inventory.reorderPoint - inventory.currentStock) AS unitsNeeded
RETURN product.name,
       inventory.warehouseLocation,
       supplier.name,
       unitsNeeded,
       effectiveLeadTime,
       supplier.contactInfo,
       ROUND(unitsNeeded * effectiveLeadTime / 30.0) AS priorityScore
ORDER BY priorityScore DESC
```

---

## Business Intelligence Dashboard Queries

### 11. Executive Supply Chain Summary
**Business Question**: "Provide executive dashboard metrics across the supply chain"

```gql
MATCH (product:Product)-[:STOCKED_IN]->(inventory:Inventory)
      -[:LOCATED_AT]->(warehouse:Warehouse)
WITH COUNT(DISTINCT product) AS totalProducts,
     COUNT(DISTINCT warehouse) AS totalWarehouses,
     SUM(inventory.currentStock) AS totalInventoryUnits,
     COUNT(CASE WHEN inventory.currentStock < inventory.reorderPoint THEN 1 END) AS lowStockItems

MATCH (supplier:Supplier)-[:SUPPLIES]->(product:Product)
WITH totalProducts, totalWarehouses, totalInventoryUnits, lowStockItems,
     COUNT(DISTINCT supplier) AS totalSuppliers,
     AVG(supplier.leadTimeDays) AS avgLeadTime

OPTIONAL MATCH (event:SupplyChainEvent)
WHERE event.eventDate >= date('2026-03-01')
WITH totalProducts, totalWarehouses, totalInventoryUnits, lowStockItems,
     totalSuppliers, avgLeadTime,
     COUNT(event) AS recentEvents,
     COUNT(CASE WHEN event.severityLevel IN ['High', 'Critical'] THEN 1 END) AS criticalEvents

RETURN {
  inventory: {
    totalProducts: totalProducts,
    totalWarehouses: totalWarehouses,
    totalInventoryUnits: totalInventoryUnits,
    lowStockItems: lowStockItems,
    stockHealthPercentage: ROUND(100.0 * (totalProducts - lowStockItems) / totalProducts)
  },
  suppliers: {
    totalSuppliers: totalSuppliers,
    avgLeadTime: ROUND(avgLeadTime, 1)
  },
  risks: {
    recentEvents: recentEvents,
    criticalEvents: criticalEvents,
    riskLevel: CASE 
      WHEN criticalEvents > 5 THEN 'HIGH'
      WHEN criticalEvents > 2 THEN 'MEDIUM'
      ELSE 'LOW'
    END
  }
} AS dashboardMetrics
```

### 12. Category Performance Comparison
**Business Question**: "Compare performance metrics across product categories"

```gql
MATCH (category:ProductCategory)<-[:BELONGS_TO]-(product:Product)
      -[:STOCKED_IN]->(inventory:Inventory)
OPTIONAL MATCH (product)-[:SUPPLIED_BY]->(supplier:Supplier)
WITH category,
     COUNT(DISTINCT product) AS productCount,
     SUM(inventory.currentStock) AS totalStock,
     AVG(inventory.currentStock) AS avgStock,
     COUNT(DISTINCT supplier) AS supplierCount,
     AVG(supplier.leadTimeDays) AS avgLeadTime,
     COUNT(CASE WHEN inventory.currentStock < inventory.reorderPoint THEN 1 END) AS lowStockCount
RETURN category.name,
       productCount,
       totalStock,
       ROUND(avgStock, 2) AS avgStock,
       supplierCount,
       ROUND(avgLeadTime, 1) AS avgLeadTime,
       lowStockCount,
       ROUND(100.0 * lowStockCount / productCount) AS lowStockPercentage,
       ROUND(totalStock / supplierCount) AS stockPerSupplier
ORDER BY lowStockPercentage, avgLeadTime
```

---

## Advanced Pattern Analysis

### 13. Hub Detection (Critical Suppliers)
**Business Question**: "Identify suppliers that are critical hubs in the supply network"

```gql
MATCH (supplier:Supplier)-[:SUPPLIES]->(product:Product)
      -[:BELONGS_TO]->(category:ProductCategory)
WITH supplier,
     COUNT(DISTINCT product) AS productCount,
     COUNT(DISTINCT category) AS categoryCount,
     COLLECT(DISTINCT category.name) AS categories
MATCH (supplier)-[:SUPPLIES]->(product:Product)
      -[:STOCKED_IN]->(inventory:Inventory)
WITH supplier, productCount, categoryCount, categories,
     SUM(inventory.currentStock * product.price) AS inventoryValue
WHERE productCount > 5 OR categoryCount > 2
RETURN supplier.name,
       supplier.contactInfo,
       productCount,
       categoryCount,
       categories,
       ROUND(inventoryValue, 2) AS totalInventoryValue,
       CASE 
         WHEN categoryCount > 2 AND productCount > 10 THEN 'CRITICAL HUB'
         WHEN categoryCount > 1 OR productCount > 8 THEN 'IMPORTANT HUB'
         ELSE 'STANDARD SUPPLIER'
       END AS hubStatus
ORDER BY categoryCount DESC, productCount DESC
```

### 14. Bottleneck Analysis
**Business Question**: "Find potential bottlenecks in the supply chain"

```gql
MATCH (product:Product)-[:SUPPLIED_BY]->(supplier:Supplier)
WHERE supplier.leadTimeDays > 20
MATCH (product)-[:STOCKED_IN]->(inventory:Inventory)
MATCH (product)-[:HAS_FORECAST]->(forecast:DemandForecast)
WHERE forecast.forecastDate >= date('2026-04-01')
WITH product, supplier,
     SUM(inventory.currentStock) AS totalStock,
     SUM(forecast.predictedDemand) AS totalDemand,
     MAX(supplier.leadTimeDays) AS maxLeadTime
WHERE totalDemand > totalStock
MATCH (product)-[:SUPPLIED_BY]->(altSupplier:Supplier)
WHERE altSupplier <> supplier
WITH product, supplier, totalStock, totalDemand, maxLeadTime,
     COUNT(altSupplier) AS alternativeSuppliers,
     MIN(altSupplier.leadTimeDays) AS bestAltLeadTime
RETURN product.name,
       product.category,
       supplier.name AS bottleneckSupplier,
       maxLeadTime,
       (totalDemand - totalStock) AS supplyGap,
       alternativeSuppliers,
       COALESCE(bestAltLeadTime, maxLeadTime) AS bestAltLeadTime,
       CASE 
         WHEN alternativeSuppliers = 0 THEN 'CRITICAL BOTTLENECK'
         WHEN alternativeSuppliers < 2 THEN 'HIGH RISK BOTTLENECK'
         ELSE 'MANAGEABLE BOTTLENECK'
       END AS bottleneckSeverity
ORDER BY 
  CASE bottleneckSeverity 
    WHEN 'CRITICAL BOTTLENECK' THEN 1 
    WHEN 'HIGH RISK BOTTLENECK' THEN 2 
    ELSE 3 
  END,
  supplyGap DESC
```

---

## Query Optimization Tips

### Performance Best Practices
1. **Use Labels**: Always specify node labels `(:Product)` rather than `(n)`
2. **Property Filtering**: Apply property filters early in MATCH clauses
3. **Limit Results**: Use `LIMIT` for large result sets in development
4. **Index Utilization**: Ensure indexes on frequently queried properties

### GQL Syntax Notes
- **Relationships**: Use `-[:RELATIONSHIP_TYPE]->` for directed relationships
- **Optional Matches**: Use `OPTIONAL MATCH` for nullable relationships
- **Path Variables**: Assign paths to variables for complex analysis
- **Aggregation**: Use `WITH` clauses to aggregate before further matching

### Business Logic Integration
- **Category Filtering**: Filter by product categories for domain-specific analysis
- **Time Windows**: Use date ranges for temporal analysis
- **Risk Assessment**: Implement business rules in `CASE` statements
- **Threshold Logic**: Apply reorder points and stock level business rules

These GQL queries demonstrate the power of graph thinking for supply chain analytics, allowing you to naturally express complex business relationships and traverse your data following real-world connections.