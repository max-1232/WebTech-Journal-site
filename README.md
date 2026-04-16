# MyJournal - Digitaal Dagboek

Een persoonlijke web-applicatie gebouwd met Flask waarmee gebruikers hun eigen verhalen en herinneringen kunnen vastleggen, bewerken en beheren.

## Functies
* **Gebruikersbeheer:** Registreren, inloggen en veilig uitloggen met behulp van flask-login.
* **Journal Entries:** Aanmaken, bewerken en verwijderen van entries.
* **Responsive Design:** Uiterlijk is met behulp van Bootstrap 
* **Berichten:** Automatische flash meldingen die komen als iets is gelukt of bij foutmeldingen

## Technische informatie
* **Backend:** Python / Flask
* **Database:** SQLite met SQLAlchemy
* **Frontend:** Jinja2 templates, Bootstrap 
* **Pakketbeheer:** `uv`

## Installatie & Gebruik

Volg deze stappen om het project lokaal te draaien:

1. **Kloon de repository:**
   ```bash
   git clone https://github.com/max-1232/WebTech-Journal-site/tree/main
   cd WebTech-Journal-site

2. **Installeer uv**
    ```bash
    Voor Linux: "curl -LsSf https://astral.sh/uv/install.sh | sh"
    Voor Windows (in Powershell): "powershell -c "irm https://astral.sh/uv/install.ps1 | iex""
    Voor Mac (met brew):  "brew install uv"

3. **Packets downloaden**
    ```bash
    uv sync
  Vervolgens eventueel terminal opnieuw opstarten

4. **Project runnen**
    ```bash
    uv run python app.py
  De website zal beschikbaar zijn op: http://127.0.0.1:5000


De database wordt automatisch aangemaakt met een test gebruiker
- Username: Max
- Email: max@hanze.nl
- Wachtwoord: max

Om een nieuwe gebruiker aan te maken, kan dat via Registreren. Hierna kan vervolgens ingelogd worden met de nieuwe account.
