import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#import data
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#snowflake connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()

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

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# fruit dataframe 
streamlit.dataframe(fruits_to_show) # pandas df turned to streamlist df


streamlit.header('Fruityvice Fruit Advice!')

try:
    fruit_variable = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_variable:
        streamlit.error("Please select a fruit to get information.")
    else:
        streamlit.write('The user entered', fruit_variable)

        # api request
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_variable}")

        fruity_vice_normalized = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruity_vice_normalized)
except URLError as e:
    streamlit.error()

streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

second_fruit_variable = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.text(f"Thanks for adding {second_fruit_variable}!")

streamlit.stop()

my_cur.execute("insert into fruit_load_list values ('test from streamlit')");