@echo OFF

echo Change the 5th line in this batch file to your python install.
@rem CHANGE THIS TO WHAT YOUR PYTHON 3.6+ INSTALL IS (e.g.: C:\Program Files\python\scripts\python.exe
set pythonver=python

echo Is "%pythonver%" the correct python 3.6+ directory?
echo Close the window if incorrect.
PAUSE

virtualenv venv

echo Activating venv. && venv\scripts\activate && echo Adding dependencies. && pip install pyqt5 requests appdirs pypresence mitmproxy pyinstaller

echo Done!
PAUSE