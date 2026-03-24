# Sample Agent Questions - Product, Inventory & Supply Chain Ontology

## Overview

This document provides sample questions that demonstrate the capabilities of the Fabric Data Agent using the ontology graph model built on **Product**, **Inventory**, and **Supply Chain** schemas. The agent can answer complex business questions by traversing relationships between entities across these three interconnected domains.

## Data Agent Instructions

The agent is configured to understand and query the following business domains:

### Business Domain Coverage
- 👥 **Democratization**: Non-technical users get enterprise-grade analytics
- 🔄 **Agility**: Business changes don't break existing queries



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

## How to Query Your Fabric Ontology

### Query Methods Available

#### 1. **Natural Language Queries (Recommended)**
Use Fabric's AI-powered query interface to ask questions in plain English:

```
"Show me all camping products with low inventory levels"
"Which suppliers have active disruption events?"
"What's the total inventory value by warehouse?"
```

#### 2. **Graph Query Language (GQL)**
For structured graph traversals:

```gql
MATCH (i:Inventory)-[:TracksProduct]->(p:Product)-[:BelongsToCategory]->(c:ProductCategory {CategoryName: 'Camping'})
WHERE i.CurrentStock < i.ReorderPoint
RETURN p.ProductName, i.CurrentStock, i.ReorderPoint
```

#### 3. **SPARQL Queries**
For semantic web-style queries:

```sparql
PREFIX ont: <http://fabric.ontology/>
SELECT ?productName ?stockLevel ?warehouse
WHERE {
  ?product ont:hasName ?productName ;
           ont:hasInventory ?inventory .
  ?inventory ont:currentStock ?stockLevel ;
             ont:locatedAt ?warehouse .
  FILTER (?stockLevel < 50)
}
```

#### 4. **Power BI Integration**
Connect Power BI to your ontology for visual analytics:
- Use the Fabric connector in Power BI Desktop
- Create relationships using ontology mappings
- Build dashboards with semantic layer intelligence

---

### Troubleshooting GQL Query Errors

#### Common Issues & Solutions

**1. Incorrect Relationship Names**
- ❌ `[:BELONGS_TO]` → ✅ `[:BelongsToCategory]` 
- ❌ `[:STORED_IN]` → ✅ `[:StoredAt]`
- ❌ `[:TRACKS_PRODUCT]` → ✅ `[:TracksProduct]`

**Your Actual Relationship Names:**
- `BelongsToCategory`: Product → ProductCategory
- `TracksProduct`: Inventory → Product  
- `StoredAt`: Inventory → Warehouses
- `OrderedFrom`: PurchaseOrders → Suppliers
- `Contains`: PurchaseOrders → PurchaseOrderItems
- `OrdersProduct`: PurchaseOrderItems → Product

**2. Wrong Relationship Direction**
- ❌ `(p:Product)-[:TracksProduct]->(i:Inventory)` 
- ✅ `(i:Inventory)-[:TracksProduct]->(p:Product)`

**3. Query Syntax Issues**
- Ensure proper spacing around relationship patterns
- Use correct node and property names
- Check parentheses and brackets are balanced

#### Testing Your Queries

**Start Simple:**
```gql
// Test basic node retrieval first
MATCH (p:Product) RETURN p LIMIT 5

// Then test relationships one by one  
MATCH (p:Product)-[:BelongsToCategory]->(c:ProductCategory) 
RETURN p.ProductName, c.CategoryName LIMIT 5
```

**Check Available Relationships:**
```gql
// See what relationships exist from Product nodes
MATCH (p:Product)-[r]->(n) 
RETURN type(r) as RelationshipType, labels(n) as ConnectedTo
LIMIT 20
```

---

### Example Queries for Your Ontology

#### Basic Entity Queries

**Get All Product Categories:**
```gql
MATCH (c:ProductCategory)
RETURN c.CategoryName, c.CategoryDescription
ORDER BY c.CategoryName
```

**Find Products by Category:**
```gql
MATCH (p:Product)-[:BelongsToCategory]->(c:ProductCategory {CategoryName: 'Camping'})
RETURN p.ProductName, p.ListPrice, p.StandardCost
ORDER BY p.ListPrice DESC
```

#### Cross-Domain Relationship Queries

**Products with Low Inventory:**
```gql
MATCH (i:Inventory)-[:TracksProduct]->(p:Product)
MATCH (i)-[:StoredAt]->(w:Warehouses)
WHERE i.CurrentStock < i.ReorderPoint
RETURN p.ProductName, p.ProductCategory, i.CurrentStock, 
       i.ReorderPoint, w.WarehouseName
ORDER BY i.CurrentStock ASC
```

**Supplier Risk Analysis:**
```gql
MATCH (s:Suppliers)-[:AFFECTED_BY]->(e:SupplyChainEvents)
-[:SUPPLIES]->(ps:ProductSuppliers)-[:FOR_PRODUCT]->(p:Product)
WHERE e.Status = 'Active' AND e.Severity IN ['High', 'Critical']
RETURN s.SupplierName, e.EventName, e.Severity,
       COUNT(p) as AffectedProductCount
ORDER BY AffectedProductCount DESC
```

#### Aggregation and Analytics

**Inventory Value by Warehouse:**
```gql
MATCH (w:Warehouses)<-[:StoredAt]-(i:Inventory)-[:TracksProduct]->(p:Product)
RETURN w.WarehouseName, 
       SUM(i.CurrentStock * p.StandardCost) as TotalValue,
       COUNT(i) as ProductCount
ORDER BY TotalValue DESC
```

**Purchase Order Analysis:**
```gql
MATCH (po:PurchaseOrders)-[:OrderedFrom]->(s:Suppliers)
MATCH (po)-[:Contains]->(poi:PurchaseOrderItems)-[:OrdersProduct]->(p:Product)
WHERE po.Status = 'Pending'
RETURN s.SupplierName, po.PurchaseOrderNumber, 
       SUM(poi.QuantityOrdered * poi.UnitCost) as OrderValue,
       po.ExpectedDeliveryDate
ORDER BY OrderValue DESC
```

#### Complex Business Intelligence

**Supply Chain Vulnerability Assessment:**
```gql
MATCH (p:Product)-[:SUPPLIED_BY]->(ps:ProductSuppliers)-[:FROM_SUPPLIER]->(s:Suppliers)
WHERE NOT EXISTS {
  MATCH (p)-[:SUPPLIED_BY]->(ps2:ProductSuppliers)-[:FROM_SUPPLIER]->(s2:Suppliers)
  WHERE s2.SupplierID <> s.SupplierID
}
WITH p, s
MATCH (p)-[:TRACKED_IN]->(i:Inventory)
WHERE i.CurrentStock < (i.ReorderPoint * 1.5)
RETURN p.ProductName, s.SupplierName, i.CurrentStock, 
       i.ReorderPoint, 'Single Source + Low Stock' as RiskType
ORDER BY i.CurrentStock ASC
```

---

### Accessing Your Ontology

#### Through Fabric Workspace
1. **Open Fabric Workspace** → Navigate to your `fabriciq_team_ontology.Ontology`
2. **Query Interface** → Use the built-in query editor
3. **Natural Language** → Type questions in the search/query box
4. **Graph Explorer** → Visual interface for browsing relationships

#### Programmatic Access
```python
# Python example using Fabric REST API
import requests

headers = {
    'Authorization': 'Bearer <your_token>',
    'Content-Type': 'application/json'
}

query = {
    "query": "MATCH (p:Product) WHERE p.ProductCategory = 'Camping' RETURN p LIMIT 10",
    "parameters": {}
}

response = requests.post(
    'https://<your-fabric-endpoint>/v1/ontology/query',
    headers=headers,
    json=query
)
```

#### Power BI Connection
1. **Get Data** → More → Online Services → Microsoft Fabric
2. **Connect to Ontology** → Select your workspace and ontology
3. **Import Relationships** → Fabric automatically maps graph relationships
4. **Build Reports** → Use semantic understanding for intuitive reporting

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

### 🎯 Strategic Business Questions - **THE ONTOLOGY ADVANTAGE**

#### **C-Suite Risk Management** 🏢
- "Identify our top 5 supply chain vulnerabilities" → **Instant risk dashboard**
- "Which products have backup supplier coverage?" → **Supplier dependency analysis**
- "Show me geographic concentration risks in our supplier base" → **Geographic risk heatmap**
- "What's our inventory buffer against supply disruptions?" → **Resilience scoring**

#### **Operational Excellence** 🔧
- "Which slow-moving products are tying up warehouse space?" → **Capital optimization**
- "Show me opportunities to consolidate suppliers for better terms" → **Procurement strategy**
- "Which products could benefit from demand forecast accuracy improvements?" → **ML model targeting**
- "Where can we optimize safety stock levels without increasing risk?" → **Inventory optimization**

#### **Performance Intelligence** 📊
- "Compare inventory turnover rates across product categories" → **Category performance**
- "Show supplier performance rankings by reliability and cost" → **Vendor scorecards**
- "What's our forecast accuracy vs. industry benchmarks?" → **Competitive analysis**
- "How does our warehouse utilization compare to capacity planning goals?" → **Operational KPIs**

**💰 Business Impact:** Each question represents decisions worth **millions in working capital, risk mitigation, and operational efficiency**.

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

## 🔧 **Technical Implementation Details**

### **Ontology Configuration**

**Entity Type Mapping:**
```yaml
Product:
  key: ProductID
  properties: [ProductName, ListPrice, StandardCost, ProductCategoryID]
  relationships: [BelongsToCategory]

Inventory:
  key: InventoryID  
  properties: [CurrentStock, ReorderPoint, WarehouseID, ProductID]
  relationships: [TracksProduct, StoredAt]

Suppliers:
  key: SupplierID
  properties: [SupplierName, LeadTimeDays, ReliabilityScore]
  relationships: [SuppliesProduct]
```

### **Common Issues & Solutions**

**Issue**: "No data in ontology preview"
**Solution**: 
1. Check semantic model relationships are published
2. Verify lakehouse tables are managed (not external)
3. Refresh graph model manually

**Issue**: "GQL queries fail"
**Solution**:
1. Verify relationship names match ontology schema
2. Check relationship directions
3. Add `Support group by in GQL` to agent instructions

**Issue**: "Agent gives generic responses"
**Solution**:
1. Bind data to entity types
2. Refresh graph model after schema changes
3. Test with simple queries first

### **Performance Optimization**

- **Graph Model Refresh**: Schedule during off-hours
- **Query Complexity**: Start simple, build complexity incrementally  
- **Data Volume**: Test with subset before full dataset
- **Relationship Depth**: Limit traversal depth for large graphs

### **Development Checklist**

**Phase 1 - Setup:**
- [ ] Fabric workspace configured (F64+ capacity)
- [ ] Lakehouse tables created with proper relationships
- [ ] Power BI semantic model published
- [ ] Ontology generated from semantic model

**Phase 2 - Configuration:**
- [ ] Entity types reviewed and renamed if needed
- [ ] Entity type keys configured
- [ ] Relationship types bound to data
- [ ] Graph model refreshed

**Phase 3 - Testing:**
- [ ] Basic GQL queries tested
- [ ] Cross-domain relationships verified
- [ ] Data agent created and configured
- [ ] Natural language queries tested

**Phase 4 - Validation:**
- [ ] Sample questions from each domain work
- [ ] Performance acceptable for data volume
- [ ] Agent responses are domain-specific
- [ ] Documentation updated

### **Next Steps for Engineers**

1. **Clone this accelerator** as starting template
2. **Replace sample data** with your business domain
3. **Modify entity relationships** for your use case
4. **Test incrementally** with simple queries first
5. **Scale gradually** to production data volumes

### **Resources & Documentation**

- [Fabric Ontology Documentation](https://learn.microsoft.com/en-us/fabric/iq/ontology/)
- [GQL Query Reference](https://learn.microsoft.com/en-us/fabric/graph/gql-reference-abridged)
- [Power BI Semantic Models](https://learn.microsoft.com/en-us/fabric/data-warehouse/semantic-models)
- [Data Agent Configuration](https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent)