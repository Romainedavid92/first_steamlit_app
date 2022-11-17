import streamlit
import pandas

#import data
my_fruit_list = pandas.read_csv(""https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"")

# title
streamlit.title('My Parents New Healthy Diner')

# body
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

#specials Header
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# fruit dataframe 
streamlit.dataframe(my_fruit_list) # pandas df turned to streamlist df
