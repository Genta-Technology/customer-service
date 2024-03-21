"""
Python file that run the Chatbot API and Dashboard
"""
import multiprocessing
import os

def run_api():
    """
    Runs the FastAPI server.
    """
    os.system("uvicorn src.api.api:app --reload")

def run_dashboard():
    """
    Runs the Streamlit dashboard.
    """
    os.system("streamlit run src/monitoring_system/app.py")

if __name__ == "__main__":
    # Create separate processes for the API and dashboard
    api_process = multiprocessing.Process(target=run_api)
    dashboard_process = multiprocessing.Process(target=run_dashboard)

    # Start both processes
    api_process.start()
    dashboard_process.start()

    # Wait for both processes to finish (optional)
    api_process.join()
    dashboard_process.join()