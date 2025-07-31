import os
import re
import fitz
import pytesseract
from PIL import Image
import io
import unicodedata

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\\Program Files\\Tesseract-OCR\\tessdata'

def extrair_texto_pdf(path_pdf):
    """Extrai texto de PDF pesquisável (sem OCR)."""
    texto = ""
    try:
        with fitz.open(path_pdf) as doc:
            for page in doc:
                texto += page.get_text()
    except Exception as e:
        print(f"❌ Erro ao ler {path_pdf}: {e}")
    return texto.strip()

def extrair_texto_ocr(path_pdf):
    """Extrai texto da primeira página de PDF escaneado usando Tesseract OCR."""
    try:
        with fitz.open(path_pdf) as doc:
            page = doc[0]  # primeira página sempre
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")  # tons de cinza
            return pytesseract.image_to_string(img, lang="por").strip()
    except Exception as e:
        print(f"❌ Erro no OCR de {path_pdf}: {e}")
        return ""

def extrair_info(texto):
    # 🔍 Tenta capturar subempenho no formato padrão (000000/2024), em qualquer lugar do texto
    match_sub = re.search(r"\b(\d{6}/\d{4})\b", texto)
    if match_sub:
        subempenho = match_sub.group(1)
    elif re.search(r"\bSubempenho\s+Ordin[aá]rio\b", texto, re.IGNORECASE):
        subempenho = "Ordinario"
    else:
        subempenho = "sem_subempenho"

    # 🔍 Credor padrão
    match_credor = re.search(r"Credor\s*[:. ]\s*(\d+)\s+([A-ZÇÃÂÉÊÍÓÔÕÚÜÀ ]+)", texto, re.IGNORECASE)
    if match_credor:
        numero_credor = match_credor.group(1)
        nome_credor = match_credor.group(2).strip()
    else:
        # 🔍 Alternativa: tenta número seguido de nome em caixa alta (OCR falha leve)
        match_alt = re.search(r"\b(\d{3,})\s+([A-ZÇÃÂÉÊÍÓÔÕÚÜÀ ]{3,})\b", texto)
        if match_alt:
            numero_credor = match_alt.group(1)
            nome_credor = match_alt.group(2).strip()
        else:
            numero_credor = "sem_credor"
            nome_credor = "sem_nome"

    nome_credor = " ".join(nome_credor.split())
    nome_credor_limpo = re.sub(r'[\\/*?:"<>|]', "", nome_credor).replace(" ", "_")

    return f"{nome_credor_limpo}_{numero_credor}_{subempenho}"


def limpar_nome(nome):
    """Remove acentos e caracteres ilegais para nome de arquivos."""
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    return re.sub(r'[\\/*?:"<>|]', "", nome)

def renomear_pdfs(pasta):
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):
            caminho_antigo = os.path.join(pasta, arquivo)
            print(f"\n🔍 Lendo: {arquivo}")

            texto = extrair_texto_pdf(caminho_antigo)
            if len(texto.strip()) < 50:  # Se texto vazio ou curto, tenta OCR
                print("⚠ Texto muito curto, tentando OCR...")
                texto = extrair_texto_ocr(caminho_antigo)

            info = extrair_info(texto)
            print(f"📄 Extraído: {info}")  

            if info:
                novo_nome = limpar_nome(info) + ".pdf"
                caminho_novo = os.path.join(pasta, novo_nome)

              
                if arquivo != novo_nome:
                    if not os.path.exists(caminho_novo):
                        os.rename(caminho_antigo, caminho_novo)
                        print(f"✔ Renomeado para: {novo_nome}")
                    else:
                        print(f"⚠ Nome destino já existe: {novo_nome}. Pulando.")
                else:
                    print("✔ Já está com o nome correto.")
            else:
                print(f"⚠ Informação não encontrada em: {arquivo}")

# ✅ Altere aqui para sua pasta de testes
renomear_pdfs(r"C:\\organizarpdfs\\arquivosteste")
