import datetime
from babel.numbers import format_currency
from fpdf import FPDF

class Invoice_PDF(FPDF):
    font_size_small = 8
    font_size_p = 12
    font_size_h1 = 24
    font_size_h2 = 20
    font_size_h3 = 16

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_margins(15,15,15)
        self.alias_nb_pages()
        self.add_page()


    def calc_height_in_mm(self, line_height_factor:float=1.3) -> float:
        return self.font_size_pt*0.3527*line_height_factor

    def header(self):
        text_absender = "Calvary Chapel Siegen e.V.\nRockSolid | Jugendgruppe\nAlte Eisenstraße 6\n57080 Siegen\nTel: +49 (0)271 313 8888 8\n "
        # self.set_lang("DE")
        # self.set_author("RockSolid Siegen")

        # Logo
        self.image('logo.png', 15, 15, 33)
        self.add_font("Brandon", "B", r"fonts/HVDFontsBrandonTextBold.ttf", True)
        self.add_font("Brandon", "N", r"fonts/HVDFontsBrandonTextRegular.ttf", True)

        self.set_font("Brandon", "N", self.font_size_p)
        height = self.calc_height_in_mm()
        self.multi_cell(0, height, text_absender, 0, "R")

        # Kontakt
        self.set_font("Brandon", "B", 16)
        height = self.calc_height_in_mm()
        self.cell(0, height, "Kontakt", 0, 2, "R")

        # Name: Josua Hippenstiel & E-Mail
        self.set_font("Brandon", "N", self.font_size_p)
        height = self.calc_height_in_mm()
        self.cell(0, height, "Josua Hippenstiel", 0, 2, "R")
        self.cell(0, height, "jugendfreizeit@rocksolidsiegen.de", 0, 2, "R")
        self.cell(0, height, " ", 0, 2, "R")

        # Datum Überschrift
        self.set_font("Brandon", "B", 16)
        height = self.calc_height_in_mm()
        self.cell(0, height, "Datum", 0, 2, "R")

        # Datum 01.01.2023
        self.set_font("Brandon", "N", self.font_size_p)
        height = self.calc_height_in_mm()
        self.cell(0, height, f"{datetime.datetime.now().strftime('%d.%m.%Y')}", 0, 2, "R")
        self.cell(0, height, " ", 0, 2, "R")

        # Post Absender
        self.set_font("Brandon", "N", self.font_size_small)
        self.text(25,50,"Calvary Chapel Siegen e.V. | Alte Eisenstraße 6 | 57080 Siegen")
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Brandon', 'N', self.font_size_p)
        height = self.calc_height_in_mm()
        # Page number
        self.cell(0, height, 'Seite ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def write_personal_data(self, current_id:int, name_rechnung:str, name_teilnehmer:str, address_street:str, plz:int, city:str, country:str, freizeit_kosten:float, busfahrt_kosten:float, discount:float, discount_code:str):
        self.set_font("Brandon", "N", self.font_size_p)
        height = self.calc_height_in_mm(1.5)
        self.text(25, 50+height, f"{name_rechnung}")
        self.text(25, 50+2*height, f"{address_street}")
        self.text(25, 50+3*height, f"{plz} {city}")
        self.text(25, 50+4*height, f"{country}")

        # Rechnungsüberschrift
        self.set_font("Brandon", "B", self.font_size_h1)
        height = self.calc_height_in_mm()
        self.cell(0, height, f"Rechnung #JF2023-{current_id:03}", 0, 2)
        self.ln(20)

        # Print table
        self.set_font("Brandon", "B", self.font_size_p)
        height = self.calc_height_in_mm(2)
        width_pos_col = 15
        width_description_col = 115
        width_cost_col = 50

        pos = 1
        # Überschriften Tabelle
        self.cell(width_pos_col, height, "Pos", "B", 0, "C")
        self.cell(width_description_col, height, "Bezeichnung", "B", 0, "L")
        self.cell(width_cost_col, height, "Betrag", "B", 1, "L")

        # Freizeitbetrag
        self.set_font("Brandon", "N", self.font_size_p)
        self.cell(width_pos_col, height, f"{pos}", 0, 0, "C")
        self.cell(width_description_col, height, f"Freizeitteilnahme von {name_teilnehmer}", 0, 0, "L")
        self.cell(width_cost_col, height, f"{format_currency(freizeit_kosten, 'EUR', locale='de_DE')}", 0, 1, "L")

        # Buskosten
        if busfahrt_kosten != 0:
            pos = pos + 1
            self.cell(width_pos_col, height, f"{pos}", 0, 0, "C")
            self.cell(width_description_col, height, f"Busfahrt für {name_teilnehmer}", 0, 0, "L")
            self.cell(width_cost_col, height, f"{format_currency(busfahrt_kosten, 'EUR', locale='de_DE')}", 0, 1, "L")

        if discount != 0:
            pos = pos + 1
            self.cell(width_pos_col, height, f"{pos}", 0, 0, "C")
            self.cell(width_description_col, height, f"Rabatt ({discount_code})", 0, 0, "L")
            self.cell(width_cost_col, height, f"{format_currency(discount, 'EUR', locale='de_DE')}", 0, 1, "L")

        # Gesamtbetrag
        gesamtbetrag = freizeit_kosten + busfahrt_kosten - discount
        self.set_font("Brandon", "B", self.font_size_p)
        self.cell(width_pos_col, height, "", "T", 0, "C")
        self.cell(width_description_col, height, "Gesamtbetrag", "T", 0, "R")
        self.cell(width_cost_col, height, f"{format_currency(gesamtbetrag, 'EUR', locale='de_DE')}", "T", 1, "L")

        self.ln(height)

        # Abschließender Text
        self.set_font("Brandon", "N", self.font_size_p)
        height = self.calc_height_in_mm()
        self.write(height, "Den Betrag bitte bis zum 15.05.2023 auf das untenstehende Konto überweisen. Der Rechnungsbetrag enthält keine Umsatzsteuer.")
        self.ln(height*2)
        self.cell(0, height, "Bankverbindungen:", 0, 1, "L")
        self.cell(0, height, "Name: Calvary Chapel Siegen e.V. (RockSolid)", 0, 1, "L")
        self.cell(0, height, "IBAN: DE49 4476 1534 0829 9190 05", 0, 1, "L")
        self.cell(0, height, "BIC: GENODEM1NRD", 0, 1, "L")
        self.cell(0, height, f"Verwendungszweck: JF2023-{current_id:03}", 0, 1, "L")
        self.ln(height)
        self.cell(0, height, "Liebe Grüße,", 0, 1, "L")
        self.cell(0, height, "Euer Freizeitteam", 0, 1, "L")


def create_pdf(current_id:int, invoice_name:str, name_teilnehmer:str, address_street:str, address_zip:int, address_city:str, address_country:str, freizeit_kosten:float, busfahrt_kosten:float, discount:float, discount_code:str) -> FPDF:
    # Instantiation of inherited class
    pdf = Invoice_PDF('P', 'mm', 'A4')
    pdf.write_personal_data(current_id, invoice_name, name_teilnehmer, address_street, address_zip, address_city, address_country, freizeit_kosten, busfahrt_kosten, discount, discount_code)
    return pdf
