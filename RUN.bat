@echo off
cd /d C:\INJCT

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

:: Run the Streamlit app
streamlit run app.py
