echo Activating venv.
chmod a+x venv/bin/activate
source venv/bin/activate

echo Using pyinstaller.
pyinstaller -y -F -i "favicon.ico" --add-data "background.png":"." --add-data "logo.png":"." --add-data "favicon.ico":"." --add-data "blogbackground.png":"." --add-data "blog.html":"." --add-data "refresh.png":"." --add-data "venv/lib/python3.7/site-packages/mitmproxy/addons/onboardingapp":"mitmproxy/addons/onboardingapp" --add-data "EasyMineLauncher.jar":"." pymcl.py
echo Done!
read -p "Press enter to continue..."