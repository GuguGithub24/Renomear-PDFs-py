import os
import sys
import pytesseract

if getattr(sys, 'frozen', False):
    pasta_base = sys._MEIPASS
else:
    pasta_base = os.path.dirname(os.path.abspath(__file__))

caminho_tesseract = os.path.join(pasta_base, "tesseract-portable", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = caminho_tesseract
os.environ["TESSDATA_PREFIX"] = os.path.join(pasta_base, "tesseract-portable")
