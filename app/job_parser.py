import os

def extract_job_description(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = file_path.lower().split(".")[-1]
    if ext == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Only TXT format supported for job descriptions (for now)")
