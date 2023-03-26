import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
from PIL import Image

st.title('Real World Sales Analysis Project')
st.markdown("""
This app performs simple analysis of an online tech store sales dataset for 2019!  \n
* **Data Source:** Randomly Generated using create_data.py script in the git repository
* **Python libraries:** pandas, matplotlib, streamlit
""")
importIm = Image.open('./Misc/Import.png')
st.image(importIm)
st.markdown("""

""")
st.markdown("""
#### Task #1: Merge the 12 months of sales data into a single CSV file:
""")
task1Im = Image.open('./Misc/Task#1.png')
st.image(task1Im)

files = [file for file in os.listdir("./Sales_Data")]
all_months_data = pd.DataFrame()
for file in files:
    df = pd.read_csv("./Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, df])

all_months_data.to_csv("all_data.csv", index=False)
all_data = pd.read_csv("all_data.csv")

st.markdown("""
## Input Data:
""")
st.write(all_data)

st.markdown("""
#### Task #2: Clean up the data:
* **Drop empty rows**
""")
task21Im = Image.open('./Misc/Task#2.1.png')
st.image(task21Im)

nan_df = all_data[all_data.isna().any(axis=1)]
all_data = all_data.dropna(how='all')
st.markdown("""
* **Find and Delete invalid rows**
""")
task22Im = Image.open('./Misc/Task#2.2.png')
st.image(task22Im)

all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
st.markdown("""
* **Convert into the correct data type**
""")
task23Im = Image.open('./Misc/Task#2.3.png')
st.image(task23Im)

all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

st.markdown("""
#### Task #3: Augment data with additional columns:
* **Add month column**
""")
task31Im = Image.open('./Misc/Task#3.1.png')
st.image(task31Im)

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
st.markdown("""
* **Add sales column**
""")
task32Im = Image.open('./Misc/Task#3.2.png')
st.image(task32Im)

all_data['Sales'] = all_data['Quantity Ordered'] * all_data["Price Each"]
st.markdown("""
* **Add city column**
""")
task33Im = Image.open('./Misc/Task#3.3.png')
st.image(task31Im)


def get_city(address):
    return address.split(',')[1]


def get_state(address):
    return address.split(',')[2].split(' ')[1]


all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

st.markdown("""
* **Add hour column**
""")
task34Im = Image.open('./Misc/Task#3.4.png')
st.image(task34Im)

all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute

st.markdown("""
## Output Data:
""")
st.write(all_data)

st.markdown("""
### Question #1: What was the best month for sales?
**Answer:** The store's best sales for 2019 were during *December*!
""")
question1Im = Image.open('./Misc/Question#1.png')
st.image(question1Im)

months = range(1, 13)
results_1 = all_data.groupby('Month').sum(numeric_only=True)
plt.bar(months, results_1['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')

st.pyplot(plt)
plt.clf()

st.markdown("""
### Question #2: What city had the highest number of sales?
**Answer:** *San Francisco (CA)* has made the most number of sales for 2019 by *almost 2 times* than its closest competitor!
""")
question2Im = Image.open('./Misc/Question#2.png')
st.image(question2Im)

cities = [city for city, df in all_data.groupby('City')]
results_2 = all_data.groupby('City').sum(numeric_only=True)
plt.bar(cities, results_2['Sales'])
plt.xticks(cities, rotation='vertical', size=8)
plt.xlabel('City Name')
plt.ylabel('Sales in USD ($)')

st.pyplot(plt)
plt.clf()

st.markdown("""
### Question #3: What time should we display advertisements to maximize likelihood of customer's buying a product?
**Answer:** It appears that the most optimal times for showing advertisements to customers are between  \n *11 AM - 1 PM* and *6 PM - 8 PM*!
""")
question3Im = Image.open('./Misc/Question#3.png')
st.image(question3Im)

hours = [hour for hour, df in all_data.groupby('Hour')]
results_3 = all_data.groupby(['Hour']).count()
plt.plot(hours, results_3)
plt.xticks(hours)
plt.xlabel('Hours')
plt.ylabel('Numbers of Orders')
plt.grid()

st.pyplot(plt)
plt.clf()

st.markdown("""
### Question #4: What products are most often sold together?
**Answer:** Most people choose to buy an *appropriate charging port* when getting a new *android or apple phone*!
""")
question4Im = Image.open('./Misc/Question#4.png')
st.image(question4Im)

df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'Grouped']].drop_duplicates()

count = Counter()
for row in df['Grouped']:
    row_list = row.split(',')
    count.update((Counter(combinations(row_list, 2))))

results_4 = pd.DataFrame(count.most_common(10))
results_4.columns = ['Products', 'Quantity of Orders']

st.dataframe(results_4, use_container_width=True)

st.markdown("""
### Question #5: What product sold the most?
**Answer:** The most sold products during 2019 were *AA and AAA battery 4-packs*, because of their *low-price point* and *non-reusable nature*.
""")
question5Im = Image.open('./Misc/Question#5.png')
st.image(question5Im)

products = [product for product, df in all_data.groupby('Product')]

quantity_ordered = all_data.groupby('Product').sum()['Quantity Ordered']
prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered)
ax2.plot(products, prices, color='g')

ax1.set_xlabel('Product')
ax1.set_xticklabels(products, rotation='vertical', size=8)
ax1.set_ylabel('Quantity Ordered')
ax2.set_ylabel('Price ($)')

st.pyplot(fig)
plt.clf()
