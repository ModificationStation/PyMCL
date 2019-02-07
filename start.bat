@echo OFF

echo Change the 4th line in this batch file to your python install.
@rem CHANGE THIS TO WHAT YOUR PYTHON 3.6+ INSTALL IS (e.g.: C:\Program Files\python\scripts\python.exe
set pythonver=python

echo Is "%pythonver%" the correct python 3.6+ directory?
echo Close the window if incorrect.
PAUSE

echo Activating venv.
venv\Scripts\activate & python launcher.py & PAUSE