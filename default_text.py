

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
                richtig cool, dass du auf der Jugendfreizeit dabei bist!
                Dieses Jahr dürfen wir acht großartige Tage zusammen in Dänemark verbringen.
                Die Woche wird gefüllt sein mit Gottesdiensten, Gemeinschaft, Baden im Meer, Kleingruppen und noch vielem mehr!
                Damit wir alle gut vorbereitet sind, findest du hier einige wichtige Infos für die Freizeit.
                Bitte nimm dir ein paar Minuten Zeit dir die Punkte gründlich durchzulesen und die ToDo's abzuhaken!
            </p>
        </div>
        <div style=\"padding: 16px 32px; background-color: #eb5a41; color: #FFF;\">
            <h2>
                Busfahrt
            </h2>
            <p>
                Wir treffen uns am 21.07.2023 um 21:00 Uhr, auf dem <a href=\"https://goo.gl/maps/DMsRWn4DnLKVFMGj9\" style=\"text-decoration: none; color: #FFF;\">Parkplatz der Calvary Chapel Siegen</a>.
                Es ist wichtig, dass du pünktlich da bist!
                Wir können leider nicht planen, wie häufig wir an welchen Raststätten halten werden.
                Bitte pack Dir deshalb ausreichen Proviant ein.
                Das Mittagessen am Samstag ist die erste Mahlzeit in Dänemark.
            </p>
            <h2 style=\"margin-top: 32px;\">
                Gepäck
            </h2>
            <p>
                Jeder Teilnehmer darf 1 großes Gepäckstück und 1 Handgepäckstück mitbringen.
                Bitte achte darauf, dass Dein Gepäck von Dir selbst getragen werden kann.
            </p>

            <h2 style=\"margin-top: 32px;\">
                Bettzeug
            </h2>
            <p>
                Vor Ort sind die Betten mit Matratzen ausgestattet. Dementsprechend müssen ein Spannbettlaken und entweder ein Schlafsack oder eine Decke & Kissen mit den Bezügen mitgebracht werden.
            </p>

            <h2 style=\"margin-top: 32px;\">
                Sonstiges Gepäck
            </h2>
            <p>
                Handtücher, Körperhygieneartikel, Sonnencreme, Badekleidung, Sportkleidung,
                Rucksack, Verpflegung für die Busfahrt, Trinkflasche, Stifte und Bibel.
            </p>
        </div>
        <div style=\"padding: 16px 32px; text-align: center;\">
            <img src=\"https://emails.rocksolidsiegen.de/jf2023-infobrief/girls.png\" alt=\"Youth1\" style=\"width: 100%; max-width: 400px;\">
        </div>


        <div style=\"background-color: #366db4; padding: 16px 32px; color: #FFF;\">
            <h2>Dokumente</h2>
            <p style=\"font-style: italic;\">
                Es ist eine Voraussetzung für die Teilnahme an der Freizeit, dass du folgende Dokumente mitbringst
            </p>
            <ul>
                <li>Personalausweis/Reisepass</li>
                <li>Krankenkassenkarte/Auslandskrankenschein</li>
                <li>Impfheft (Das gelbe Heft, nicht die COVID-19 Nachweise.)</li>
            </ul>
            <p>
                Prüfe bitte jetzt die Gültigkeit deiner Dokumente.
                Wenn du keine deutsche Staatsbürgerschaft hast, prüfe bitte, ob du aus Deutschland ausreisen und in Dänemark einreisen darfst.
                Bitte packe die Dokumente ins Handgepäck, da wir diese vor Beginn der Busfahrt einsammeln werden. Diese bekommst du natürlich am Ende der Freizeit zurück!
                Ohne diese Dokumente kannst du leider nicht mitfahren.
            </p>

            <h2 style=\"margin-top: 32px;\">Versicherung und Regeln</h2>
            <p>
                Wir empfehlen dringend den Abschluss einer Reiserücktrittversicherung.
                Prüfe bitte, ob deine Krankenversicherung auch in Dänemark ausreichend ist, oder ob du eine Auslandskrankenversicherung benötigst.

                Auf unserer Website findest du die AGB's für die Freizeit. Dort sind einige Grundlagen und Regeln für die Freizeit aufgelistet. Bitte lese sie dir vor der Freizeit durch.
                So können wir Missverständnisse gut vermeiden!
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
                Jeden Tag wird es drei leckere und nahrhafte Mahlzeiten geben, welche im Freizeitpreis enthalten sind.
                Wenn du dir während den Busfahrten oder vor Ort im Dorf etwas kaufen möchtest, musst du es selbst bezahlen. Es gibt vor Ort keine Möglichkeit Wertsachen zu verschließen.
                Infos zur Verwendung von EC- & Kreditkarten in Dänemark findest du unter folgenden Links:
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
            <p>Wenn du Allergien hast oder z.B. Vegetarier bist und du diese noch nicht bei der Anmeldung angegebenen hast, teile es uns bitte als bald als möglich per E-Mail mit.</p>
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
                Wir freuen uns riesig! <br>
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
