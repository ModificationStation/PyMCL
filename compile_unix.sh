echo Change the 4th line in this batch file to your python install.

# CHANGE THIS TO WHAT YOUR PYTHON 3.6+ INSTALL IS (e.g.: C:\Program Files\python\scripts\python.exe
export pythonver=python3

echo Is \"$pythonver\" the correct python 3.6+ directory?
echo CTRL+C if incorrect.

read -p "Press enter to continue..."

echo Creating venv.
$pythonver -m venv venv

echo Activating venv.
chmod a+x venv/bin/activate
source venv/bin/activate

echo Adding dependencies.
pip install pyqt5 requests appdirs pyinstaller pypresence

echo Using pyinstaller.
pyinstaller -y -F -i "favicon.ico" --add-data "background.png":"." --add-data "logo.png":"." --add-data "favicon.ico":"." --add-data "blogbackground.png":"." --add-data "blog.html":"." --add-data "refresh.png":"." --add-data "venv/Lib/site-packages/mitmproxy/addons/onboardingapp":"mitmproxy/addons/onboardingapp" --add-data "EasyMineLauncher.jar":"." pymcl.py
echo Complete!
read -p "Press enter to continue..."