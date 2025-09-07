#Transforma guia docente en PDF a .txt utilizando libreria pymupdf

import fitz  # pymupdf

def pdf_to_text(pdf_path, txt_path):
    doc = fitz.open(pdf_path)
    with open(txt_path, "w", encoding="utf-8") as outfile:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            outfile.write(f"--- Página {page_num} ---\n")
            outfile.write(text)
            outfile.write("\n\n")
    print(f"Texto extraído correctamente a {txt_path}")

# Cambia los nombres de archivo según corresponda
pdf_to_text("guia_docente.pdf", "guia_docente.txt")
