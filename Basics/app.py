
import streamlit as st
import pandas as pd
# Sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)

# Display the DataFrame in the Streamlit app    
st.title('DataFrame Example')
st.dataframe(df)

# Create a Line Chart
st.subheader('Line Chart Example')
st.line_chart(df['Age'])
# Create a Bar Chart
st.subheader('Bar Chart Example')
st.bar_chart(df.set_index('Name')['Age'])
# Create a Map
st.subheader('Map Example')
st.map(pd.DataFrame({
    'lat': [40.7128, 34.0522, 41.8781],
    'lon': [-74.0060, -118.2437, -87.6298]
}, index=['New York', 'Los Angeles', 'Chicago']))
