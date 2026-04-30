# Sample Agent Test Questions

Test questions to validate the Semantic Model → Ontology data agent. Organized by difficulty — start from the top and work down.

---

## Test Questions

| # | Level | Domain | Question | Validates | Test Result F2 | Test Results F8 |
|---|---|---|---|---|---|---|
| 1 | Beginner | Product | How many products do we have? | Single-entity count | Good. | Good |
| 2 | Beginner | Product | List all product categories. | Entity listing + display names | Good | Good |
| 3 | Beginner | Inventory | List all warehouses. | Entity listing | Good | Good |
| 4 | Beginner | Supply Chain | List all suppliers. | Entity listing | Good | Good |
| 5 | Intermediate | Inventory | Which products are below their reorder point? | Filter + comparison logic | Good | Good |
| 6 | Intermediate | Inventory | What is the current stock of Alpine Explorer Tent? | Product → Inventory join | Technical Issues | **Good** |
| 7 | Intermediate | Inventory | Show all purchase orders with status Delivered. | Status filter (valid values: Delivered, Sent, InTransit) | Good | Good |
| 8 | Intermediate | Supply Chain | Which products are supplied by Fabrikam | Bridge entity traversal. Supplier names: Fabrikam, Contoso Ltd, Proseware Inc, Alpine Ski House, Worldwide Importers | Good | Good |
| 9 | Intermediate | Inventory | Which warehouse has the most available stock? | Aggregation + sorting | Good | Good |
| 10 | Intermediate | Inventory | How much of Coffee Mug is reserved in stock? | Specific product lookup | no answer | **Good** |
| 11 | Advanced | Inventory | What is total forecasted demand for Summit Breeze Jacket (Ice Cream Bowl) | Category → Product → Forecast path | Good | Good |
| 12 | Advanced | Inventory | List top 5 products by current stock in Main Distribution Center. | Multi-hop join + sort + limit | Good | Good |
| 13 | Advanced | Supply Chain | Which suppliers were affected by weather disruptions? | Event impact traversal | Good | Good |
| 14 | Advanced | Supply Chain | What is the total value of purchase orders with supplier Fabrikam | Aggregation across PO items + supplier | no answer | no answer |
| 15 | Advanced | Cross-domain | Show products with low stock that have active supply chain disruptions. | Multi-domain correlation | Good | Good |
