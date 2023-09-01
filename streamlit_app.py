import streamlit 
import pandas as pd
import requests
import snowflake.connector

streamlit.title("My Parents New Healthy Diner")

streamlit.header("Breakfast Menu")
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header("Build Your Own Fruit Smothie")

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

streamlit.dataframe(my_fruit_list)

my_fruit_list = my_fruit_list.set_index('Fruit')

# create multiselect 
fruit_filter = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])

filtered = my_fruit_list.loc[fruit_filter]

#display the table 

streamlit.dataframe(filtered)

#new section to display the fruiyvice response 

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

resp = requests.get('https://fruityvice.com/api/fruit/'+fruit_choice)
streamlit.text(resp)
streamlit.text(resp.json())

#snowflake 

streamlit.header("Snowflake part")
my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])

#add input filed 
add_my_fruit = streamlit.text_input("Add any fruit you like : ")
my_cur = my_cnx.cursor()
my_cur.execute(f"INSERT INTO fruit_load_list VALUES ('{add_my_fruit}')")
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text(f"the fruit load list contains : {my_data_row}")
