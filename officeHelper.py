import base64
import requests
import streamlit as st

OFFICE_TOKEN_VALUE = st.secrets["OFFICE"]["CLIENT_SECRET"]
OFFICE_APP_ID = st.secrets["OFFICE"]["CLIENT_APP_ID"]
SCOPES = ["User.Read", "Mail.Send"]
TENANT = st.secrets["OFFICE"]["TENANT"]
AUTHORITY_URL = f"https://login.microsoftonline.com/{TENANT}/"
START_POINT = "https://graph.microsoft.com/v1.0/"
NODE_EMAIL = "me/sendMail"
EMAIL_URL = START_POINT + NODE_EMAIL
REDIRECT_URL = st.secrets["OFFICE"]["REDIRECT_URL"]
# REDIRECT_URL = "http://localhost:8501/" # uncomment for local development
AUTO_SIGN_IN = False
AGB_FILE = "ZusatzbedingungenundInformationenRockSolidJugendfreizeit.pdf"

def draft_attachment(file_name, file_bytes):
    media_content = base64.b64encode(file_bytes)

    data_body = {
        '@odata.type': '#microsoft.graph.fileAttachment',
        'contentBytes': media_content.decode('utf-8'),
        'name': file_name
    }
    return data_body

def draft_agb_attachment():
    with open(AGB_FILE, "rb") as agb_bytes:
        return draft_attachment(AGB_FILE, agb_bytes.read())

def send_to_authorize():
    login_url = f"{AUTHORITY_URL}oauth2/v2.0/authorize"

    # Authorization
    params_authorize = {
        "client_id": OFFICE_APP_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URL,
        "scope": " ".join(SCOPES),
        "response_mode": "query"
    }

    authorization_request_url = requests.get(url=login_url, params=params_authorize, timeout=100).url
    #webbrowser.open(authorization_request_url)
    st.markdown(f"[Erneut Autorisieren]({authorization_request_url})", unsafe_allow_html=True)

def set_authorization_key():
    query_params = st.experimental_get_query_params()
    if "code" in query_params.keys():
        try:
            current_auth_code = st.session_state["auth_code"]
        except KeyError:
            current_auth_code = "x"

        if not current_auth_code == query_params["code"]:
            st.session_state["auth_code"] = query_params["code"]
            set_access_token()
    else:
        if "auth_code" not in st.session_state.keys():
            if AUTO_SIGN_IN:
                send_to_authorize()

def set_access_token():
    token_url = f"{AUTHORITY_URL}oauth2/v2.0/token"
    token_post = {
        "client_id": OFFICE_APP_ID,
        "scope": " ".join(SCOPES),
        "code": st.session_state["auth_code"],
        "redirect_uri": REDIRECT_URL,
        "grant_type": "authorization_code",
        "client_secret": OFFICE_TOKEN_VALUE
    }

    response = requests.post(token_url, data=token_post, timeout=1000).json()
    try:
        st.session_state["access_token"] = response["access_token"]
    except KeyError:
        st.session_state["access_token"] = ""

def send_email_rechnung(email_recipient, name, invoice_pdf, is_parent:bool):
    if is_parent:
        html_content = f"""
        <p>Hallo {name}, </p>
        <p>Wohooo! Wir freuen uns, dass du dein Kind für die Jugendfreizeit 2023 angemeldet hast.
        Anbei findest du die Rechnung. Sollte irgendwas unklar sein, schreib uns einfach eine
        E-Mail unter jugendfreizeit@rocksolidsiegen.de oder antworte auf diese E-Mail. </p>
        <p>Wir sind super gespannt und freuen uns!</p>
        <p>Gottes Segen,<br>
        Das Jugendfreizeitteam </p>
        <p>------<br>
        Diese E-Mail wurde automatisch generiert.</p>
        """
    else:
        html_content = f"""
        <p>Hey {name}, </p>
        <p>Wohooo! Wir freuen uns, dass du bei der Jugendfreizeit 2023 dabei bist.
        Anbei findest du die Rechnung. Sollte irgendwas unklar sein, schreib uns einfach eine
        E-Mail unter jugendfreizeit@rocksolidsiegen.de oder antworte auf diese E-Mail. </p>
        <p>Wir sind super gespannt und freuen uns auf dich!</p>
        <p>Gottes Segen,<br>
        Das Jugendfreizeitteam </p>
        <p>------<br>
        Diese E-Mail wurde automatisch generiert.</p>
        """

    attachments = [invoice_pdf, draft_agb_attachment()]
    subject = "Jugendfreizeit 2023 | Rechnung"

    return send_email(html_content, subject, email_recipient, attachments)

def send_zahlungserinnerung(email_recipient, name, invoice_pdf, is_parent:bool, betrag_eingang, betrag_ausstehend, betrag_gesamt):
    if is_parent:
        html_content = f"""
        <p>Hallo {name}, </p>
        <p>Wir wollten dich nur noch mal kurz dran erinnern, dass der
        Zahlungsbeitrag für die Jugendfreizeit für dein Kind ansteht.
        Von den {betrag_ausstehend} haben wir {betrag_eingang} erhalten.
        Bitte überweise also noch die restlichen {betrag_ausstehend}.
        Wir haben unten noch mal die ursprüngliche Rechnung für den Gesamtbetrag angehängt.</p>
        <p>Solltest du Fragen haben oder irgendetwas unklar sein, schreib uns einfach eine
        E-Mail unter jugendfreizeit@rocksolidsiegen.de oder antworte auf diese E-Mail.
        <p>Gottes Segen,<br>
        Das Jugendfreizeitteam </p>
        <p>------<br>
        Diese E-Mail wurde automatisch generiert.</p>
        """
    else:
        html_content = f"""
        <p>Hallo {name}, </p>
        <p>Wir wollten dich nur noch mal kurz dran erinnern, dass dein
        Zahlungsbeitrag für die Jugendfreizeit ansteht.
        Von den {betrag_ausstehend} haben wir {betrag_eingang} erhalten.
        Bitte überweise also noch die restlichen {betrag_ausstehend}.
        Wir haben unten noch mal die ursprüngliche Rechnung für den Gesamtbetrag angehängt.</p>
        <p>Solltest du Fragen haben oder irgendetwas unklar sein, schreib uns einfach eine
        E-Mail unter jugendfreizeit@rocksolidsiegen.de oder antworte auf diese E-Mail.
        <p>Gottes Segen,<br>
        Das Jugendfreizeitteam </p>
        <p>------<br>
        Diese E-Mail wurde automatisch generiert.</p>
        """

    attachments = [invoice_pdf, draft_agb_attachment()]
    subject = "Jugendfreizeit 2023 | Zahlungserinnerung"

    return send_email(html_content, subject, email_recipient, attachments)

def send_email(body:str, subject:str, email_recipient: str, attachments:list):
    try:
        st.session_state["access_token"]
    except KeyError:
        reauthorize_button()
        return False

    header = {
        "Authorization": "Bearer " + st.session_state["access_token"]
    }

    data = {
        "message": {
            # recipient list
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": f"{email_recipient}"
                    }
                }
            ],
            # email subject
            "subject": subject,
            "replyTo": [
                {
                    "emailAddress": {
                        "address": "jugendfreizeit@rocksolidsiegen.de"
                    }
                }
            ],
            "importance": "normal",
            "body": {
                "contentType": "HTML",
                "content": body
            },
            # include attachments
            "attachments": attachments
        }
    }

    response = requests.post(EMAIL_URL, headers=header, json=data, timeout=1000)
    if not response:
        st.write(response.text)
        st.write("E-Mail konnte nicht versandt werden. Versuche dich neu zu autorisieren. Oder kontaktiere einen Admin.")
        send_to_authorize()
        return False

    return True

def reauthorize_button():
    st.write("Du bist derzeit nicht autorisiert. Versuche dich erneut zu autorisieren.")
    send_to_authorize()

def main_loop():
    set_authorization_key()
