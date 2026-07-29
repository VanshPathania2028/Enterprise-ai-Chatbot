from pathlib import Path

def read_file(path: str):
    file = Path(path)

    if not file.exists():
        return "File not found."

    if file.is_dir():
        return "Given path is a directory."
    
    return file.read_text(encoding="utf-8")