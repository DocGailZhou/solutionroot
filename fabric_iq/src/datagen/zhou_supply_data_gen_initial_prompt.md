# Sales and Supply Chain Data Gen Initial Prompt 

We have the supply chain data models defined (we can still modify if needed later). 

C:\Repos\Code\Explore\solutionroot\fabric_iq\src\fabric\notebooks\schema. 

Need to create below models

- model_inventory.ipynb
- model_supplychain.ipynb

Other models established are

- model_customer.ipynb
- model_product.ipynb
- model_sales.ipynb
- model_finance.ipynb

Now we need to define the process to generate data. 

### Data input and output 

customer and product domain data have been carefully generated and stored in 

C:\Repos\Code\Explore\solutionroot\fabric_iq\src\datagen\input.

I need to use the data  generated in sales data generated and saved in: 

C:\Repos\Code\Explore\solutionroot\fabric_iq\src\datagen\output\sales

**Sales for each product category will be stored in subfolders:**

C:\Repos\Code\Explore\solutionroot\fabric_iq\src\datagen\output\sales\kitchen

C:\Repos\Code\Explore\solutionroot\fabric_iq\src\datagen\output\sales\camping 

C:\Repos\Code\Explore\solutionroot\fabric_iq\src\datagen\output\sales\ski

**Other input:** 

For suppliers, I can give some some sample names 

For suppliers, I have created a file C:\Repos\Code\Explore\solutionroot\fabric_iq\src\datagen\input\suppliers.json

For warehouses, I have created a file  C:\Repos\Code\Explore\solutionroot\fabric_iq\src\datagen\input\warehouses.json

#### Data Output

Need to generate sales and finance data for given period, based on intelligence built in customer type and segments. 

For product category, will give more specific input later. 

Need to generate supply  data based on sales data for forecast and other intelligence such as inventory transactions (based on sales)

