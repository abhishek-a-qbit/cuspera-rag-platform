@echo off
cd /d "C:\Users\Abhishek A\Desktop\Cuspera"
call venv\Scripts\activate.bat
streamlit run app/streamlit_final.py --server.port 8501
pause
