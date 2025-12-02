Con esto creas el ejecutable:
1. Creas tu entonrno virutal "python -m venv venv"
2. Instalas las dependencias con "pip install -r requirements.txt"
3. pyinstaller --onefile --windowed --icon=nombre.ico --name "EnglishLearningGame" --add-data "vocabulary.py;." --add-data "game_ui.py;." --add-data "data_manager.py;." main.py
