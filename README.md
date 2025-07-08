# BewegendeAnimatieTest

Een minimaal script voor het genereren van bewegende animaties binnen een ovaal, bedoeld voor fMRI/ECG-achtige visualisaties.

## Bestanden

- `main.py` - Hoofdscript dat de GIF animatie genereert
- `constants.py` - Configuratie voor ovaal afmetingen en animatie instellingen
- `background/` - Directory voor achtergrond afbeeldingen

## Gebruik

1. Plaats het bestand `brain_background.png` in de `background/` directory
2. Installeer de benodigde dependency: `pip install Pillow`
3. Voer het script uit: `python main.py`

Het script genereert een `brain_animation.gif` bestand met de bewegende animatie binnen het gedefinieerde ovaal.

## Configuratie

Pas de instellingen aan in `constants.py`:
- Ovaal positie en afmetingen
- Aantal animatie frames
- Frame duur
- Output bestandsnaam