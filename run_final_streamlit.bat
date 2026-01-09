@echo off
cd /d "C:\Users\Abhishek A\Desktop\Cuspera"
call venv\Scripts\activate.bat
set API_URL=http://localhost:8001
streamlit run app/streamlit_final.py --server.port 8501
pause
