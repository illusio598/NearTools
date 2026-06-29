@echo off
chcp 65001 >nul
title Near Tools - Setup
cls

echo.
echo  ================================
echo      NEAR TOOLS  -  Setup
echo  ================================
echo.

:: --- vérification des pythons installé ---
echo  Verification des mise à jour de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo  Python introuvable - installation en cours...
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    if errorlevel 1 (
        echo.
        echo  [ERREUR] Python n'a pas pu etre installe automatiquement.
        echo  Telecharge-le manuellement : https://www.python.org/downloads/
        echo  Coche bien "Add Python to PATH" puis relance ce setup.
        pause
        exit /b 1
    )
)
python --version
echo  [OK]
echo.


echo  Installation des librairies (rich, requests)...
python -m pip install --upgrade pip --quiet >nul 2>&1
python -m pip install rich requests
if errorlevel 1 (
    echo.
    echo  [ERREUR] pip install a echoue.
    echo  Essaie de relancer ce script en tant qu'administrateur.
    pause
    exit /b 1
)
echo  [OK]
echo.

:: --- Lancement ---
echo  Lancement de Near Tools...
echo.
python "%~dp0neartools.py"
pause
