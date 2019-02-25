echo Activating venv.
export $worked=false

source venv/bin/activate && export $worked=true

if [$worked=true]
then
	echo Starting launcher.
	python launcher.py
else
	echo Failed to activate virtualenv.

read -p "Press enter to continue..."