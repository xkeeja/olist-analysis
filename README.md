## Objectives of the module

We will analyze a dataset provided by an e-commerce marketplace called [Olist](https://www.olist.com) to answer the CEO's question:

> How to increase customer satisfaction (so as to increase profit margin) while maintaining a healthy order volume?

## About Olist 🇧🇷

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/best-practices/olist.png" width="500"/>

Olist is a leading e-commerce service that connects merchants to main marketplaces in Brazil. They provide a wide range of offers including inventory management, dealing with reviews and customer contacts to logistic services.

Olist charges sellers a monthly fee. This fee is progressive with the volume of orders.

Here are the seller and customer workflows:

**Seller:**

- Seller joins Olist
- Seller uploads products catalogue
- Seller gets notified when a product is sold
- Seller hands over an item to the logistic carrier

👉 Note that multiple sellers can be involved in one customer order!

**Customer:**

- Browses products on the marketplace
- Purchases products from Olist.store
- Gets an expected date for delivery
- Receives the order
- Leaves a review about the order

👉 A review can be left as soon as the order is sent, meaning that a customer can leave a review for a product he did not receive yet!

## Dataset

The dataset consists of ~100k orders from 2016 and 2018 that were made on the Olist store, available as csv files on Le Wagon S3 bucket (❗️the datasets available on Kaggle may be slightly different).

✅ Download the 9 datasets compressed in the `olist.zip` file, unzip it and store them in your `~/code/<user.github_nickname>/{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }}/data/csv` folder:

```bash
curl https://wagon-public-datasets.s3.amazonaws.com/olist/olist.zip > ~/code/<user.github_nickname>/{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }}/data/csv/olist.zip
unzip -d ~/code/<user.github_nickname>/{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }}/data/csv/ ~/code/<user.github_nickname>/{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }}/data/csv/olist.zip
rm ~/code/<user.github_nickname>/{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }}/data/csv/olist.zip
```

Check you have the 9 datasets on your machine:

```bash
ls ~/code/<user.github_nickname>/{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }}/data/csv
```

## Setup

### 1 - Project Structure
Go to your local `~/code/<user.github_nickname>` folder.
This will be your project structure for the week.

```bash
.
# Your whole code logic and data, this is your "package"
├── context-and-setup
    ├── data                # Your data source (git ignored)
    |   ├── csv
    |   |   ├── olist_customers_dataset.csv
    |   |   └── olist_orders_dataset.csv
    |   |   └── ...
    |   ├── README.md       # database documentation
    |
    ├── olist               # Your data-processing logic
    |   ├── data.py
    |   ├── product.py
    |   ├── seller.py
    |   ├── utils.py
    |   └── __init__.py.    # turns the olist folder into a "package"
# Your notebooks & analyses, challenge-by-challenge
├── data-preparation
├── exploratory-analysis
├── orders
├── simple-analysis
├── ...
├── logit
├── olist_ceo_request
```

### 2 - Edit the `PYTHONPATH`

Add `olist` path to your `PYTHONPATH`.

This will allow you to easily import modules defined in `olist` in your notebooks throughout the week.

Open your terminal and navigate to your home directory by running:

```bash
cd
```

Now you'll need to open your `.zshrc` file. As you might have noticed the file starts with a dot which means it's a hidden file. To be able to see this file in your terminal you'll need to run the command below, the flag `-a` will allow you to see hidden files:

```bash
ls -a
```

Next lets open the file using your text editor:

```bash
code .zshrc
```

Now in your terminal run:
```bash
cd ~/code/<user.github_nickname>/{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }} && echo "export PYTHONPATH=\"$(pwd):\$PYTHONPATH\""
```

👉 Copy the resulting output line from your terminal and paste it at the bottom of your ~/.zshrc file. Don't forget to save and restart all your terminal windows to take this change into account.



### 🔥 Check your setup

Go to your `{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }}` folder and run an `ipython` session:

```bash
cd ~/code/<user.github_nickname>/{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }}
ipython
```

Then type the following to check that the setup phase from the previous exercise worked:

```python
from olist.data import Olist
Olist().ping()
# => pong
```

If you get something else than `pong`, raise a ticket to get some help from a TA. You might have a problem with the `$PYTHONPATH`.

## Push your code on GitHub

From your `{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }}` directory, commit and push your code:

```bash
cd ~/code/<user.github_nickname>/{{ local_path_to("04-Decision-Science/01-Project-Setup/01-Context-and-Setup") }}
git add .
git commit -m 'kick off olist challenge'
git push origin master
```


🏋️‍♀️ This is the final challenge of the week (you have until the end of the Communicate topic to complete it).

**Before diving into it, take time to finish the challenge 02 on sellers analysis (Liner Regression topic)**.

## Problem

>❓ How should Olist improve it's profit margin, given that it has:
> - some revenues per sellers per months
> - some revenues per orders
> - some reputation costs (estimated) per bad reviews
> - some operational costs of IT system that grows with number of orders, but not linearly (scale effects)

## Unit Economics (detailed)

***Revenue***

- Olist takes a **10% cut** on the product price (excl. freight) of each order delivered.
- Olist charges **80 BRL by month** per seller.

***Cost***

- In the long term, bad customer experience has business implications: low repeat rate, immediate customer support cost, refunds or unfavorable word of mouth communication. We will assume that we have an estimate measure of the monetary cost for each bad review:

review_score|cost (BRL)
---|---
1 star|100
2 stars|50
3 stars|40
4 stars|0
5 stars|0

In addition, Olist's **IT costs** (servers, etc...) increase with the amount of orders processed, albeit less and less rapidly (scale effects).
For the sake of simplicity, we will consider Olist's **total cumulated IT Costs** to be proportional to the **square-root** of the total cumulated number of orders approved.
The IT department also told you that since the birth of the marketplace, cumulated IT costs have amounted to 500,000 BRL.

## ✏️ Your turn!

👉 **Open the `ceo_request.ipynb` notebook and start from there.**

- We'll start from a blank Notebook
- Refrain from re-using from previous notebooks - they were made for investigation only
- All your re-usable logic is coded in `olist/*.py` scripts
