import datetime as dt
import streamlit as st
import mysql.connector
import pandas as pd
import requests
import weasyprint

MONEY_EARLY = 268
MONEY_LATE = 318
MONEY_BUS = 80
MONEY_SIBLING = -30
MONEY_STAFF = -50
MONEY_KITCHEN = 0
DATE_EARLY_BIRD = dt.date(2023, 4, 1)

SIGN_UP_DATETIME = "timestamp"
FIRST_NAME_COL = "first_name"
LAST_NAME_COL = "last_name"
KEY_COL = "id"
FORM_FOR_CHILD_COL = "form_for_child"
PARENT_FIRST_NAME_COL = "parent_first_name"
PARENT_LAST_NAME_COL = "parent_last_name"
EMAIL_COL = "email"
PHONE_COL = "phone"
PARENT_EMAIL_COL = "parent_email"
PARENT_PHONE_COL = "parent_phone"
ADDRESS_COL = "address"
ZIP_COL = "zip"
CITY_COL = "city"
COUNTRY_COL = "country"
GENDER_COL = "gender"
T_SHIRT_COL = "t_shirt_size"
BIRTHDAY_COL = "birthday"
DOCTOR_NAME_COL = "doctor_name"
DOCTOR_PHONE_COL = "doctor_phone"
EMERGENCY_CONTACT_1_NAME_COL = "emergency_contact_1_name"
EMERGENCY_CONTACT_1_PHONE_COL = "emergency_contact_1_phone"
EMERGENCY_CONTACT_2_NAME_COL = "emergency_contact_2_name"
EMERGENCY_CONTACT_2_PHONE_COL = "emergency_contact_2_phone"
ALLERGIES_COL = "allergies"
MENTAL_ISSUES_COL = "mental_issues"
CHRONICAL_DISEASES_COL = "chronical_diseases"
MEDICATION_COL = "medication"
ZIMMERWUNSCH_COL = "zimmerwunsch"
ZECKENIMPFUNG_COL = "zecken_impfung"
TETANUS_IMPFUNG_COL = "tetanus_impfung"
BUS_COL = "bus"
BUS_MUENSTER_COL = "bus_muenster"
SIBLING_COL = "sibling"
MITARBEITER_COL = "mitarbeiter"
COMMENT_COL = "comment"
SPONSORED_COL = "sponsored"
BALANCE_COL = "balance"
STAFF_COL = "mitarbeiter"
CONFIRMED_COL = "confirmed"

############### Functions ###############
def render_name(primary):
    current_index = data_total[data_total[KEY_COL]==primary].index
    display_data = data_total.loc[current_index, FIRST_NAME_COL].values + " " + data_total.loc[current_index, LAST_NAME_COL].values + f" ({primary})"
    return display_data[0]

############### Views ###############
def all_view():
    st.dataframe(data_total)

def single_view(primary=0):
    current_id = st.sidebar.selectbox("Namen auswählen", data_total[KEY_COL], format_func=render_name, index=primary)
    current_data = data_total[data_total[KEY_COL]==current_id]
    current_name = current_data[FIRST_NAME_COL] + " " + current_data[LAST_NAME_COL]
    st.markdown(f"### {current_name.values[0]}")
    st.dataframe(current_data.T, use_container_width=True)


def single_edit(primary=0):
    current_id = st.sidebar.selectbox("Namen auswählen", data_total[KEY_COL], format_func=render_name, index=primary)
    current_data = data_total[data_total[KEY_COL]==current_id]
    current_name = current_data[FIRST_NAME_COL].values[0] + " " + current_data[LAST_NAME_COL].values[0]
    st.markdown(f"### Bearbeitung von {current_name} ({current_id})")
    with st.form("Bearbeitung"):
        first_name = st.text_input("Vorname", current_data[FIRST_NAME_COL].values[0])
        last_name = st.text_input("Nachname", current_data[LAST_NAME_COL].values[0])
        form_for_child = st.checkbox("Für Kind", current_data[FORM_FOR_CHILD_COL].values[0])
        parent_first_name = st.text_input("Vorname des Erziehungsberechtigten", current_data[PARENT_FIRST_NAME_COL].values[0])
        parent_last_name = st.text_input("Nachname des Erziehungsberechtigten", current_data[PARENT_LAST_NAME_COL].values[0])
        email = st.text_input("E-Mail", current_data[EMAIL_COL].values[0])
        phone = st.text_input("Nachname", current_data[PHONE_COL].values[0])
        parent_email = st.text_input("E-Mail Eltern", current_data[PARENT_EMAIL_COL].values[0])
        parent_phone = st.text_input("Telefon Eltern", current_data[PARENT_PHONE_COL].values[0])
        address = st.text_input("Adresse", current_data[ADDRESS_COL].values[0])
        plz = st.number_input("PLZ", current_data[ZIP_COL].values[0])
        city = st.text_input("Stadt", current_data[CITY_COL].values[0])
        country = st.text_input("Land", current_data[COUNTRY_COL].values[0])
        gender = st.text_input("Geschlecht (m/w)", current_data[GENDER_COL].values[0])
        t_shirt_size = st.text_input("T-Shirt-Size", current_data[T_SHIRT_COL].values[0])
        birthday = st.date_input("Geburtstag", current_data[BIRTHDAY_COL].values[0])
        doctor_name = st.text_input("Arzt Name", current_data[DOCTOR_NAME_COL].values[0])
        doctor_phone = st.text_input("Arzt Telefon", current_data[DOCTOR_PHONE_COL].values[0])
        emergency_contact_1_name = st.text_input("Notfallkontakt 1 Name", current_data[EMERGENCY_CONTACT_1_NAME_COL].values[0])
        emergency_contact_1_phone = st.text_input("Notfallkontakt 1 Telefon", current_data[EMERGENCY_CONTACT_1_PHONE_COL].values[0])
        emergency_contact_2_name = st.text_input("Notfallkontakt 2 Name", current_data[EMERGENCY_CONTACT_2_NAME_COL].values[0])
        emergency_contact_2_phone = st.text_input("Notfallkontakt 2 Telefon", current_data[EMERGENCY_CONTACT_2_PHONE_COL].values[0])
        allergies = st.text_area("Allergien", current_data[ALLERGIES_COL].values[0])
        mental_issues = st.text_area("Geistige oder soziale Beeinträchtigungen", current_data[MENTAL_ISSUES_COL].values[0])
        chronical_diseases = st.text_area("Chronische Erkrankungen", current_data[CHRONICAL_DISEASES_COL].values[0])
        medication = st.text_area("Regelmäßige Medikamenteneinnahme", current_data[MEDICATION_COL].values[0])
        zimmerwunsch = st.text_area("Zimmerwunsch", current_data[ZIMMERWUNSCH_COL].values[0])
        comment = st.text_area("Kommentar", current_data[COMMENT_COL].values[0])
        tetanus = st.checkbox("Tetanus Impfung", current_data[TETANUS_IMPFUNG_COL].values[0])
        zecken = st.checkbox("Zecken Impfung", current_data[ZECKENIMPFUNG_COL].values[0])
        bus = st.checkbox("Mit Busfahrt", current_data[BUS_COL].values[0])
        bus_muenster = st.checkbox("Mit Buszustieg in Münster", current_data[BUS_MUENSTER_COL].values[0])

        balance = st.number_input("Geldeingang", current_data[BALANCE_COL].values[0])
        sponsored = st.checkbox("Gesponsert", current_data[SPONSORED_COL].values[0])
        staff = st.checkbox("Mitarbeiter", current_data[STAFF_COL].values[0])
        confirmed = st.checkbox("Teilnahme bestätigt", current_data[CONFIRMED_COL].values[0])

        submit = st.form_submit_button()
        if submit:
            update_query = f"UPDATE Anmeldung SET {FIRST_NAME_COL}='{first_name}', {LAST_NAME_COL}='{last_name}',{FORM_FOR_CHILD_COL}={form_for_child},{PARENT_FIRST_NAME_COL}='{parent_first_name}',{PARENT_LAST_NAME_COL}='{parent_last_name}',{PHONE_COL}='{phone}',{EMAIL_COL}='{email}',{PARENT_EMAIL_COL}='{parent_email}',{PARENT_PHONE_COL}='{parent_phone}',{ADDRESS_COL}='{address}',{ZIP_COL}={plz},{CITY_COL}='{city}',{COUNTRY_COL}='{country}',{GENDER_COL}='{gender}',{T_SHIRT_COL}='{t_shirt_size.lower()}',{BIRTHDAY_COL}='{birthday}',{DOCTOR_NAME_COL}='{doctor_name}',{DOCTOR_PHONE_COL}='{doctor_phone}',{EMERGENCY_CONTACT_1_NAME_COL}='{emergency_contact_1_name}',{EMERGENCY_CONTACT_1_PHONE_COL}='{emergency_contact_1_phone}',{EMERGENCY_CONTACT_2_NAME_COL}='{emergency_contact_2_name}',{EMERGENCY_CONTACT_2_PHONE_COL}='{emergency_contact_2_phone}',{ALLERGIES_COL}='{allergies}',{MENTAL_ISSUES_COL}='{mental_issues}',{CHRONICAL_DISEASES_COL}='{chronical_diseases}',{MEDICATION_COL}='{medication}',{ZIMMERWUNSCH_COL}='{zimmerwunsch}',{COMMENT_COL}='{comment}',{TETANUS_IMPFUNG_COL}={tetanus},{ZECKENIMPFUNG_COL}={zecken},{BUS_COL}={bus},{BUS_MUENSTER_COL}={bus_muenster},{SPONSORED_COL}={sponsored},{BALANCE_COL}={balance},{STAFF_COL}={staff},{CONFIRMED_COL}={confirmed} WHERE {KEY_COL} = {current_id}"
            update_cursor = connection.cursor()
            update_cursor.execute(update_query)
            connection.commit()
            st.write(f"{update_cursor.rowcount} Datensatz aktualisiert")

    if st.button("Löschen"):
        delete_query = f"DELETE FROM Anmeldung WHERE id={current_id}"
        delete_cursor = connection.cursor()
        delete_cursor.execute(delete_query)
        connection.commit()
        st.write(f"{delete_cursor.rowcount} Datensatz gelöscht")

    if st.button("Rechnung erstellen"):
        api_key = st.secrets["RS_API_KEY_INVOICE"]
        invoice_api_url = st.secrets["RS_API_URL_INVOICE"]

        if current_data[FORM_FOR_CHILD_COL].value[0]:
            # Invoice at Parent
            invoice_name = current_data[PARENT_FIRST_NAME_COL].values[0] + " " + current_data[PARENT_LAST_NAME_COL].values[0]
        else:
            invoice_name = current_name

        sign_up_date = dt.datetime.fromisoformat(current_data[SIGN_UP_DATETIME].values[0])

        if sign_up_date < DATE_EARLY_BIRD:
            freizeitkosten = MONEY_EARLY
        else:
            freizeitkosten = MONEY_LATE

        if current_data[BUS_COL].values[0]:
            buskosten = MONEY_BUS
        else:
            buskosten = 0



        discount = 0

        if current_data[SIBLING_COL].values[0]:
            discount += MONEY_SIBLING

        if current_data[STAFF_COL].values[0]:
            discount += MONEY_STAFF

        total_cost = freizeitkosten + buskosten + discount

        if current_data[SPONSORED_COL].values[0]:
            discount = -total_cost

        data_invoice = {
            "key": api_key,
            "id": current_id,
            "invoice_name": invoice_name,
            "name_teilnehmer": current_name,
            "address_street": current_data[ADDRESS_COL].values[0],
            "address_zip": current_data[ZIP_COL].values[0],
            "address_city": current_data[CITY_COL].values[0],
            "address_country": current_data[COUNTRY_COL].values[0],
            "buskosten": buskosten,
            "discount": -discount
        }

        response = requests.get(
            url=invoice_api_url,
            params=data_invoice,
            timeout=100
        )

        st.write(response.url)
        pdf = weasyprint.HTML(response.url).write_pdf()
        st.write(pdf)




st.markdown("# JF 2023 Dashboard")

connection = mysql.connector.connect(
    host=st.secrets["DATABASE_HOST"],
    port=st.secrets["DATABASE_PORT"],
    user=st.secrets["DATABASE_USER"],
    password=st.secrets["DATABASE_PASSWORD"],
    database=st.secrets["DATABASE_NAME"]
)

query = "SELECT * FROM `Anmeldung`"
data_total = pd.read_sql(query, connection)

views = {
    "Übersicht": all_view,
    "Einzelansicht": single_view,
    "Bearbeiten": single_edit,
}

view = st.sidebar.radio("Ansicht", views)

views[view]()
connection.close()
