# Sample Agent Questions - Product, Inventory & Supply Chain Ontology

## Overview

This document provides sample questions that demonstrate the capabilities of the Fabric Data Agent using the ontology graph model built on **Product**, **Inventory**, and **Supply Chain** schemas. The agent can answer complex business questions by traversing relationships between entities across these three interconnected domains.

## Common Data Source Issues

If you experience problems, below are commonly root causes: 

1. **Connection Problem**: The system or query interface may not be connected to the Microsoft Fabric Ontology Graph Model or Lakehouse. This means the tool cannot reach or access your data at all.
2. **Permission or Access Error**: My environment might not have the required permissions to query the database or underlying data lake. Role or credential issues are a frequent cause.
3. **Backend System Outage**: The Fabric Lakehouse, related databases, or query engines could be down for maintenance or experiencing outages.
4. **Configuration Issues**: The data source, endpoints, or connection strings may be misconfigured, preventing queries from running.
5. **Data Not Loaded**: The necessary business data (products, orders, suppliers, etc.) may not be imported or synced in the underlying system yet.
6. **Query Timeout or Failure**: Some tools have query execution limits; infrastructure issues or inefficient queries can cause failures.



## Available Business Domains

### 🏷️ Product Schema (2 tables)
- **Product**: Product catalog with specifications, pricing, and categorization
- **ProductCategory**: Hierarchical product categories (Camping, Kitchen, Ski)

### 📦 Inventory Schema (6 tables)  
- **Warehouses**: Warehouse locations and operational details
- **Inventory**: Current stock levels by product and warehouse
- **InventoryTransactions**: Stock movement audit trail
- **PurchaseOrders**: Procurement order headers
- **PurchaseOrderItems**: Purchase order line items
- **DemandForecast**: Predictive demand planning

### 🚚 Supply Chain Schema (3 tables)
- **Suppliers**: Supplier master data with backup relationships
- **ProductSuppliers**: Product-supplier mapping with pricing
- **SupplyChainEvents**: Disruption events and impact tracking

---

## Sample Agent Questions

### 📊 Product Analysis Questions

#### Basic Product Queries
- "How many products do we have in each category?"
- "What's the average list price for camping products?"
- "Show me all ski products with their standard costs"
- "Which products have the highest markup (difference between list price and standard cost)?"
- "List all products that are currently discontinued"

#### Product Category Analysis
- "What's the price distribution across our three main categories: Camping, Kitchen, and Ski?"
- "Which product category has the most expensive average pricing?"
- "Show me the product count and total value for each brand in the camping category"
- "What's the weight distribution of products in the kitchen category?"

#### Product Lifecycle Analysis
- "Which products were launched in the last 6 months?"
- "Show me products that are approaching their end-of-sale date"
- "What percentage of our product catalog is currently active?"

---

### 📦 Inventory Management Questions

#### Stock Level Analysis
- "Which products are currently below their reorder point?"
- "Show me the top 10 products by current stock value"
- "What's our total inventory value across all warehouses?"
- "Which warehouse has the highest inventory turnover?"
- "List products with safety stock levels below 10 units"

#### Warehouse Performance
- "How is our inventory distributed across warehouses?"
- "Which warehouse has the highest utilization rate?"
- "Show me warehouse capacity and current usage by location"
- "What's the average inventory value per warehouse?"
- "Which warehouses are operating at or near capacity?"

#### Stock Movement Analysis
- "What were the top 5 inventory transactions by value last month?"
- "Show me products with the most frequent stock adjustments"
- "Which transaction types are most common in our inventory system?"
- "What's the trend in inventory receipts vs. sales over the last quarter?"

#### Purchase Order Insights
- "Which suppliers have the most purchase orders in progress?"
- "Show me overdue purchase orders and their impact on inventory"
- "What's our average purchase order fulfillment time?"
- "Which products have the most pending purchase order items?"
- "What's the total value of purchase orders by delivery warehouse?"

#### Demand Forecasting
- "Which products have the highest predicted demand next month?"
- "Show me forecast accuracy for camping products over the last quarter"
- "Which products show growing vs. declining demand trends?"
- "What's our confidence level on forecasts for ski products?"

---

### 🚚 Supply Chain Intelligence

#### Supplier Performance
- "Which suppliers have the best reliability scores?"
- "Show me suppliers by product category and their lead times"
- "Which backup suppliers are available for our main camping gear supplier?"
- "What's the average wholesale cost by supplier for kitchen products?"
- "List suppliers with active disruption events affecting them"

#### Product-Supplier Relationships  
- "Which products have multiple supplier options?"
- "Show me products with only single-source suppliers (risk analysis)"
- "What's the cost variance between primary and backup suppliers?"
- "Which suppliers offer the broadest product range?"
- "List products with the shortest supplier lead times"

#### Disruption Impact Analysis
- "What active supply chain events are affecting our operations?"
- "Which suppliers are impacted by current weather disruptions?"
- "Show me products with availability issues due to supply chain events"
- "What's the estimated financial impact of active disruptions?"
- "Which geographic areas have the most supply chain risks?"

---

### 🔄 Cross-Schema Integration Questions

#### Product-to-Inventory Integration
- "Which high-value products are running low in stock?"
- "Show me inventory levels for our top 10 best-selling product categories"
- "What's the inventory turnover rate for camping vs. kitchen vs. ski products?"
- "Which discontinued products still have significant inventory?"
- "Show me products where current stock exceeds 3 months of forecasted demand"

#### Inventory-to-Supply Chain Integration
- "Which suppliers should we contact for products below reorder point?"
- "Show me purchase orders from suppliers currently experiencing disruptions"
- "What's the impact of supply chain delays on our inventory planning?"
- "Which warehouses are expecting deliveries from high-risk suppliers?"
- "How do supplier lead times affect our safety stock calculations?"

#### End-to-End Supply Chain Visibility
- "Trace the supply chain path for a specific product from supplier to warehouse"
- "Which products are most vulnerable to supply disruptions (single supplier + low stock)?"
- "Show me the complete supply chain status for camping products"
- "What's the cascading impact if our main supplier for kitchen products goes down?"
- "Which product categories have the most resilient supply chains?"

#### Financial Impact Analysis
- "What's the cost impact if we switch to backup suppliers for disrupted products?"
- "Show me inventory carrying costs by product category and warehouse"
- "How do supplier price increases affect our product profitability?"
- "What's the financial exposure of products with supply chain risks?"

#### Operations Planning
- "Which products need immediate reordering based on current inventory and supplier lead times?"
- "Show me the optimal warehouse allocation for incoming purchase orders"
- "What's our demand vs. supply balance for the next 3 months?"
- "Which suppliers should we prioritize for relationship strengthening?"

---

### 🎯 Strategic Business Questions

#### Risk Management
- "Identify our top 5 supply chain vulnerabilities"
- "Which products have backup supplier coverage?"
- "Show me geographic concentration risks in our supplier base"
- "What's our inventory buffer against supply disruptions?"

#### Optimization Opportunities  
- "Which slow-moving products are tying up warehouse space?"
- "Show me opportunities to consolidate suppliers for better terms"
- "Which products could benefit from demand forecast accuracy improvements?"
- "Where can we optimize safety stock levels without increasing risk?"

#### Performance Benchmarking
- "Compare inventory turnover rates across product categories"
- "Show supplier performance rankings by reliability and cost"
- "What's our forecast accuracy vs. industry benchmarks?"
- "How does our warehouse utilization compare to capacity planning goals?"

---

## Query Complexity Examples

### Simple Single-Schema Queries
- Basic counts, sums, and filters within one domain
- Example: "How many camping products are currently active?"

### Medium Cross-Schema Queries  
- Queries spanning 2 schemas with straightforward joins
- Example: "Show inventory levels for all ski products"

### Complex Multi-Schema Analytics
- Advanced queries requiring multiple joins and business logic
- Example: "Which products are at risk of stockout considering current inventory, supplier lead times, and active disruptions?"

### Strategic Decision Support
- Executive-level questions requiring comprehensive analysis
- Example: "What's our overall supply chain resilience score and top 3 improvement opportunities?"

---

## Expected Agent Capabilities

The agent should be able to:
- ✅ Navigate relationships between Product ↔ Inventory ↔ Supply Chain
- ✅ Aggregate data across multiple warehouses and suppliers 
- ✅ Calculate derived metrics (turnover, utilization, risk scores)
- ✅ Provide time-series analysis and trend identification
- ✅ Offer proactive insights and recommendations
- ✅ Handle both operational and strategic business questions
- ✅ Explain complex supply chain relationships in business terms