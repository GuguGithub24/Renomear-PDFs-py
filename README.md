# Projeto RenomearPDF

Este programa renomeia PDFs baseando-se no conteúdo, utilizando OCR com Tesseract.

## Requisitos

- Python 3.8 ou superior
- Tesseract OCR instalado no sistema

## Instalando o Tesseract OCR

Baixe o instalador oficial do Tesseract para Windows aqui:

https://github.com/tesseract-ocr/tesseract/releases

Execute o instalador e instale o Tesseract na pasta padrão.

## Configuração

Se o programa não localizar o Tesseract automaticamente, configure o caminho manualmente no arquivo `config.py`:

```python
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
