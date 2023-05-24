

class Infobrief():
    subject = "Infobrief | Jugendfreizeit 2023"
    html = """<!DOCTYPE html>
<html lang=\"de\">
<head>
    <meta charset=\"UTF-8\">
    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">
    <meta name=\"format-detection\" content=\"telephone=no, date=no, address=no, email=no, url=no\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{{subject}}</title>
    <style>
        @font-face {
            font-family: \"BrandonText\";
            src: url(\"https://emails.rocksolidsiegen.de/fonts/HVDFontsBrandonTextBold.ttf\");
            font-weight: bold;
        }

        @font-face {
            font-family: \"BrandonText\";
            src: url(\"https://emails.rocksolidsiegen.de/fonts/HVDFontsBrandonTextRegular.ttf\");
            font-weight: normal;
        }
        body {
            font-weight: normal;
            font-family: \"BrandonText\", system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        }
    </style>
</head>
<body
    style=\"
        margin: 0;
        padding: 0;
        font-size:max(16px, 1rem);
    \"
>
<header
    style=\"text-align: center;\"
>
    <img src=\"https://emails.rocksolidsiegen.de/jf2023-infobrief/logo-jf2023.png\" alt=\"logo_jf_renew\" style=\"width: 100%; max-width: 300px;\">
    <h1 style=\"padding: 16px 32px;\">Informationen zur Jugendfreizeit 2023 in Dänemark</h1>
</header>
<main>
    <div style=\"padding: 16px 32px;\">
        <p>Hey {{name}},</p>
        <p>
            richtig cool, dass Du Teil der Jugendfreizeit sein wirst! Dieses Jahr dürfen wir gemeinsam acht wunderbare Tage in Dänemark verbringen. Auf Dich warten großartige Menschen, begeisterndes Programm, leckeres Essen und natürlich Baden im Meer. Unser Wunsch ist es, dass Du dabei ganz viel Freude hast, tiefe Freundschaften baust und vor allem erneuernde Begegnungen mit Jesus hast. Damit Du Dich gut auf die Freizeit vorbereiten kannst, haben wir hier einige wichtige Infos für Dich. Bitte nimm Dir ein paar Minuten Zeit, alles gründlich durchzulesen.
        </p>
    </div>
    <div style=\"padding: 16px 32px; background-color: #eb5a41; color: #FFF;\">
        <h2>
            Busfahrt
        </h2>
        <p>
            Wir treffen uns am Freitag, den 21.07.2023, um 21:00 Uhr auf dem <a href=\"https://goo.gl/maps/DMsRWn4DnLKVFMGj9\" style=\"text-decoration: none; color: #FFF;\">Parkplatz der Calvary Chapel Siegen</a>. Es ist wichtig, dass Du pünktlich da bist! Das Mittagessen am Samstag ist die erste Mahlzeit in Dänemark. Bitte pack Dir deshalb ausreichend Proviant für die Fahrt ein.
        </p>
        <p>
            <strong>Treffpunkt Zustiege:</strong> <br>
            Münster: 00:00 Uhr Raststätte Münsterland Ost (A1) <br>
            Hamburg: 04:00 Uhr Raststätte Holmoor /Quickborn (A7) <br>
        </p>
        <h2 style=\"margin-top: 32px;\">
            Gepäck
        </h2>
        <p>
            Du darfst 1 großes Gepäckstück und 1 Handgepäckstück mitbringen. Bitte achte darauf, dass Dein Gepäck von Dir selbst getragen werden kann.

        </p>

        <h2 style=\"margin-top: 32px;\">
            Bettzeug
        </h2>
        <p>
            Vor Ort sind die Betten mit Matratzen ausgestattet. Bring bitte ein Spannbettlaken, Kissen und Schlafsack oder Decke mit den Bezügen mit.
        </p>

        <h2 style=\"margin-top: 32px;\">
            Sonstiges Gepäck
        </h2>
        <p>
            Handtücher, Körperhygieneartikel, Sonnencreme, Badekleidung, Sportkleidung, Rucksack, Verpflegung für die Busfahrt, Trinkflasche, Stifte und Bibel
        </p>
    </div>
    <div style=\"padding: 16px 32px; text-align: center;\">
        <img src=\"https://emails.rocksolidsiegen.de/jf2023-infobrief/girls.png\" alt=\"Youth1\" style=\"width: 100%; max-width: 400px;\">
    </div>


    <div style=\"background-color: #366db4; padding: 16px 32px; color: #FFF;\">
        <h2>Dokumente</h2>
        <p style=\"font-style: italic;\">
            Es ist eine Voraussetzung für Deine Teilnahme an der Freizeit, dass Du folgende Dokumente mitbringst:
        </p>
        <ul>
            <li>Personalausweis/Reisepass</li>
            <li>Gesundheitskarte/Auslandskrankenschein</li>
            <li>Impfheft (Das gelbe Heft, nicht die COVID-19 Nachweise)</li>
        </ul>
        <p>
            Prüfe bitte jetzt die Gültigkeit Deiner Dokumente. Wenn Du keine deutsche Staatsbürgerschaft hast, prüfe, ob Du aus Deutschland ausreisen und in Dänemark einreisen darfst. Bitte packe die Dokumente ins Handgepäck, da wir diese vor Beginn der Busfahrt kontrollieren werden.
            Die Gesundheitskarte und den Impfausweis werden wir einsammeln.
            Diese bekommst Du natürlich am Ende der Freizeit zurück!
        </p>

        <h2 style=\"margin-top: 32px;\">Versicherung und Regeln</h2>
        <p>
            Wir empfehlen Dir den Abschluss einer Reiserücktrittversicherung.
            Prüfe bitte, ob Deine Krankenversicherung auch in Dänemark ausreichend ist, oder ob Du eine Auslandskrankenversicherung benötigst. Auf unserer Website findest Du die AGB's für die Freizeit. Dort sind einige Grundlagen und Regeln für die Freizeit aufgelistet. Bitte lese sie Dir vor der Freizeit durch. So können wir Missverständnisse gut vermeiden!
        </p>

        <div style=\"margin: 32px 0rem;\">
            <a
                href=\"https://rocksolidsiegen.de/jugendfreizeit-2023-agbs/\"
                style=\"background-color: #efd741; padding: 8px 16px; color: #000; border-radius: 10px; text-decoration: none; \"
            >
                AGBs lesen
            </a>
        </div>
    </div>
    <div style=\"padding: 16px 32px; text-align: center;\">
        <div style=\"padding: 16px 32px; text-align: center;\">
            <img src=\"https://emails.rocksolidsiegen.de/jf2023-infobrief/Welcome.png\" alt=\"Youth2\" style=\"width: 100%; max-width: 600px;\">
        </div>
    </div>

    <div style=\"padding: 16px 32px; background-color: #52b99e;\">
        <h2>Verpflegung & Taschengeld</h2>
        <p>
            Jeden Tag wird es drei leckere und nahrhafte Mahlzeiten geben, welche im Freizeitpreis enthalten sind. Wenn Du Dir während den Busfahrten oder vor Ort im Dorf etwas kaufen möchtest, musst Du es selbst bezahlen. Es gibt vor Ort keine Möglichkeit, Wertsachen zu verschließen. Infos zur Verwendung von EC- & Kreditkarten in Dänemark findest Du unter folgenden Links:
        </p>
        <div style=\"margin: 32px 0;\">
            <a
                href=\"https://www.sparkasse.de/themen/urlaub-und-reise/geld-abheben-im-ausland.html\"
                style=\"background-color: #efd741; padding: 8px 16px; color: #000; border-radius: 10px; text-decoration: none; margin-right: 16px;\"
            >
                sparkasse.de
            </a>
            <a
                href=\"https://www.vr.de/privatkunden/ihre-ziele/urlaub/geld-abheben-im-ausland.html\"
                style=\"background-color: #efd741; padding: 8px 16px; color: #000; border-radius: 10px; text-decoration: none; \"
            >
                vr.de
            </a>
        </div>
        <h2 style=\"margin-top: 64px;\">Allergien & Essensverzicht</h2>
        <p>
            Wenn Du Allergien hast oder z.B. Vegetarier bist und Du diese noch nicht bei der Anmeldung angegeben hast, teile es uns bitte zeitnah per E-Mail mit.
            Wenn Du eine akut Medizin/ Antiallergikum hast, nimm dies bitte unbedingt mit und prüfe vorher das Verfallsdatum.
        </p>
        <div style=\"margin: 32px 0rem;\">
            <a
                href=\"mailto:jugendfreizeit@rocksolidsiegen.de\"
                style=\"background-color: #efd741; padding: 8px 16px; color: #000; border-radius: 10px; text-decoration: none; display: inline-block; max-width: 100%; text-align: center;\"
            >
                Allergien und Unverträglichkeiten mitteilen
            </a>
        </div>
    </div>
    <div style=\"padding: 16px 32px;\">
        <h2>Rückfragen</h2>
        <p>Bei Fragen oder Problemen kannst Du uns gerne eine E-Mail schreiben.</p>
        <div style=\"margin: 32px 0rem;\">
            <a
                href=\"mailto:jugendfreizeit@rocksolidsiegen.de\"
                style=\"background-color: #efd741; padding: 8px 16px; color: #000; border-radius: 10px; text-decoration: none; \"
            >
                Schreib uns eine E-Mail
            </a>
        </div>
    </div>
    <div style=\"padding: 16px 32px;\">
        <p>
            Wir freuen uns auf Dich! <br>
            Dein RockSolid Team.
        </p>
    </div>
</main>
<footer style=\"text-align: center; color: gray; border-top: grey 1px solid; margin-top: 32px; padding-top: 32px;\">
    <small>
        <img src=\"https://emails.rocksolidsiegen.de/jf2023-infobrief/logo.png\" alt=\"RockSolid Logo\" width=\"100\">
        <p>Calvary Chapel Siegen e.V. | Alte Eisenstraße 6 | 57080 Siegen</p>
    </small>
</footer>


</body>
</html>"""
