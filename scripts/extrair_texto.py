import fitz  # pymupdf
import re

def extrair_texto_pdf(caminho_pdf):
    try:
        doc = fitz.open(caminho_pdf)
        texto = ""
        for page in doc:
            texto += page.get_text()
        return texto.lower()
    except Exception:
        return ""

def extrair_metodos(texto):
    padrao = r"(materials and methods|methods)(.*?)(results|discussion|conclusion)"
    match = re.search(padrao, texto, re.DOTALL)
    if match:
        return match.group(2)
    return texto  # fallback
