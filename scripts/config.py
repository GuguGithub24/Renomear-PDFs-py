import os
import sys
import pytesseract

if getattr(sys, 'frozen', False):
    pasta_base = sys._MEIPASS
else:
    pasta_base = os.path.dirname(os.path.abspath(__file__))

# Caminho do tesseract-portable
caminho_portable = os.path.join(pasta_base, "tesseract-portable", "tesseract.exe")

# Caminho padrão da instalação do Tesseract
caminho_padrao = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(caminho_portable):
    caminho_tesseract = caminho_portable
    tessdata_dir = os.path.join(pasta_base, "tesseract-portable", "tessdata")
else:
    caminho_tesseract = caminho_padrao
    tessdata_dir = r"C:\Program Files\Tesseract-OCR\tessdata"  # ou derive de caminho_tesseract

pytesseract.pytesseract.tesseract_cmd = caminho_tesseract
os.environ["TESSDATA_PREFIX"] = tessdata_dir
