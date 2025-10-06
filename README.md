# 1E2 x Stichting Accessibility
## Teamleden
- [Errol](https://github.com/Errol-0950548)
- [Kevin](https://github.com/Kevin-1111102)
- [Ruben](https://github.com/ruben-0926195)
- [Thomas](https://github.com/thomas-2402548)

## Projectbeschrijving

Dit project is een webapplicatie die bestaat uit drie componenten:

#### Component voor ervaringsdeskundigen
- Ervaringsdeskundigen krijgen een overzicht van zowel onderzoeken (op basis van voorkeuren en overige filters) als aanmeldingen.  
- Ervaringsdeskundigen kunnen meer informatie verkrijgen over een onderzoek door de onderzoeksdetails in te zien.  
- Ervaringsdeskundigen kunnen zich eenvoudig aan- en afmelden voor onderzoeken.  
- Ervaringsdeskundigen kunnen hun eigen gegevens inzien en aanpassen.

#### Component voor beheerders
- Beheerders krijgen een overzicht van nieuwe onderzoeken, ervaringsdeskundigen, organisaties en aanmeldingen (ervaringsdeskundigen die zich hebben aangemeld voor deelname aan een onderzoek).
- Beheerders kunnen de details van alle nieuwe onderzoeken inzien.
- Beheerders kunnen de details van alle nieuwe ervaringsdeskundigen inzien.
- Beheerders kunnen de details van alle nieuwe organisaties inzien.
- Beheerders kunnen de details van alle nieuwe aanmeldingen inzien.
- Beheerders kunnen nieuwe onderzoeken, ervaringsdeskundigen, organisaties en aanmeldingen goed- of afkeuren.

#### Component voor organisaties
- Organisaties krijgen een overzicht van al hun onderzoeken.  
- Organisaties kunnen de details van hun eigen onderzoeken inzien (en deelnemers, mits het onderzoek is goedgekeurd én het onderzoek deelnemers heeft) en deze beperkt aanpassen.
- Organisaties kunnen hun eigen onderzoeken verwijderen.

#### REST API
- Ons project functioneert ook als een REST API, waarmee verschillende CRUD-functionaliteiten beschikbaar zijn, mits de gebruiker beschikt over de juiste rechten.

## Bijzondere Functionaliteiten

**JWT Authenticatie**

Wanneer een gebruiker succesvol is ingelogd, ontvangt hij een `access_token` in de vorm van een cookie. Deze cookie wordt automatisch meegestuurd bij elk volgend HTTP-verzoek.

Het `access_token` bevat de volgende gegevens:
- **identity**: het unieke ID van de gebruiker.
- **additional_claims**: de rol van de gebruiker.

Afhankelijk van het gebruikers-ID en de rol, kunnen responses verschillen per verzoek. Daarnaast zijn bepaalde routes uitsluitend toegankelijk voor gebruikers met de juiste rol.

In de applicatie wordt gebruikgemaakt van twee belangrijke Flask hooks om authenticatie en tokenrefresh te regelen:

`app.py`
```python
app.before_request(check_jwt_authentication)
app.after_request(refresh_jwt)
```

Zie:
- `constants.py` voor de routes.
- `middlewares/jwt_auth.py` voor authenticatie en tokenrefresh
- [Swagger Documentatie](#api-documentatie)

**E-mails verzenden**

De applicatie bevat een `send_email` functie waarmee e-mails worden verzonden via MailerSend als:
- `Status van account is veranderd`
- `Status van onderzoek is veranderd`
- `Status van aanmelding op onderzoek is veranderd`

**Adminlog**

In de database wordt bijgehouden wanneer een admin iets goed- of afkeurt.

**Accessibility widget**

In een cookie worden de voorkeuren van de gebruiker met betrekking tot het thema van de website bewaard. Daarnaast krijgt de gebruiker de optie om het thema naar eigen wens in te stellen.

**Mockdata**

In `mockdata.py` staan functies voor het genereren van testdata. Nadat de functies naar wens zijn aangepast, kan een nieuwe database gegenereerd worden door `databases/database_generator.py` te runnen.

**Security**

Wachtwoorden worden gesalt en gehasht voordat deze worden opgeslagen in de database.

## Instructies

***Let op: Zorg ervoor dat je de naam van het meegeleverde env bestand verandert naar .env en dat je deze in de projectfolder plaatst (zie locatie .env.example).***

Volg de onderstaande stappen om deze applicatie correct in te stellen:

### 1. Maak een virtual environment aan:

Zorg ervoor dat je Python geïnstalleerd hebt. We raden versie 3.11 of 3.12 aan. Maak een Virtual Environment aan met dit command:

```bash
python -m venv venv
```

### 2. Activeer de virtual environment
Afhankelijk van je besturingssysteem voer je een van de onderstaande commands uit:

**Windows:**
```bash
venv\Scripts\activate
```

**MacOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Installeer de vereiste python packages

```bash
pip install -r requirements.txt
```

### 4. Start de applicatie

Na het installeren van de vereiste python packages kun je de applicatie starten met dit command:

```bash
python app.py
```

## API Documentatie

***Let op: Zorg ervoor dat applicatie is gestart.***

* [Swagger Documentatie](http://127.0.0.1:5000/apidocs/)

## Bruno

***Let op: Zorg ervoor dat applicatie is gestart.***

De folder `api_requests_org` is een Bruno-collectie die meerdere requests bevat met betrekking tot de functionaliteiten van organisaties, inclusief tests.

## Inloggegevens

**Ervaringsdeskundige**\
demo@ervaringsdeskundige.nl\
demo123

**Organisatie**\
demo@organisatie.nl\
demo123

**Admin**\
demo@admin.nl\
demo123

## Bronnen

#### Code

* [Flassger (Swagger)](https://github.com/flasgger/flasgger/tree/master)
* [Swagger Auth](https://swagger.io/docs/specification/v2_0/authentication/authentication/)
* [Swagger v2 Example](https://editor.swagger.io/?url=https://petstore.swagger.io/v2/swagger.yaml)
* [Flask-JWT](https://flask-jwt-extended.readthedocs.io/en/stable/)
* [JWT in Cookies](https://flask-jwt-extended.readthedocs.io/en/3.0.0_release/tokens_in_cookies/)
* [Faker (mock_data)](https://faker.readthedocs.io/en/master/index.html)
* [Bruno (testing api-endpoints)](https://docs.usebruno.com/testing/tests/introduction)

#### Fonts

* [Montserrat](https://fonts.google.com/specimen/Montserrat) [©️](https://fonts.google.com/specimen/Montserrat/license)
* [Mulish](https://fonts.google.com/specimen/Mulish) [©️](https://fonts.google.com/specimen/Mulish/license)

#### Afbeeldingen

* [Accessibility logo](https://www.accessibility.nl/themes/sa/images/logo.svg)
* [Accessibility icon](https://www.accessibility.nl/themes/sa/favicon/apple-touch-icon.png)
* [Woman sitting at table](https://unsplash.com/photos/woman-sitting-in-front-of-brown-wooden-table-NoRsyXmHGpI)[©️](https://unsplash.com/license)
* [Man and woman in wheelchair holding hands](https://www.pexels.com/photo/a-man-and-woman-sitting-on-the-wheelchair-8542190/)[©️](https://www.pexels.com/license/)
