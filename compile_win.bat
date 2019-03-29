@echo OFF

echo Change the 4th line in this batch file to your python install.
@rem CHANGE THIS TO WHAT YOUR PYTHON 3.6+ INSTALL IS (e.g.: C:\Program Files\python\scripts\python.exe
set pythonver=python

echo Is "%pythonver%" the correct python 3.6+ directory?
echo Close the window if incorrect.
PAUSE

echo Activating venv. && venv\scripts\activate && echo Adding dependencies. && pip install pyqt5 requests appdirs pypresence mitmproxy && echo Using pyinstaller. && pyinstaller -y -F -i "favicon.ico" --add-data "background.png";"." --add-data "logo.png";"." --add-data "favicon.ico";"." --add-data "blogbackground.png";"." --add-data "blog.html";"." --add-data "refresh.png";"." --add-data "venv\Lib\site-packages\mitmproxy\addons\onboardingapp";"mitmproxy\addons\onboardingapp" pymcl.py
echo Complete!
PAUSE