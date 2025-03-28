import sys
import subprocess
import os


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py [data|website]")
        sys.exit(1)

    mode = sys.argv[1]
    
    if mode == "data":
       subprocess.run(["python", f"{os.getcwd()}/create_data.py"])
    elif mode == "website":
        subprocess.run(["streamlit", "run", "./streamlit_app.py"])
    else:
        print("Invalid argument. Use 'data' to import data or 'website' to run the Streamlit app.")