import os
import sys
import re
import fitz
import pytesseract
from PIL import Image
import io
import unicodedata

def extrair_texto_pdf(path_pdf):

    texto = ""
    try:
        with fitz.open(path_pdf) as doc:
            for page in doc:
                texto += page.get_text()
    except Exception as e:
        print(f"❌ Erro ao ler {path_pdf}: {e}")
    return texto.strip()

def extrair_texto_ocr(path_pdf):
    try:
        with fitz.open(path_pdf) as doc:
            page = doc[0]  
            pix = page.get_pixmap(dpi=270)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
            texto_ocr = pytesseract.image_to_string(img, lang="por").strip()
            print(texto_ocr)
            return texto_ocr
    except Exception as e:
        print(f"❌ Erro no OCR de {path_pdf}: {e}")
        return ""
    
def extrair_info(texto, palavras_chave=None):
    if palavras_chave is None:
        palavras_chave = ["empenho", "ordinário", "restos", "extra", "subempenho"]

    texto_original = texto
    texto_lower = texto.lower()

    num_empenho = "sem_empenho"

    for palavra in palavras_chave:
        pos = texto_lower.find(palavra.lower())
        if pos != -1:
            trecho_após = texto_lower[pos:]
        
            match = re.search(r"(\d{6})\s+(\d{4})\s+(\d{4})", trecho_após)
            if match:
                num_empenho = f"{match.group(1)}_{match.group(2)}_{match.group(3)}"
                break

            match_fallback = re.search(r"\d{4,}", trecho_após)
            if match_fallback:
                num_empenho = match_fallback.group()
                break

            match_fallback = re.search(r"\d{4,}", trecho_após)
            if match_fallback:
                num_empenho = match_fallback.group()
                break

    match_credor = re.search(r"Credor\s*[:. ]\s*(\d+)\s+([A-ZÇÃÂÉÊÍÓÔÕÚÜÀ ]+)", texto, re.IGNORECASE)
    if match_credor:
        numero_credor = match_credor.group(1)
        nome_credor = match_credor.group(2).strip()
    else:
        match_alt = re.search(r"\b(\d{3,})\s+([A-ZÇÃÂÉÊÍÓÔÕÚÜÀ ]{3,})\b", texto)
        if match_alt:
            numero_credor = match_alt.group(1)
            nome_credor = match_alt.group(2).strip()
        else:
            numero_credor = "sem_credor"
            nome_credor = "sem_nome"

    nome_credor = " ".join(nome_credor.split())
    nome_credor_limpo = re.sub(r'[\\/*?:"<>|]', "", nome_credor).replace(" ", "_")

    return {
        "empenho": num_empenho,
        "credor_numero": numero_credor,
        "credor_nome": nome_credor_limpo
    }

def limpar_nome(nome):
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    return re.sub(r'[\\/*?:"<>|]', "", nome)

def renomear_pdfs(entrada):
    if isinstance(entrada, list):
        arquivos = entrada
    elif isinstance(entrada, str):
        arquivos = [
            os.path.join(entrada, f)
            for f in os.listdir(entrada)
            if f.lower().endswith(".pdf")
        ]
    else:
        raise ValueError("Entrada inválida: deve ser um diretório (str) ou lista de arquivos.")

    for caminho_antigo in arquivos:
        if not caminho_antigo.lower().endswith(".pdf"):
            continue

        nome_arquivo = os.path.basename(caminho_antigo)
        pasta = os.path.dirname(caminho_antigo)

        print(f"\n🔍 Lendo: {nome_arquivo}")
        texto = extrair_texto_pdf(caminho_antigo)

        if len(texto.strip()) < 50:
            print("Iniciando OCR...")
            texto = extrair_texto_ocr(caminho_antigo)

        info_dict = extrair_info(texto)
        print(f"📄 Extraído: {info_dict}")

        if info_dict["empenho"] != "sem_empenho" or info_dict["credor_nome"] != "sem_nome":
            empenho_curto = info_dict["empenho"]
            nome_base = f"{empenho_curto}_{info_dict['credor_numero']}_{info_dict['credor_nome']}"
            novo_nome = f"{nome_base}.pdf"
            caminho_novo = os.path.join(pasta, novo_nome)

            try:
                if nome_arquivo == novo_nome:
                    print("✔ Já está com o nome correto.")
                    continue
                
                if os.path.exists(caminho_novo):
                    print(f"⚠ Nome destino já existe: {novo_nome}. Pulando.")
                    continue

                os.rename(caminho_antigo, caminho_novo)
                print(f"✅ Renomeado para: {novo_nome}")

            except Exception as e:
                print(f"❌ Erro ao renomear '{nome_arquivo}': {e}")
        else:
            print(f"⚠ Informação não encontrada em: {nome_arquivo}")

            
