import os
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Caminho para o executável do tesseract (só se necessário no Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_texto_pdf(path_pdf):
    texto = ""
    try:
        with fitz.open(path_pdf) as doc:
            for page in doc:
                texto += page.get_text()
    except Exception as e:
        print(f"Erro ao ler {path_pdf}: {e}")
    return texto.strip()

def extrair_texto_ocr(path_pdf):
    texto = ""
    try:
        with fitz.open(path_pdf) as doc:
            for page in doc:
                imagem = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(imagem.tobytes("png")))
                texto += pytesseract.image_to_string(img, lang='por')
    except Exception as e:
        print(f"Erro no OCR de {path_pdf}: {e}")
    return texto.strip()

def extrair_info(texto):
    # Exemplo: extrair CPF no formato 000.000.000-00
    match = re.search(r'\d{3}\.\d{3}\.\d{3}-\d{2}', texto)
    if match:
        return match.group(0)
    return None

def limpar_nome(nome):
    # Remove caracteres ilegais para nomes de arquivos
    return re.sub(r'[\\/*?:"<>|]', "", nome)

def renomear_pdfs(pasta):
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):
            caminho_antigo = os.path.join(pasta, arquivo)
            print(f"Lendo: {arquivo}")

            texto = extrair_texto_pdf(caminho_antigo)
            if len(texto.strip()) < 50:  # Se texto vazio ou curto, tenta OCR
                texto = extrair_texto_ocr(caminho_antigo)

            info = extrair_info(texto)
            if info:
                novo_nome = limpar_nome(info) + ".pdf"
                caminho_novo = os.path.join(pasta, novo_nome)

                if not os.path.exists(caminho_novo):  # Evita sobrescrever
                    os.rename(caminho_antigo, caminho_novo)
                    print(f"✔ Renomeado para: {novo_nome}")
                else:
                    print(f"⚠ Arquivo já existe: {novo_nome}")
            else:
                print(f"⚠ Informação não encontrada em: {arquivo}")

# Use aqui a sua pasta com os PDFs
renomear_pdfs("C:/caminho/da/pasta")
