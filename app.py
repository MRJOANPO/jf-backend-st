import streamlit as st
import mysql.connector
import pandas as pd


connection = mysql.connector.connect(
    host=st.secrets["DATABASE_HOST"],
    port=st.secrets["DATABASE_PORT"],
    user=st.secrets["DATABASE_USER"],
    password=st.secrets["DATABASE_PASSWORD"],
    database=st.secrets["DATABASE_NAME"]
)

query = "SELECT * FROM `Anmeldung`"
data_total = pd.read_sql(query, connection)

st.dataframe(data_total, use_container_width=True)

current_id = 0

def all_view():
    for current_person in data_total:
        st.write(current_person)