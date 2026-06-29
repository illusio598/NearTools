# Near Tools - Discord Multi-Tool

## Installation rapide

1. Double-clique sur **NearTools-Setup.bat**
2. Le setup va :
   - Installer Python (si absent)
   - Installer les libs requises (rich, requests)
   - Configurer le tool dans %LOCALAPPDATA%\NearTools\
   - Créer un raccourci sur le bureau
   - Lancer Near Tools

## Si Windows SmartScreen bloque
- Clique sur "Informations complémentaires"
- Puis "Exécuter quand même"

## Lancement manuel
```
python neartools.py
```
(nécessite Python 3.10+ avec `pip install rich requests`)

## Stockage
Token + webhook sauvegardés dans :
%APPDATA%\NearTools\

## WARNING ! 
Les fonctions selfbot (DM All Friends, Spam Canal,
User Lookup via token) violent les ToS Discord. Tu es responsable de ton usage.

Made by Near
