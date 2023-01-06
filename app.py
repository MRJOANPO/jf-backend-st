import streamlit as st
from sqlalchemy import create_engine
import pandas as pd




engine = create_engine(
    url="{0}+{1}://{2}:{3}@{4}:{5}/{6}".format(
        st.secrets["DATABASE_DIALECT"],
        st.secrets["DATABASE_DRIVER"],
        st.secrets["DATABASE_USER"],
        st.secrets["DATABASE_PASSWORD"],
        st.secrets["DATABASE_HOST"],
        st.secrets["DATABASE_PORT"],
        st.secrets["DATABASE_NAME"]
    )
)

query = "SELECT * FROM `Anmeldung`"
data_total = pd.read_sql(query, engine)

st.dataframe(data_total, use_container_width=True)

current_id = 0

def all_view():
    for current_person in data_total:
        st.write(current_person)