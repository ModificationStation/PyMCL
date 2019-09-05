@echo OFF

echo Activating venv. && venv\scripts\activate && echo Using pyinstaller. && pyinstaller -y -F -i "favicon.ico" --add-data "background.png";"." --add-data "logo.png";"." --add-data "favicon.ico";"." --add-data "blogbackground.png";"." --add-data "blog.html";"." --add-data "refresh.png";"." --add-data "venv\Lib\site-packages\mitmproxy\addons\onboardingapp";"mitmproxy\addons\onboardingapp" --add-data "EasyMineLauncher.jar";"." pymcl.py
echo Done!
PAUSE