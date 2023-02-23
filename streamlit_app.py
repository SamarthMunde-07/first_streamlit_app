
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣  Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale ,Spinach & Rocket Smoothy')
streamlit.text('🍔 Burger, Pizza & pastas')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#adding the table
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


#multiselect function
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#a function for repeatly running the code
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  

#TO GET FUTIVICE API RESPONSE I.E BY REQUESTS
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
      
      
except URLError as e:
  streamlit.error()
  
#below this will not run
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT* FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruitload List Contains:")
streamlit.dataframe(my_data_rows)

#End user to add the fruit
add_my_fruit = streamlit.text_input('What fruit would you like information about?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

#adding new value
my_cur.execute("insert into fruit_load_list values('from streamlit')")

