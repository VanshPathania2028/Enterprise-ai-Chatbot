from pathlib import Path
from pypdf import PdfReader

def load_pdf(pdf_path: str) -> str:
    """
    Read a PDF file and return all text.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

if __name__ == "__main__":
    # Use forward slashes with relative path to avoid Windows backslash Unicode issues
    pdf_path = "documents/E-PHARMACY & DIGITAL HEALTH PLATFORM  STRATEGIC OVERVIEW.pdf"
    pdf = Path(pdf_path)
    if not pdf.exists():
        print(f"ERROR: File not found at {pdf.resolve()}")
    else:
        content = load_pdf(pdf)
        print(content[:1000])
