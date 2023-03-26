import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

st.title('Real World Sales Analysis Project')
st.markdown("""
#### Task #1: Merge the 12 months of sales data into a single CSV file:
""")
files = [file for file in os.listdir("./Sales_Data")]
all_months_data = pd.DataFrame()
for file in files:
    df = pd.read_csv("./Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, df])

all_months_data.to_csv("all_data.csv", index=False)
all_data = pd.read_csv("all_data.csv")

st.markdown("""
#### Task #2: Clean up the data:
* **Drop empty rows**
""")
nan_df = all_data[all_data.isna().any(axis=1)]
all_data = all_data.dropna(how='all')
st.markdown("""
* **Find and Delete invalid rows**
""")
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
st.markdown("""
* **Convert into the correct data type**
""")
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

st.markdown("""
#### Task #3: Augment data with additional columns:
* **Add month column**
""")
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
st.markdown("""
* **Add sales column**
""")
all_data['Sales'] = all_data['Quantity Ordered'] * all_data["Price Each"]
st.markdown("""
* **Add city column**
""")


def get_city(address):
    return address.split(',')[1]


def get_state(address):
    return address.split(',')[2].split(' ')[1]


all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

st.markdown("""
## Output:
""")
st.write(all_data)

st.markdown("""
### Question #1: What was the best month for sales? How much was earned that month?
""")
months = range(1, 13)
results = all_data.groupby('Month').sum()
plt.bar(months, results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')

st.pyplot(plt)
plt.clf()

st.markdown("""
### Question #2: What city had the highest number of sales?
""")
cities = [city for city, df in all_data.groupby('City')]
results = all_data.groupby('City').sum()
plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation='vertical', size=8)
plt.xlabel('City Name')
plt.ylabel('Sales in USD ($)')

st.pyplot(plt)
plt.clf()

st.markdown("""
### Question #3: What time should we display advertisements to maximize likelihood of customer's buying a product?
""")
