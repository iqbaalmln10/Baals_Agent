import os
from langchain_core.tools import tool

@tool
def list_files(directory: str = "."):
    """Gunakan ini untuk melihat daftar file dan folder di direktori tertentu."""
    try:
        files = os.listdir(directory)
        ignored = [".git", "__pycache__", "venv", ".env", "node_modules"]
        filtered_files = [f for f in files if f not in ignored]
        return f"Isi folder '{directory}': {', '.join(filtered_files)}"
    except Exception as e:
        return f"Error membaca folder: {str(e)}"

@tool
def read_file_content(file_path: str):
    """Gunakan ini untuk membaca isi dari sebuah file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return f"Isi file {file_path}:\n\n{content}"
    except Exception as e:
        return f"Error membaca file: {str(e)}"