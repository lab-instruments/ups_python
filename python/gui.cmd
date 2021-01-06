@echo off

:: Start Virtual Environment
cmd /k ".\venv\Scripts\activate & python gui.py & deactivate"
