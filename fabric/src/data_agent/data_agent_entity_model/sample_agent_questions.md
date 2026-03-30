# Sample Agent Test Questions

## Overview

This document provides sample questions to test the Data Agent Entity Model's capabilities across product inventory, warehouse operations, supply chain management, and demand forecasting scenarios.

## How to Use These Questions

The questions below contain placeholders in square brackets (e.g., `[Product Name]`) that you should replace with actual values from your system. You can also ask the data agent to show you available options first.

### Example Values

**Product Names:**
- Adventurer Pro Backpack
- Alpine Explorer Tent  
- Espresso Machine
- Food Storage Set
- Waterproof Ski Pants
- Ski Boot Bag - Premium

**Product Categories:**
- Backpacks
- Camping Stoves
- Ice Cream Dishes
- Cooking Utensils
- Ski Apparel
- Winter Footwear

**Warehouse Names:**
- Main Warehouse
- Regional Warehouse
- Backup Warehouse

**Supplier Names:**
- Ask the data agent: "List all suppliers" to get available supplier names

> **Tip:** You can ask the data agent to "show me all product categories" or "list all product names" to discover available values for testing. 
---

## Test Questions

| # | Domain | Question | Notes |
|---|--------|----------|-------|
| 1 | Inventory | What is the available stock for [**Product Name**] in all warehouses? | Multi-warehouse stock query |
| 2 | Inventory | List products that are below their reorder point. | Stock alert analysis |
| 3 | Inventory | Which products have the highest inventory levels? | High stock identification |
| 4 | Inventory | How much of [Product Name] is reserved in stock? | Reserved stock inquiry |
| 5 | Warehouse | Show details for all warehouses, including their locations and capacities. | Warehouse information overview |
| 6 | Warehouse | Which warehouse has the most available space? | Capacity analysis |
| 7 | Warehouse | List all products stored in [Warehouse Name]. | Warehouse inventory view |
| 8 | Supply Chain | Who are the suppliers for [Product Name]? | Supplier lookup |
| 9 | Purchase Order | List all purchase orders awaiting delivery. | Pending delivery tracking |
| 10 | Purchase Order | Show recent purchase orders from [Supplier Name]. | Supplier order history |
| 11 | Supply Chain | Which products are supplied by [Supplier Name]? | Supplier product catalog |
| 12 | Supply Chain | List recent supply chain events or disruptions for [Product Name]. | Product-specific disruptions |
| 13 | Demand Forecast | What is the demand forecast for [Product Category] next month? | Category demand prediction |
| 14 | Demand Forecast | Which products are expected to have low demand in the upcoming quarter? | Low demand identification |
| 15 | Product Category | What are all the product categories in the system? | Category listing |
| 16 | Product Category | Show all products in the [Category Name] category. | Category product view |