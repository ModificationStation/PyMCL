@echo OFF

echo Change the 4th line in this batch file to your python install.
@rem CHANGE THIS TO WHAT YOUR PYTHON 3.6+ INSTALL IS (e.g.: C:\Program Files\python\scripts\python.exe
set pythonver=python

echo Is "%pythonver%" the correct python 3.6+ directory?
echo Close the window if incorrect.
PAUSE

echo Creating venv.
%pythonver% -m venv venv

echo Activating venv.
venv\Scripts\activate & echo Adding dependencies. & pip install pyqt5 requests appdirs & echo Using pyinstaller. & pyinstaller -y -F -w -i "favicon.ico" --add-data "background.png";"." --add-data "logo.png";"." --add-data "favicon.ico";"." --add-data "blogbackground.png";"." --add-data "blog.html";"." launcher.py & echo Complete! & PAUSE