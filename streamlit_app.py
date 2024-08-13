# Import python packages
import streamlit as st
import requests

# st.text(fruityvice_response)

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!.
    """
)



# option = st.selectbox(
#     "What is your Favourite Fruit?",
#     ("Banana", "Strawberry", "peaches"),
# )

# st.write("Your Favourite Fruit is:", option)

from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)





options = st.multiselect(
    "Choose upto 5 ingredients:",my_dataframe ,max_selections=5
   
)


if options:
    st.write("You selected:", options)
    st.text( options)
    ingredients_string=''
    for each in options:
        ingredients_string+=each+' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
    values ('""" + ingredients_string + """')"""

    st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


