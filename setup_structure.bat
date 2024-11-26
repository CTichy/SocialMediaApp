@echo off
:: Create the base project folder structure
mkdir src
mkdir src\routes
mkdir src\utils
mkdir images

:: Create placeholder files
echo > src\__init__.py
echo > src\api.py
echo > src\db.py
echo > src\auth.py
echo > src\routes\__init__.py
echo > src\routes\users.py
echo > src\routes\posts.py
echo > src\utils\__init__.py
echo > src\utils\image.py
echo > src\utils\logger.py

:: Create other top-level project files
echo > .env
echo > requirements.txt
echo > pytest.ini
echo > Dockerfile
echo > docker-compose.yml
echo > README.md

:: Notify the user
echo Folder structure created successfully!
pause
