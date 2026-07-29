from loader import load_pdf
from chunking import chunk_text
text = load_pdf("documents/E-PHARMACY & DIGITAL HEALTH PLATFORM  STRATEGIC OVERVIEW.pdf")
chunks = chunk_text(text)
print(len(chunks))
print(chunks[0])