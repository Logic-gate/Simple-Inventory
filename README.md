##Simple Inventory
I personally use this system to run my business. I thought of sharing it as to give back to the community that gave me sooooo much. It uses flask.

###Respect where it's due:
* Charts.js by http://www.chartjs.org/
* Startbootstrap-grayscale by https://github.com/IronSummitMedia

###Before you use it, please consider the following:
* This is not a sophisticated system. 
* Security measures were not taken to insure safe data transactions(I use it locally)
* Json formatted files are used instead of common DB standards.
* HTML/CSS needs a bit of work.


####Data files:
Path: `app/sku/`  
Accepted SKU titles: `WH-XXXX-NNNNN`& `DS-XXXXXX-NNNNN`. Where `WH` refers to `Warehouse` and `DS` to `Drop-Shipping`. CAPS
Quantity Validation Line: `156` & `157` in `views.py`
    
   
    warehouse_products = len([ii for ii, s in enumerate(location) if 'sku_WH' in s])
	drop_shipping_products = len([ii for ii, s in enumerate(location) if 'sku_DS' in s]) 
---

Data Format: `JSON`

    {
        "PRODUCTS": [
        {
            "SKU": "WH-TEST-112233", 
            "STOCK_LOCATION": "3R-2S", 
            "NAME": "TEST PRODUCT", 
            "WEIGHT": "125g", 
            "PLACE_OF_ORIGIN": "Planet Earth", 
            "COMPANY": "TEST COMPANY", 
            "IMAGE": "2014-06-03--1401813980_1024x768_scrot.png", 
            "STOCK": "120",
            "ORIGINAL_STOCK": "121"
        }
    ]
    }
    
Accepted Name: `sku_WH-XXXXX-NNNNN.data`. Generated automaticlly  
Image Path: `static/product/`

---
####Todo
* Track edits – especially `qty`
* Add email notification
* Security, security, security
* Add more charts

####ScreenShots
Inventory
![All](https://dl.dropboxusercontent.com/u/79143906/Screenshot%20-%2002272015%20-%2008%3A10%3A50%20PM.png)  
Add A product:
![Add Product](https://dl.dropboxusercontent.com/u/79143906/add_product.png)
Stats:
![Stats](https://dl.dropboxusercontent.com/u/79143906/Screenshot%20-%2002272015%20-%2008%3A10%3A27%20PM.png)

`