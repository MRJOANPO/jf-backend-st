import datetime
import re

import streamlit as st
import mysql.connector
import pandas as pd
import babel.numbers

import invoice_creator
import officeHelper

MONEY_EARLY = 348
MONEY_LATE = 398
MONEY_BUS = 0
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
EXTERNAL_STAFF_COL = "external_staff"
KITCHEN_TEAM_COL = "kitchen_team"
CONFIRMED_COL = "confirmed"
DATE_INVOICE_COL = "last_rechnung_datetime"
SWIM_CONFIRM_COL = "swim_confirm"
LEAVE_CONFIRM_COL = "leave_confirm"
EXTRA_DISCOUNT_COL = "extra_discount"
DELETED_COL = "deleted"

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
        discount += -current_data[EXTRA_DISCOUNT_COL]
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

    if current_data[EXTERNAL_STAFF_COL]:
        discount = -total_cost
        discount_code += ("Externer Mitarbeiter, ")

    if discount_code != "":
        discount_code = discount_code.rstrip(", ")

    total_cost += discount

    return (total_cost, freizeitkosten, buskosten, discount, discount_code)

def calc_balance(current_data):
    total_kosten, _, _, _, _  = calc_kosten(current_data)

    try:
        current_data = current_data.iloc[0,:]
    except pd.errors.IndexingError:
        pass

    return total_kosten - current_data[BALANCE_COL]

def render_money(number):
    return babel.numbers.format_currency(number, "EUR", locale="de_DE")

def privileges_checker(username:str, password:str) -> int:
    regex = re.compile('[^a-zA-Z]')
    username = regex.sub('', username)
    username = username.lower()

    login_cursor = connection.cursor()
    login_query = f"SELECT * FROM Users WHERE `username`='{username}'"
    login_cursor.execute(login_query)
    login_data = login_cursor.fetchall()
    if len(login_data) == 1:
        correct_password = login_data[0][2]
        if correct_password == password:
            privilege_id =  login_data[0][3]
            return privilege_id

    if username != "":
        st.write("Falscher Benutzer oder falsches Passwort")
    return 0

@st.cache_data
def convert_dataframe(df: pd.DataFrame):
    return df.to_csv(
        index=False,
        sep=";",
        decimal=",",
        encoding="utf8"
    ).encode("utf8")

def calc_age(born: datetime.date):
    today = datetime.date.today()
    return today.year - born.year - ((today.month,
                                      today.day) < (born.month,
                                                    born.day))

def convert_bool_to_text(value:int) -> str:
    if value == 1:
        return "ja"

    return "nein"

def display_gender(value:str) -> str:
    if value == "w":
        return "weiblich"

    return "männlich"

def delete_person(current_id:int):
    delete_query = f"UPDATE Anmeldung SET {DELETED_COL}=1 WHERE id={current_id}"
    delete_cursor = connection.cursor()
    delete_cursor.execute(delete_query)
    connection.commit()
    st.write(f"{delete_cursor.rowcount} Datensatz gelöscht")
    st.experimental_rerun()

def send_zahlungserinnerung(current_data, current_id, current_name):
    if current_data[CONFIRMED_COL] == 1:
        if pd.isna(current_data[DATE_INVOICE_COL]) is False:
            if current_data[FORM_FOR_CHILD_COL]:
                            # Invoice at Parent
                invoice_name = current_data[PARENT_FIRST_NAME_COL] + " " + current_data[PARENT_LAST_NAME_COL]
                email_main = current_data[PARENT_EMAIL_COL]
                is_parent = True
            else:
                invoice_name = current_name
                email_main = current_data[EMAIL_COL]
                is_parent = False

            gesamt_kosten , freizeitkosten, _, discount, discount_code = calc_kosten(current_data)

            busfahrt = int(current_data[BUS_COL])==1

            data_invoice = {
                            "current_id": current_id,
                            "invoice_name": invoice_name,
                            "name_teilnehmer": current_name,
                            "address_street": current_data[ADDRESS_COL],
                            "address_zip": current_data[ZIP_COL],
                            "address_city": current_data[CITY_COL],
                            "address_country": current_data[COUNTRY_COL],
                            "freizeit_kosten": freizeitkosten,
                            "busfahrt_kosten": MONEY_BUS,
                            "busfahrt": busfahrt,
                            "discount": -discount,
                            "discount_code": discount_code
                        }
            file_name_pdf = f"JF2023-{current_id:03}.pdf"
            pdf = invoice_creator.create_pdf(**data_invoice)
            pdf_bytes = pdf.output(file_name_pdf, "S").encode('latin-1')
            pdf_attachment = officeHelper.draft_attachment(file_name_pdf, pdf_bytes)

            email_kosten_ausstehend = render_money(gesamt_kosten - current_data[BALANCE_COL])
            email_kosten_total = render_money(gesamt_kosten)
            email_kosten_erhalten = render_money(current_data[BALANCE_COL])

            if officeHelper.send_zahlungserinnerung(
                                email_main, invoice_name,
                                pdf_attachment,
                                is_parent,
                                email_kosten_erhalten,
                                email_kosten_ausstehend,
                                email_kosten_total
                            ):
                    st.write(f"Zahlungserinnerung für {current_name} wurde per E-Mail versandt")
        else:
            st.write("Zahlungserinnerung kann nicht ausgestellt werden, weil Teilnehmer noch nie eine Rechnung bekommen hat.")
    else:
        st.write("Rechnung konnte nicht ausgestellt werden, da Teilnehmer nicht bestätigt")

def get_first_emergency_contact(current_data):
    if current_data[FORM_FOR_CHILD_COL] == 1:
        # Return Erziehungsberechtigter
        return current_data[PARENT_FIRST_NAME_COL] + " " + current_data[PARENT_LAST_NAME_COL] + " (" + current_data[PARENT_PHONE_COL] + ")"

    return current_data[EMERGENCY_CONTACT_1_NAME_COL] + " (" + current_data[EMERGENCY_CONTACT_1_PHONE_COL] + ")"

def get_second_emergency_contact(current_data):
    if current_data[FORM_FOR_CHILD_COL] == 1:
        # Return Erziehungsberechtigter
        return current_data[EMERGENCY_CONTACT_1_NAME_COL] + " (" + current_data[EMERGENCY_CONTACT_1_PHONE_COL] + ")"

    return current_data[EMERGENCY_CONTACT_2_NAME_COL] + " (" + current_data[EMERGENCY_CONTACT_2_PHONE_COL] + ")"


############### Views ###############
def all_view():

    if not len(data_total) == 0:
        st.markdown("### Anzahl Anmeldungen")
        data_days = data_total.groupby(data_total[SIGN_UP_DATETIME].dt.date)[KEY_COL].count()
        data_days.rename("Anzahl", inplace=True)
        st.bar_chart(data_days)
        st.write(f"Anzahl Anmeldungen: {len(data_total)}")

        st.markdown("### Alter")
        ages_data = data_total[BIRTHDAY_COL].apply(calc_age)
        age_average_total = ages_data.mean()
        age_average_mitarbeiter = ages_data[(data_total[STAFF_COL]==1) | (data_total[EXTERNAL_STAFF_COL]==1) | (data_total[KITCHEN_TEAM_COL]==1)].mean()
        age_average_teilnehmer = ages_data[(data_total[STAFF_COL]==0) & (data_total[EXTERNAL_STAFF_COL]==0) & (data_total[KITCHEN_TEAM_COL]==0)].mean()
        ages_grouped = ages_data.groupby(ages_data).count()
        ages_grouped.rename("Alter", inplace=True)
        st.bar_chart(ages_grouped)
        st.markdown(f"**Durchschnitt**: {age_average_total:.1f} *(alle)*, {age_average_teilnehmer:.1f} *(Teilnehmer)*, {age_average_mitarbeiter:.1f} *(Mitarbeiter)*")

        st.markdown("### T-Shirt Größen")
        t_shirt_data = data_total.groupby(T_SHIRT_COL)[KEY_COL].count()
        t_shirt_data.rename("T-Shirt Größen", inplace=True)
        st.bar_chart(t_shirt_data)

        st.markdown("### Geschlecht in %")
        staff_only_data = data_total[(data_total[STAFF_COL]==1) | (data_total[EXTERNAL_STAFF_COL]==1) | (data_total[KITCHEN_TEAM_COL])==1]
        teilnehmer_only_data = data_total[(data_total[STAFF_COL]==0) & (data_total[EXTERNAL_STAFF_COL]==0) & (data_total[KITCHEN_TEAM_COL])==0]
        gender_data_staff = staff_only_data.groupby(GENDER_COL)[KEY_COL].count()/staff_only_data.shape[0]*100
        gender_data_teilnehmer = teilnehmer_only_data.groupby(GENDER_COL)[KEY_COL].count()/teilnehmer_only_data.shape[0]*100

        gender_data_staff.rename("Mitarbeiter", inplace=True)
        gender_data_teilnehmer.rename("Teilnehmer", inplace=True)

        gender_data = pd.DataFrame([gender_data_teilnehmer, gender_data_staff])
        gender_data.rename(columns={"m":"Männlich", "w":"Weiblich"}, inplace=True)
        st.bar_chart(gender_data)

        st.markdown("### Mitarbeiter und Teilnehmer")
        count_ma = len(data_total[data_total[STAFF_COL]==1])
        count_ext_ma = len(data_total[data_total[EXTERNAL_STAFF_COL]==1])
        count_kitchen = len(data_total[data_total[KITCHEN_TEAM_COL]==1])
        count_teilnehmer = len(data_total) - count_ma - count_ext_ma - count_kitchen
        data_aufteilung = pd.DataFrame(
            {"Aufteilung": [count_teilnehmer, count_ma, count_ext_ma, count_kitchen]},
            index=["Teilnehmer", "Mitarbeiter", "Externe Mitarbeiter", "Küchenteam"]
        )
        st.bar_chart(data_aufteilung)

        st.markdown("### Alle Daten")
        st.dataframe(data_total)
        csv = convert_dataframe(data_total)
        st.download_button(
            "Alle Daten herunterladen",
            csv,
            f"JugendfreizeitExport{datetime.datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    else:
        st.write("Momentan sind keine Daten vorhanden")

def confirm_signup(primary=0):
    st.sidebar.markdown("---")
    only_not_approved = st.sidebar.checkbox("Zeig nur Teilnehmer, welche noch nicht bestätigt wurden", True)
    if only_not_approved:
        data_selected = data_total[data_total[CONFIRMED_COL]==0]
        current_id = st.sidebar.selectbox("Namen auswählen", data_selected[KEY_COL], format_func=render_name, index=primary)
    else:
        current_id = st.sidebar.selectbox("Namen auswählen", data_total[KEY_COL], format_func=render_name, index=primary)

    current_data = data_total[data_total[KEY_COL]==current_id]

    try:
        current_name = current_data[FIRST_NAME_COL].values[0] + " " + current_data[LAST_NAME_COL].values[0]
    except IndexError:
        st.markdown("Keine Daten zum Anzeigen")
        return

    st.markdown(f"### Antrag auf Teilnahme für {current_name} ({current_id})")

    filled_out_by_parent = current_data[FORM_FOR_CHILD_COL].values[0] == 1

    if filled_out_by_parent:
        st.markdown("#### Daten der Eltern")
        st.write(f"**Vorname:** {current_data[PARENT_FIRST_NAME_COL].values[0]}")
        st.write(f"**Nachname:** {current_data[PARENT_LAST_NAME_COL].values[0]}")
        st.write(f"**E-Mail:** {current_data[PARENT_EMAIL_COL].values[0]}")
        st.write(f"**Telefon:** {current_data[PARENT_PHONE_COL].values[0]}")
        st.write(f"**Adresse:** {current_data[ADDRESS_COL].values[0]}, {current_data[ZIP_COL].values[0]} {current_data[CITY_COL].values[0]}, {current_data[COUNTRY_COL].values[0]}")
        st.write(f"**Darf schwimmen gehen:** {convert_bool_to_text(current_data[SWIM_CONFIRM_COL].values[0])}")
        st.write(f"**Darf das Gelände verlassen:** {convert_bool_to_text(current_data[LEAVE_CONFIRM_COL].values[0])}")

    st.markdown("#### Daten Teilnehmer")
    st.write(f"**Vorname:** {current_data[FIRST_NAME_COL].values[0]}")
    st.write(f"**Nachname:** {current_data[LAST_NAME_COL].values[0]}")
    st.write(f"**Geschlecht:** {display_gender(current_data[GENDER_COL].values[0])}")
    st.write(f"**E-Mail:** {current_data[EMAIL_COL].values[0]}")
    st.write(f"**Telefonnummer:** {current_data[PHONE_COL].values[0]}")

    if not filled_out_by_parent:
        st.write(f"**Adresse:** {current_data[ADDRESS_COL].values[0]}, {current_data[ZIP_COL].values[0]} {current_data[CITY_COL].values[0]}, {current_data[COUNTRY_COL].values[0]}")

    st.write(f"**T-Shirt-Size:** {current_data[T_SHIRT_COL].values[0]}")
    st.write(f"**Geburtstag:** {current_data[BIRTHDAY_COL].values[0]} ({current_data[BIRTHDAY_COL].apply(calc_age).values[0]} Jahre)")

    st.markdown("#### Medizinische Daten")
    st.write(f"**Arzt Name:** {current_data[DOCTOR_NAME_COL].values[0]}")
    st.write(f"**Arzt Telefon:** {current_data[DOCTOR_PHONE_COL].values[0]}")
    st.write(f"**Notfallkontakt 1 Name:** {current_data[EMERGENCY_CONTACT_1_NAME_COL].values[0]}")
    st.write(f"**Notfallkontakt 1 Telefon:** {current_data[EMERGENCY_CONTACT_1_PHONE_COL].values[0]}")
    if not filled_out_by_parent:
        st.write(f"**Notfallkontakt 2 Name:** {current_data[EMERGENCY_CONTACT_2_NAME_COL].values[0]}")
        st.write(f"**Notfallkontakt 2 Telefon:** {current_data[EMERGENCY_CONTACT_2_PHONE_COL].values[0]}")
    st.write(f"**Allergien:** {current_data[ALLERGIES_COL].values[0]}")
    st.write(f"**Geistige oder soziale Beeinträchtigungen:** {current_data[MENTAL_ISSUES_COL].values[0]}")
    st.write(f"**Chronische Erkrankungen:** {current_data[CHRONICAL_DISEASES_COL].values[0]}")
    st.write(f"**Regelmäßige Medikamenteneinnahme:** {current_data[MEDICATION_COL].values[0]}")
    st.write(f"**Tetanus Impfung:** {convert_bool_to_text(current_data[TETANUS_IMPFUNG_COL].values[0])}")
    st.write(f"**Zecken Impfung:** {convert_bool_to_text(current_data[ZECKENIMPFUNG_COL].values[0])}")

    st.markdown("#### Busfahrt")
    st.write(f"**Mit Busfahrt:** {convert_bool_to_text(current_data[BUS_COL].values[0])}")
    st.write(f"**Mit Buszustieg in Münster:** {convert_bool_to_text(current_data[BUS_MUENSTER_COL].values[0])}")

    st.markdown("#### Anmerkungen")
    st.write(f"**Zimmerwunsch:** {current_data[ZIMMERWUNSCH_COL].values[0]}")
    st.write(f"**Kommentar:** {current_data[COMMENT_COL].values[0]}")

    with st.form("Anmeldung bestätigen"):
        confirmed = st.checkbox(f"Teilnahme für {current_name} bestätigt", current_data[CONFIRMED_COL].values[0])
        externe_mitarbeiter = st.checkbox(f"Externer Mitarbeiter", current_data[EXTERNAL_STAFF_COL].values[0])
        mitarbeiter = st.checkbox(f"Mitarbeiter", current_data[STAFF_COL].values[0])
        kuechenteam = st.checkbox(f"Küchenteam", current_data[KITCHEN_TEAM_COL].values[0])
        kostenlos = st.checkbox(f"Kostenlos", current_data[SPONSORED_COL].values[0])
        geschwister = st.checkbox(f"Geschwisterkind", current_data[SIBLING_COL].values[0])
        if st.form_submit_button("Absenden"):
            confirm_query = f"UPDATE Anmeldung SET {CONFIRMED_COL}={confirmed}, {MITARBEITER_COL}={mitarbeiter}, {EXTERNAL_STAFF_COL}={externe_mitarbeiter}, {KITCHEN_TEAM_COL}={kuechenteam}, {SPONSORED_COL}={kostenlos}, {SIBLING_COL}={geschwister} WHERE `id`={current_id}"
            confirm_cursor = connection.cursor()
            confirm_cursor.execute(confirm_query)
            connection.commit()
            st.write(f"{confirm_cursor.rowcount} Datensatz aktualisiert")

    if st.button(f"Anmeldung von {current_name} löschen"):
        delete_person(current_id)

    if st.button(f"Rechnung für {current_name} versenden"):
        if "Rechnungen" in views:
            send_invoice(current_id, current_data, current_name)
        else:
            st.write("Du besitzt nicht die Rechte zum bearbeiten")

def single_edit(primary=0):
    if primary == 0:
        st.sidebar.markdown("---")
        current_id = st.sidebar.selectbox("Namen auswählen", data_total[KEY_COL], format_func=render_name, index=primary)
    else:
        current_id = primary
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
        phone = st.text_input("Telefonnummer", current_data[PHONE_COL].values[0])
        parent_email = st.text_input("E-Mail Eltern", current_data[PARENT_EMAIL_COL].values[0])
        parent_phone = st.text_input("Telefon Eltern", current_data[PARENT_PHONE_COL].values[0])
        address = st.text_input("Adresse", current_data[ADDRESS_COL].values[0])
        plz = st.number_input("PLZ", value=current_data[ZIP_COL].values[0])
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
        leave_confirm = st.checkbox("Darf das Gelände verlassen", current_data[LEAVE_CONFIRM_COL].values[0])
        bus = st.checkbox("Mit Busfahrt", current_data[BUS_COL].values[0])
        bus_muenster = st.checkbox("Mit Buszustieg in Münster", current_data[BUS_MUENSTER_COL].values[0])

        balance = st.number_input("Geldeingang", value=current_data[BALANCE_COL].values[0])
        support = st.number_input("Unterstützung", value=current_data[EXTRA_DISCOUNT_COL].values[0])
        sibling_coming = st.checkbox("Geschwisterrabatt", current_data[SIBLING_COL].values[0])
        sponsored = st.checkbox("Kostenlos", current_data[SPONSORED_COL].values[0])
        staff = st.checkbox("Mitarbeiter", current_data[STAFF_COL].values[0])
        external_staff = st.checkbox("Externer Mitarbeiter", current_data[EXTERNAL_STAFF_COL].values[0])
        kitchen = st.checkbox("Küchenteam", current_data[KITCHEN_TEAM_COL].values[0])
        confirmed = st.checkbox("Teilnahme bestätigt", current_data[CONFIRMED_COL].values[0])

        if st.form_submit_button("Daten speichern"):
            update_query = f"UPDATE Anmeldung SET {FIRST_NAME_COL}='{first_name}', {LAST_NAME_COL}='{last_name}',{FORM_FOR_CHILD_COL}={form_for_child},{PARENT_FIRST_NAME_COL}='{parent_first_name}',{PARENT_LAST_NAME_COL}='{parent_last_name}',{PHONE_COL}='{phone}',{EMAIL_COL}='{email}',{PARENT_EMAIL_COL}='{parent_email}',{PARENT_PHONE_COL}='{parent_phone}',{ADDRESS_COL}='{address}',{ZIP_COL}={plz},{CITY_COL}='{city}',{COUNTRY_COL}='{country}',{GENDER_COL}='{gender}',{T_SHIRT_COL}='{t_shirt_size.lower()}',{BIRTHDAY_COL}='{birthday}',{DOCTOR_NAME_COL}='{doctor_name}',{DOCTOR_PHONE_COL}='{doctor_phone}',{EMERGENCY_CONTACT_1_NAME_COL}='{emergency_contact_1_name}',{EMERGENCY_CONTACT_1_PHONE_COL}='{emergency_contact_1_phone}',{EMERGENCY_CONTACT_2_NAME_COL}='{emergency_contact_2_name}',{EMERGENCY_CONTACT_2_PHONE_COL}='{emergency_contact_2_phone}',{ALLERGIES_COL}='{allergies}',{MENTAL_ISSUES_COL}='{mental_issues}',{CHRONICAL_DISEASES_COL}='{chronical_diseases}',{MEDICATION_COL}='{medication}',{ZIMMERWUNSCH_COL}='{zimmerwunsch}',{COMMENT_COL}='{comment}',{TETANUS_IMPFUNG_COL}={tetanus},{ZECKENIMPFUNG_COL}={zecken},{BUS_COL}={bus},{BUS_MUENSTER_COL}={bus_muenster},{SPONSORED_COL}={sponsored},{BALANCE_COL}={balance},{STAFF_COL}={staff},{CONFIRMED_COL}={confirmed},{EXTRA_DISCOUNT_COL}={support},{SWIM_CONFIRM_COL}={swim_confirm},{KITCHEN_TEAM_COL}={kitchen},{EXTERNAL_STAFF_COL}={external_staff},{LEAVE_CONFIRM_COL}={leave_confirm},{SIBLING_COL}={sibling_coming} WHERE {KEY_COL} = {current_id}"
            update_cursor = connection.cursor()
            update_cursor.execute(update_query)
            connection.commit()
            st.write(f"{update_cursor.rowcount} Datensatz aktualisiert")

    if st.button("Löschen"):
        delete_person(current_id)

def rechnung_view(primary=0):
    st.sidebar.markdown("---")
    only_no_invoice = st.sidebar.checkbox("Zeig nur Teilnehmer, welche noch keine Rechnung bekommen haben und bestätigt wurden", True)
    if only_no_invoice:
        data_selected = data_total[data_total[DATE_INVOICE_COL].isna() & data_total[CONFIRMED_COL] == True]
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
        send_invoice(current_id, current_data, current_name)

def send_invoice(current_id, current_data, current_name):
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

        _, freizeitkosten, _, discount, discount_code = calc_kosten(current_data)

        busfahrt = int(current_data[BUS_COL].values[0])==1

        data_invoice = {
                "current_id": current_id,
                "invoice_name": invoice_name,
                "name_teilnehmer": current_name,
                "address_street": current_data[ADDRESS_COL].values[0],
                "address_zip": current_data[ZIP_COL].values[0],
                "address_city": current_data[CITY_COL].values[0],
                "address_country": current_data[COUNTRY_COL].values[0],
                "freizeit_kosten": freizeitkosten,
                "busfahrt_kosten": MONEY_BUS,
                "busfahrt": busfahrt,
                "discount": -discount,
                "discount_code": discount_code
            }
        file_name_pdf = f"JF2023-{current_id:03}.pdf"
        pdf = invoice_creator.create_pdf(**data_invoice)
        pdf_bytes = pdf.output(file_name_pdf, "S").encode('latin-1')
        pdf_attachment = officeHelper.draft_attachment(file_name_pdf, pdf_bytes)

        if officeHelper.send_email_rechnung(email_main, invoice_name, pdf_attachment, is_parent, current_id):
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

    with st.form("buchhaltung-form", clear_on_submit=True):
        uploaded_file = st.file_uploader("Hier Liste der aktuellen Buchungen hochladen", ".csv", False)
        submitted = st.form_submit_button("Jetzt Überweisungen analysieren und Teilnehmerbeträge schreiben")

        if submitted and uploaded_file is not None:
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
                    # new_balance = current_balance.values[0] + betrag # uncomment to activate adding
                    new_balance = betrag
                    buchhaltung_query = f"UPDATE Anmeldung SET {BALANCE_COL}={new_balance} WHERE id={current_id}"

                    buchhaltung_cursor.execute(buchhaltung_query)
                    connection.commit()
                    st.write(f"{buchhaltung_cursor.rowcount} Datensatz aktualisiert für {current_data[FIRST_NAME_COL].values[0]} {current_data[LAST_NAME_COL].values[0]} mit einem Betrag von {babel.numbers.format_currency(betrag, 'EUR', locale='de_DE')}")

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
        "Ext": data_total[EXTERNAL_STAFF_COL]==1,
        "Bus": data_total[BUS_COL]==1,
        "Kosten": total_calc,
        "Überwiesen": data_total[BALANCE_COL],
        "Rechnung":data_total[DATE_INVOICE_COL].isna()
        #"Betrag ausstehend": data_total[BALANCE_COL].values - finanz_calc
    })

    finanz_data["Ausstehend"] = finanz_data["Kosten"] - finanz_data["Überwiesen"]
    finanz_data = finanz_data[finanz_data["Rechnung"] == 0]
    finanz_data.drop(columns=["Rechnung"], inplace=True)
    finanz_data_raw = finanz_data.copy()

    finanz_data["Ausstehend"] = finanz_data["Ausstehend"].apply(render_money)
    finanz_data["Kosten"] = finanz_data["Kosten"].apply(render_money)
    finanz_data["Überwiesen"] = finanz_data["Überwiesen"].apply(render_money)
    st.dataframe(finanz_data)

    st.markdown("### Zusammenfassung")
    finanz_data_sum = pd.DataFrame({
        "Summe Kosten": babel.numbers.format_currency(finanz_data_raw["Kosten"].sum(), "EUR", locale="de_DE"),
        "Summe Überwiesen": babel.numbers.format_currency(finanz_data_raw["Überwiesen"].sum(), "EUR", locale="de_DE"),
        "Summe Ausstehend": babel.numbers.format_currency(finanz_data_raw["Ausstehend"].sum(), "EUR", locale="de_DE")
    }, index=[0])

    st.write(finanz_data_sum)

    st.markdown("### Leute, die zu viel bezahlt haben:")
    selected_data = data_total[(data_total[DATE_INVOICE_COL].isna() == False) & (data_total[CONFIRMED_COL]==1) & (data_total.apply(calc_balance, axis=1) < 0)]
    if len(selected_data) == 0:
        st.write("Keiner")
    else:
        for _, current_data in selected_data.iterrows():
            balance = calc_balance(current_data)
            current_name = f"{current_data[FIRST_NAME_COL]} {current_data[LAST_NAME_COL]} ({current_data[KEY_COL]})"
            st.write(f"{current_name} mit {render_money(balance)}")

def need_for_login_view():
    st.write("Anmeldung")
    with st.form("Login"):
        username = st.text_input(label="Benutzername")
        password = st.text_input(label="Passwort", type="password", autocomplete="password")
        if st.form_submit_button("Einloggen"):
            st.session_state["privileges"] = privileges_checker(username, password)
            if st.session_state["privileges"] != 0:
                st.experimental_rerun()

def zahlungserinnuerung_view():
    st.markdown("### Zahlungserinnerung")
    selected_data = data_total[(data_total[DATE_INVOICE_COL].isna() == False) & (data_total[CONFIRMED_COL]==1) & (data_total.apply(calc_balance, axis=1) > 0)]
    # st.dataframe(selected_data)

    st.markdown("### Einzeln")
    for current_row, current_data in selected_data.iterrows():
        current_balance = calc_balance(current_data)
        current_id = current_data[KEY_COL]
        with st.form(f"{current_row}"):
            current_name = f"{current_data[FIRST_NAME_COL]} {current_data[LAST_NAME_COL]}"
            st.write(f"{current_name} ({current_data[KEY_COL]}) noch {render_money(current_balance)}")
            if st.form_submit_button(f"Zahlungserinnerung für {current_name} senden"):
                send_zahlungserinnerung(current_data, current_id, current_name)

    st.markdown("#### Alle Senden")
    with st.form("send_all_zahlungserinnerung"):
        if st.form_submit_button("Zahlungserinnerung an alle senden"):
            for current_row, current_data in selected_data.iterrows():
                current_balance = calc_balance(current_data)
                current_id = current_data[KEY_COL]
                current_name = f"{current_data[FIRST_NAME_COL]} {current_data[LAST_NAME_COL]}"
                send_zahlungserinnerung(current_data, current_id, current_name)

def medical_view():
    confirmed_people = data_total[data_total[CONFIRMED_COL]==1]

    medical_data = pd.DataFrame({
        "Vorname": confirmed_people[FIRST_NAME_COL],
        "Nachname": confirmed_people[LAST_NAME_COL],
        "Alter": confirmed_people[BIRTHDAY_COL].apply(calc_age),
        "Geschlecht": confirmed_people[GENDER_COL],
        "Arzt": confirmed_people[DOCTOR_NAME_COL] + " (" + confirmed_people[DOCTOR_PHONE_COL] + ")",
        "Notfallkontakt 1": confirmed_people.apply(get_first_emergency_contact, axis=1),
        "Notfallkontakt 2": confirmed_people.apply(get_second_emergency_contact, axis=1),
        "Allergien": confirmed_people[ALLERGIES_COL],
        "Geistige oder soziale Beeinträchtigungen": confirmed_people[MENTAL_ISSUES_COL],
        "Chronische Erkrankungen": confirmed_people[CHRONICAL_DISEASES_COL],
        "Regelmäßige Medikamenteneinnahme": confirmed_people[MEDICATION_COL],
        "Tetanus Impfung": confirmed_people[TETANUS_IMPFUNG_COL] == 1,
        "Zecken Impfung": confirmed_people[ZECKENIMPFUNG_COL] == 1,
    })

    st.dataframe(medical_data, height=(medical_data.shape[0]+1)*35)
    csv = convert_dataframe(medical_data)
    st.download_button(
        "Alle medizinischen Daten herunterladen",
        csv,
        f"JF-MedicalData{datetime.datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv"
    )

def kitchen_view():
    kitchen_people = data_total[(data_total[CONFIRMED_COL]==1) & (data_total[ALLERGIES_COL] != "")]

    kitchen_data = pd.DataFrame({
        "Vorname": kitchen_people[FIRST_NAME_COL],
        "Nachname": kitchen_people[LAST_NAME_COL],
        "Alter": kitchen_people[BIRTHDAY_COL].apply(calc_age),
        "Geschlecht": kitchen_people[GENDER_COL],
        "Allergien": kitchen_people[ALLERGIES_COL]
    })

    st.dataframe(kitchen_data, height=(kitchen_data.shape[0] + 1)*35) # +1 for headline
    csv = convert_dataframe(kitchen_data)
    st.download_button(
        "Alle medizinischen Daten herunterladen",
        csv,
        f"JF-MedicalData{datetime.datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv"
    )

def header_info():
    count_waiting_for_confirm = len(data_total[data_total[CONFIRMED_COL]==0])
    count_waiting_for_invoice = len(data_total[data_total[DATE_INVOICE_COL].isna() & (data_total[CONFIRMED_COL]==1)])
    if count_waiting_for_invoice + count_waiting_for_confirm > 0:
        st.warning(f"Es warten noch {count_waiting_for_confirm} Teilnehmer auf Bestätigung und {count_waiting_for_invoice} Teilnehmer auf das zusenden der Rechnung", icon="📋")
    else:
        st.success("Super! Alles du hast keine offenen Anmeldungen", icon="🥳")

st.markdown("# JF 2023 Dashboard")

connection = mysql.connector.connect(
    host=st.secrets["DATABASE_HOST"],
    port=st.secrets["DATABASE_PORT"],
    user=st.secrets["DATABASE_USER"],
    password=st.secrets["DATABASE_PASSWORD"],
    database=st.secrets["DATABASE_NAME"]
)
get_all_query = "SELECT * FROM `Anmeldung` WHERE deleted = 0"
if  "privileges" not in st.session_state:
    st.session_state["privileges"] = 0

if st.session_state["privileges"] == 1:
    data_total = pd.read_sql(get_all_query, connection)
    header_info()
    views = {
        "Übersicht": all_view,
        "Teilnahme bestätigen": confirm_signup,
        "Bearbeiten": single_edit,
        "Rechnungen": rechnung_view,
        "Zahlungserinnerung": zahlungserinnuerung_view,
        "Buchhaltung": buchhaltung_view,
        "Finanzübersicht": finanzen_view,
        "Medizinische Daten": medical_view,
        "Küche Daten":kitchen_view
    }
elif st.session_state["privileges"] == 2:
    data_total = pd.read_sql(get_all_query, connection)
    views = {
        "Übersicht": all_view,
        "Buchhaltung": buchhaltung_view,
        "Finanzübersicht": finanzen_view,
    }
elif st.session_state["privileges"] == 3:
    data_total = pd.read_sql(get_all_query, connection)
    views = {
        "Medizinische Daten": medical_view
    }
elif st.session_state["privileges"] == 4:
    data_total = pd.read_sql(get_all_query, connection)
    views = {
        "Küche Daten": medical_view
    }
else:
    views = {
        "Einloggen": need_for_login_view,
    }

view = st.sidebar.radio("Ansicht", views)

views[view]()

officeHelper.main_loop()

#st.write(st.session_state)
connection.close()
