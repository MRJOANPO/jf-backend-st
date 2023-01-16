import datetime
import re

import streamlit as st
import mysql.connector
import pandas as pd
import babel.numbers

import invoice_creator
import officeHelper

MONEY_EARLY = 268
MONEY_LATE = 318
MONEY_BUS = 80
MONEY_SIBLING = -30
MONEY_STAFF = -50
MONEY_KITCHEN = 0
DATE_EARLY_BIRD = datetime.date(2023, 4, 1)

SIGN_UP_DATETIME = "datetime"
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
KITCHEN_TEAM_COL = "kitchen_team"
CONFIRMED_COL = "confirmed"
DATE_INVOICE_COL = "last_rechnung_datetime"
SWIM_CONFIRM_COL = "swim_confirm"
EXTRA_DISCOUNT_COL = "extra_discount"

############### Functions ###############
def render_name(primary):
    current_index = data_total[data_total[KEY_COL]==primary].index
    display_data = data_total.loc[current_index, FIRST_NAME_COL].values + " " + data_total.loc[current_index, LAST_NAME_COL].values + f" ({primary})"
    return display_data[0]

def calc_kosten(current_data):
    try:
        current_data = current_data.iloc[0,:]
    except pd.errors.IndexingError:
        pass

    sign_up_date = current_data[SIGN_UP_DATETIME]

    if pd.to_datetime(sign_up_date).date() < DATE_EARLY_BIRD:
        freizeitkosten = MONEY_EARLY
    else:
        freizeitkosten = MONEY_LATE

    if current_data[BUS_COL]:
        buskosten = MONEY_BUS
    else:
        buskosten = 0

    discount = 0
    discount_code = ""

    total_cost = freizeitkosten + buskosten

    if current_data[EXTRA_DISCOUNT_COL] != 0:
        discount += current_data[EXTRA_DISCOUNT_COL]
        discount_code += "Unterstützung, "

    if current_data[SIBLING_COL]:
        discount += MONEY_SIBLING
        discount_code += "Geschwister, "

    if current_data[STAFF_COL]:
        discount += MONEY_STAFF
        discount_code += "Mitarbeiter, "

    if current_data[SPONSORED_COL]:
        discount = -total_cost
        discount_code += ("Kostenlos, ")

    if current_data[KITCHEN_TEAM_COL]:
        discount = -total_cost
        discount_code += ("Küchenteam, ")

    if discount_code != "":
        discount_code = discount_code.rstrip(", ")

    return (total_cost, freizeitkosten, buskosten, discount, discount_code)

def render_money(number):
    return babel.numbers.format_currency(number, "EUR", locale="de_DE")
############### Views ###############
def all_view():
    st.markdown("### Anzahl Anmeldungen")
    data_days = data_total.groupby(data_total[SIGN_UP_DATETIME].dt.date)[KEY_COL].count()
    data_days.rename("Anzahl", inplace=True)
    st.bar_chart(data_days)
    st.dataframe(data_total)

def single_view(primary=0):
    current_id = st.sidebar.selectbox("Namen auswählen", data_total[KEY_COL], format_func=render_name, index=primary)
    current_data = data_total[data_total[KEY_COL]==current_id]
    current_name = current_data[FIRST_NAME_COL] + " " + current_data[LAST_NAME_COL]
    try:
        st.markdown(f"### {current_name.values[0]}")
    except IndexError:
        st.markdown("Keine Daten zum Anzeigen")
        return

    st.dataframe(current_data.T, use_container_width=True)

def single_edit(primary=0):
    st.sidebar.markdown("---")
    only_not_approved = st.sidebar.checkbox("Zeig nur Teilnehmer, welche noch nicht bestätigt wurden", True)
    if only_not_approved:
        data_selected = data_total[data_total[CONFIRMED_COL]==0]
        current_id = st.sidebar.selectbox("Namen auswählen", data_selected[KEY_COL], format_func=render_name, index=primary)
    else:
        current_id = st.sidebar.selectbox("Namen auswählen", data_total[KEY_COL], format_func=render_name, index=primary)

    # current_id = st.sidebar.selectbox("Namen auswählen", data_total[KEY_COL], format_func=render_name, index=primary)
    current_data = data_total[data_total[KEY_COL]==current_id]

    try:
        current_name = current_data[FIRST_NAME_COL].values[0] + " " + current_data[LAST_NAME_COL].values[0]
    except IndexError:
        st.markdown("Keine Daten zum Anzeigen")
        return

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
        swim_confirm = st.checkbox("Darf schwimmen gehen", current_data[SWIM_CONFIRM_COL].values[0])
        bus = st.checkbox("Mit Busfahrt", current_data[BUS_COL].values[0])
        bus_muenster = st.checkbox("Mit Buszustieg in Münster", current_data[BUS_MUENSTER_COL].values[0])

        balance = st.number_input("Geldeingang", current_data[BALANCE_COL].values[0])
        support = st.number_input("Unterstützung", current_data[EXTRA_DISCOUNT_COL].values[0])
        sponsored = st.checkbox("Gesponsert", current_data[SPONSORED_COL].values[0])
        staff = st.checkbox("Mitarbeiter", current_data[STAFF_COL].values[0])
        kitchen = st.checkbox("Küchenteam", current_data[KITCHEN_TEAM_COL].values[0])
        confirmed = st.checkbox("Teilnahme bestätigt", current_data[CONFIRMED_COL].values[0])

        submit = st.form_submit_button()
        if submit:
            update_query = f"UPDATE Anmeldung SET {FIRST_NAME_COL}='{first_name}', {LAST_NAME_COL}='{last_name}',{FORM_FOR_CHILD_COL}={form_for_child},{PARENT_FIRST_NAME_COL}='{parent_first_name}',{PARENT_LAST_NAME_COL}='{parent_last_name}',{PHONE_COL}='{phone}',{EMAIL_COL}='{email}',{PARENT_EMAIL_COL}='{parent_email}',{PARENT_PHONE_COL}='{parent_phone}',{ADDRESS_COL}='{address}',{ZIP_COL}={plz},{CITY_COL}='{city}',{COUNTRY_COL}='{country}',{GENDER_COL}='{gender}',{T_SHIRT_COL}='{t_shirt_size.lower()}',{BIRTHDAY_COL}='{birthday}',{DOCTOR_NAME_COL}='{doctor_name}',{DOCTOR_PHONE_COL}='{doctor_phone}',{EMERGENCY_CONTACT_1_NAME_COL}='{emergency_contact_1_name}',{EMERGENCY_CONTACT_1_PHONE_COL}='{emergency_contact_1_phone}',{EMERGENCY_CONTACT_2_NAME_COL}='{emergency_contact_2_name}',{EMERGENCY_CONTACT_2_PHONE_COL}='{emergency_contact_2_phone}',{ALLERGIES_COL}='{allergies}',{MENTAL_ISSUES_COL}='{mental_issues}',{CHRONICAL_DISEASES_COL}='{chronical_diseases}',{MEDICATION_COL}='{medication}',{ZIMMERWUNSCH_COL}='{zimmerwunsch}',{COMMENT_COL}='{comment}',{TETANUS_IMPFUNG_COL}={tetanus},{ZECKENIMPFUNG_COL}={zecken},{BUS_COL}={bus},{BUS_MUENSTER_COL}={bus_muenster},{SPONSORED_COL}={sponsored},{BALANCE_COL}={balance},{STAFF_COL}={staff},{CONFIRMED_COL}={confirmed},{EXTRA_DISCOUNT_COL}={support},{SWIM_CONFIRM_COL}={swim_confirm},{KITCHEN_TEAM_COL}={kitchen} WHERE {KEY_COL} = {current_id}"
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

def rechnung_view(primary=0):
    st.sidebar.markdown("---")
    only_no_invoice = st.sidebar.checkbox("Zeig nur Teilnehmer, welche noch keine Rechnung bekommen haben", True)
    if only_no_invoice:
        data_selected = data_total[data_total[DATE_INVOICE_COL].isna()]
        current_id = st.sidebar.selectbox("Namen auswählen", data_selected[KEY_COL], format_func=render_name, index=primary)
    else:
        current_id = st.sidebar.selectbox("Namen auswählen", data_total[KEY_COL], format_func=render_name, index=primary)


    current_data = data_total[data_total[KEY_COL]==current_id]

    try:
        current_name = current_data[FIRST_NAME_COL].values[0] + " " + current_data[LAST_NAME_COL].values[0]
    except IndexError:
        st.markdown("Keine Daten zum Anzeigen")
        return

    st.markdown(f"### Rechnung von {current_name} ({current_id})")

    if st.button(f"Rechnung für {current_name} erstellen und versenden"):
        if current_data[CONFIRMED_COL].values[0] == 1:
            if current_data[FORM_FOR_CHILD_COL].values[0]:
                # Invoice at Parent
                invoice_name = current_data[PARENT_FIRST_NAME_COL].values[0] + " " + current_data[PARENT_LAST_NAME_COL].values[0]
                email_main = current_data[PARENT_EMAIL_COL].values[0]
                is_parent = True
            else:
                invoice_name = current_name
                email_main = current_data[EMAIL_COL].values[0]
                is_parent = False

            _, freizeitkosten, buskosten, discount, discount_code = calc_kosten(current_data)

            data_invoice = {
                "current_id": current_id,
                "invoice_name": invoice_name,
                "name_teilnehmer": current_name,
                "address_street": current_data[ADDRESS_COL].values[0],
                "address_zip": current_data[ZIP_COL].values[0],
                "address_city": current_data[CITY_COL].values[0],
                "address_country": current_data[COUNTRY_COL].values[0],
                "freizeit_kosten": freizeitkosten,
                "busfahrt_kosten": buskosten,
                "discount": -discount,
                "discount_code": discount_code
            }
            file_name_pdf = f"JF2023-{current_id:03}.pdf"
            pdf = invoice_creator.create_pdf(**data_invoice)
            pdf_bytes = pdf.output(file_name_pdf, "S").encode('latin-1')
            pdf_attachment = officeHelper.draft_attachment(file_name_pdf, pdf_bytes)

            if officeHelper.send_email_rechnung(email_main, invoice_name, pdf_attachment, is_parent):
                st.write("Rechnung wurde per E-Mail versandt")
                update_invoice_cursor = connection.cursor()
                update_invoice_query = f"UPDATE Anmeldung SET {DATE_INVOICE_COL}='{datetime.datetime.now()}' WHERE {KEY_COL} = {current_id}"
                update_invoice_cursor.execute(update_invoice_query)
                connection.commit()
                st.write(f"{update_invoice_cursor.rowcount} Datensatz aktualisiert")
        else:
            st.write("Rechnung konnte nicht ausgestellt werden, da Teilnehmer nicht bestätigt")

def buchhaltung_view():
    st.markdown("### Buchhaltung Upload")
    uploaded_file = st.file_uploader("Hier Liste der aktuellen Buchungen hochladen", ".csv", False)

    if uploaded_file is not None:
        uploaded_data = pd.read_csv(uploaded_file, sep=";", decimal=",", encoding="cp1252", header=3)
        relevant_data = uploaded_data[uploaded_data["Verwendungszweck"].str.contains("JF2023-", case=False, na=False)]

        if len(relevant_data) == 0:
            st.markdown("In dieser Datei gibt es keine Daten, welche eingetragen werden sollten.")
        for i in range(len(relevant_data)):
            verwendungszweck = relevant_data.iloc[i,8]
            betrag = relevant_data.iloc[i,11]
            current_id = int(re.findall(r"JF2023-(\d\d\d)", verwendungszweck)[0])
            current_data = data_total[data_total[KEY_COL]==current_id]

            if len(current_data) == 0:
                st.markdown(f"Es konnte keine Person zu diesem Verwendungszweck zugeordnet werden: *{verwendungszweck}*")
            else:
                buchhaltung_cursor = connection.cursor()
                current_balance = current_data[BALANCE_COL]
                new_balance = current_balance + betrag
                buchhaltung_query = f"UPDATE {BALANCE_COL}={new_balance} WHERE id={current_id}"
                buchhaltung_cursor.execute(buchhaltung_query)
                connection.commit()
                st.write(f"{buchhaltung_cursor.rowcount} Datensatz aktualisiert für {current_data[FIRST_NAME_COL]} {current_data[LAST_NAME_COL]} mit einem Betrag von {babel.numbers.format_currency(betrag, 'EUR', 'de_DE')}")


def finanzen_view():
    st.markdown("### Übersicht Finanzen")

    finanz_calc = [calc_kosten(data_total.iloc[i,:].T) for i in range(len(data_total))]
    total_calc = [c[0] for c in finanz_calc]

    finanz_data = pd.DataFrame({
        "Name": data_total[FIRST_NAME_COL] + " " + data_total[LAST_NAME_COL],
        "MA": data_total[STAFF_COL]==1,
        "Küche": data_total[KITCHEN_TEAM_COL]==1,
        "Geschw.": data_total[SIBLING_COL]==1,
        "Free": data_total[SPONSORED_COL]==1,
        "Bus": data_total[BUS_COL]==1,
        "Kosten": total_calc,
        "Überwiesen": data_total[BALANCE_COL],
        "Rechnung":data_total[DATE_INVOICE_COL].isna()
        #"Betrag ausstehend": data_total[BALANCE_COL].values - finanz_calc
    })

    finanz_data["Ausstehend"] = finanz_data["Kosten"] - finanz_data["Überwiesen"]

    finanz_data["Ausstehend"] = finanz_data["Ausstehend"].apply(render_money)
    finanz_data["Kosten"] = finanz_data["Kosten"].apply(render_money)
    finanz_data["Überwiesen"] = finanz_data["Überwiesen"].apply(render_money)
    finanz_data = finanz_data[finanz_data["Rechnung"] == 1]
    finanz_data.drop(columns=["Rechnung"], inplace=True)
    st.dataframe(finanz_data)

    st.markdown("### Zusammenfassung")
    finanz_data_sum = pd.DataFrame({
        "Summe Kosten": finanz_data["Kosten"].sum(),
        "Summe Überwiesen": finanz_data["Überwiesen"].sum(),
        "Summe Ausstehend": finanz_data["Ausstehend"].sum(),
        "Anzahl MA": finanz_data["MA"].sum(),
        "Anzahl Küche": finanz_data["Küche"].sum(),
    }, index=[0])

    st.write(finanz_data_sum)

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
    "Rechnungen": rechnung_view,
    "Buchhaltung": buchhaltung_view,
    "Finanzübersicht": finanzen_view,
}

view = st.sidebar.radio("Ansicht", views)

views[view]()

officeHelper.main_loop()

#st.write(st.session_state)
connection.close()
