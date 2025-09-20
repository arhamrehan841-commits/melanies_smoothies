# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! 🍓")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
session = get_active_session()

# Get fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()

# Extract fruit names into a Python list
fruit_list = [row['FRUIT_NAME'] for row in my_dataframe]

# Multiselect with only fruit names (no extra dataframe shown)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

if ingredients_list:
    # Join selected ingredients into a comma-separated string
    ingredients_string = ', '.join(ingredients_list)

    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    # Submit button
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'✅ Your Smoothie ({ingredients_string}) has been ordered for {name_on_order}!', icon="👍")
