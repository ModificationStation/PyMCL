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
pip install pyqt5 requests appdirs pyinstaller pypresence mitmproxy

echo Done!
read -p "Press enter to continue..."