import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#streamlit Layout
st.set_page_config(layout="wide")

file_path = "FAOSTAT_data_en_2-20-2024.csv"
df = pd.read_csv(file_path)

# Streamlit App Title
st.title("Global Agribusiness Expansion Data")
st.write(" This live dashboard outlines key business insights, allowing relevant stakeholder to make quick business decision based on the Agriculture trend")

# Show dataset preview
if st.checkbox("Show Raw Data"):
    st.write(df.head())

# Split the page into two columns
col1, col2 = st.columns(2)

# Market Size (left)
with col1:
    st.subheader("Market Size")
    plt.figure(figsize=(8, 10))
    area_sum = df.groupby('Area')['Value'].sum().astype(int).sort_values(ascending=False)
    area_sum.head(20).plot(kind='barh', color='skyblue')
    plt.xlabel("Total Value")
    plt.ylabel("Area")
    plt.title("Total Value by Area")
    plt.gca().invert_yaxis()
    st.pyplot(plt)

# Consumer Preference (right)
with col2:  
    st.subheader("Consumer Preference")
    item_count = df.Item.value_counts()
    plt.figure(figsize=(8, 4.5))
    item_count.head(20).plot(kind='bar', color='darkblue')
    plt.xlabel("Item")
    plt.ylabel("Consumer Preference (Count)")
    plt.title("Top 20 Consumer Preferences by Item")
    plt.xticks(rotation=45, ha='right')  
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Aggregate total value sold per country
country_sum = df.groupby('Area')['Value'].sum().astype(int).sort_values(ascending=False)

# Select the top 5 countries
top_5_countries = country_sum.head(5)

# Plat Yield Lines
st.subheader("Average Yield Trend Over Time")
yield_df = df[df['Element'] == 'Yield'].copy()
yield_df['Year'] = pd.to_numeric(yield_df['Year'])
yield_trend = yield_df.groupby('Year')['Value'].mean()

plt.figure(figsize=(10, 5))
plt.plot(yield_trend.index, yield_trend.values, marker='o', linestyle='-', color='b', label='Average Yield')
plt.xlabel("Year")
plt.ylabel("Yield (units)")
plt.title("Average Yield Trend Over Time")
plt.legend()
plt.grid(True)
st.pyplot(plt)

st.subheader("Top 5 Markets with Highest Sales")
st.write(top_5_countries)

# Plot trend lines
st.subheader("Sales Trends for Top 5 Countries")

plt.figure(figsize=(10, 6))
for country in top_5_countries.index:
    country_trend = df[df['Area'] == country].groupby('Year')['Value'].sum()
    plt.plot(country_trend.index, country_trend.values, marker='o', linestyle='-', label=country)

plt.xlabel("Year")
plt.ylabel("Total Value Sold")
plt.title("Long-Term Sustainability of Top 5 Countries")
plt.legend()
plt.grid(True)
st.pyplot(plt)
