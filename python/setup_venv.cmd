@echo off

:: Build Tools
:: https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16

:: Install the Virtual Environment Here
python3 -m venv ./venv

:: Start Virtual Environment
cmd /k ".\venv\Scripts\activate & pip install -r requirements.txt & deactivate"
