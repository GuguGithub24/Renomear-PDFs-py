import tkinter as tk
from tkinter import filedialog, messagebox
from SetNamePdf import renomear_pdfs
import os
import config

# Variável global para armazenar a seleção
selecionado = None

def exibir_selecao(texto):
    caminho_label.config(text=texto)

def escolher_pasta():
    global selecionado
    pasta = filedialog.askdirectory()
    if pasta:
        selecionado = pasta
        exibir_selecao(f"Pasta selecionada:\n{pasta}")
    else:
        selecionado = None
        exibir_selecao("Nenhuma pasta selecionada.")

def escolher_arquivos():
    global selecionado
    arquivos = filedialog.askopenfilenames(
        title="Selecione um ou mais PDFs",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if arquivos:
        selecionado = list(arquivos)
        nomes = "\n".join(os.path.basename(f) for f in arquivos)
        exibir_selecao(f"{len(arquivos)} arquivo(s) selecionado(s):\n{nomes}")
    else:
        selecionado = None
        exibir_selecao("Nenhum arquivo selecionado.")

def executar_renomeacao():
    if not selecionado:
        messagebox.showwarning("Nenhuma seleção", "Selecione uma pasta ou arquivos antes de executar.")
        return

    try:
        renomear_pdfs(selecionado)
        messagebox.showinfo("Finalizado", "Renomeação concluída com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Criando janela
root = tk.Tk()
root.title("Renomear PDFs por Conteúdo")
root.geometry("480x360")
root.resizable(False, False)

label = tk.Label(root, text="Escolha como deseja selecionar os PDFs:", font=("Verdana, bold", 14) )
label.pack(pady=10)

# Botões de seleção
frame_botoes = tk.Frame(root)
frame_botoes.pack()

botao_pasta = tk.Button(frame_botoes, text="Selecionar Pasta", command=escolher_pasta, font=("Verdana", 11), width=20)
botao_pasta.grid(row=0, column=0, padx=10, pady=5)

botao_arquivos = tk.Button(frame_botoes, text="Selecionar Arquivos", command=escolher_arquivos, font=("Verdana", 11), width=20)
botao_arquivos.grid(row=0, column=1, padx=10, pady=5)

# Área para exibir seleção
caminho_label = tk.Label(root, text="Nenhuma seleção ainda.", font=("Verdana", 10), wraplength=440, justify="left")
caminho_label.pack(pady=15)

# Botão para executar
botao_executar = tk.Button(root, relief="groove",  text="Renomear", command=executar_renomeacao, font=("Verdana", 14, "bold"), width=25, bg="#1E90FF", fg="white", activebackground="#104E8B",activeforeground="white", bd=5, padx=15, pady=10)
botao_executar.pack(pady=15)

root.mainloop()
