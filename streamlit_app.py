import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#import data
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

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

def get_fruityvice_data(this_fruit_choice):
    #api request
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_variable}")
    fruity_vice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruity_vice_normalized

try:
    fruit_variable = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_variable:
        streamlit.error("Please select a fruit to get information.")
    else:
        streamlit.write('The user entered', fruit_variable)
        back_from_function = get_fruityvice_data(fruit_variable)

        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()

streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
    #snowflake connection
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    streamlit.dataframe(my_data_row)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"insert into fruit_load_list values ('{add_my_fruit}')")
        return "Thanks for adding" + new_fruit

# allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)


streamlit.stop()

