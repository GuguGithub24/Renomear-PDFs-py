import tkinter as tk
from tkinter import filedialog, messagebox
from SetNamePdf import renomear_pdfs
import config

def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        try:
            renomear_pdfs(pasta)
            messagebox.showinfo("Finalizado", "Renomeação concluída com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    else:
        messagebox.showwarning("Cancelado", "Nenhuma pasta foi selecionada.")

# Criando janela
root = tk.Tk()
root.title("Renomear PDFs por Conteúdo")
root.geometry("400x200")
root.resizable(False, False)

label = tk.Label(root, text="Clique abaixo para escolher a pasta com os PDFs:", font=("Arial", 12))
label.pack(pady=20)

botao = tk.Button(root, text="Selecionar Pasta", command=escolher_pasta, font=("Arial", 12), width=20)
botao.pack(pady=10)

root.mainloop()
