import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from pypdf import PdfReader
import threading
from queue import Queue, Empty

eventos = Queue()

def processar_contagem():
    pasta_selecionada = entry_caminho.get()
    
    if not pasta_selecionada:
        messagebox.showwarning("Aviso", "Por favor, selecione uma pasta primeiro.")
        return

    diretorio = Path(pasta_selecionada)
    if not diretorio.exists() or not diretorio.is_dir():
        messagebox.showerror("Erro", "O caminho especificado não é válido.")
        return

    btn_iniciar.config(state="disabled")
    btn_pasta.config(state="disabled")
    btn_exportar.config(state="disabled")
    text_log.delete(1.0, tk.END)
    lbl_status.config(text="Contando páginas...")

    def executar_processamento():
        total_paginas = 0
        total_pdfs = 0
        erros = []

        for arquivo in diretorio.rglob("*"):
            if not arquivo.is_file() or arquivo.is_symlink() or arquivo.suffix.lower() != ".pdf":
                continue
            try:
                leitor = PdfReader(arquivo)
                num_paginas = len(leitor.pages)
                total_paginas += num_paginas
                total_pdfs += 1
                
                linha = f"[{num_paginas:03d} págs] {arquivo.name}\n"
                text_log.insert(tk.END, linha)
                text_log.see(tk.END)
            except Exception as e:
                erros.append((arquivo.name, str(e)))
                eventos.put(("log", f"[ERRO] {arquivo.name}\n"))

        resumo = f"\n========================================\n"
        resumo += f"TOTAL DE ARQUIVOS PROCESSADOS: {total_pdfs}\n"
        resumo += f"TOTAL GERAL DE PÁGINAS: {total_paginas}\n"
        resumo += f"========================================\n"
        
        if erros:
            resumo += f"\nArquivos com erro ({len(erros)}):\n"
            for nome, _ in erros:
                resumo += f"- {nome}\n"

        eventos.put(("fim", resumo))

    threading.Thread(target=executar_processamento, daemon=True).start()

def consumir_eventos():
    # Somente a thread principal toca nos widgets Tkinter.
    try:
        while True:
            tipo, texto = eventos.get_nowait()
            text_log.insert(tk.END, texto)
            text_log.see(tk.END)
            if tipo == "fim":
                lbl_status.config(text="Processamento concluído!")
                for botao in (btn_iniciar, btn_pasta, btn_exportar):
                    botao.config(state="normal")
    except Empty:
        pass
    app.after(100, consumir_eventos)

def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione a Pasta com os PDFs")
    if pasta:
        entry_caminho.delete(0, tk.END)
        entry_caminho.insert(0, pasta)

def salvar_relatorio():
    conteudo = text_log.get(1.0, tk.END).strip()
    if not conteudo:
        messagebox.showwarning("Aviso", "Não há resultados para exportar.")
        return

    arquivo_destino = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivo de Texto", "*.txt"), ("Todos os Arquivos", "*.*")],
        title="Salvar Relatório Como..."
    )
    if arquivo_destino:
        with open(arquivo_destino, "w", encoding="utf-8") as f:
            f.write(conteudo)
        messagebox.showinfo("Sucesso", "Relatório salvo com sucesso!")

app = tk.Tk()
app.title("Contador de Páginas PDF - Digitalização")
app.geometry("600x500")

frame_topo = ttk.Frame(app, padding=10)
frame_topo.pack(fill="x")

lbl_instrucao = ttk.Label(frame_topo, text="Pasta Principal com Subpastas:")
lbl_instrucao.pack(anchor="w")

entry_caminho = ttk.Entry(frame_topo)
entry_caminho.pack(side="left", fill="x", expand=True, padx=(0, 5), pady=5)

btn_pasta = ttk.Button(frame_topo, text="Procurar...", command=selecionar_pasta)
btn_pasta.pack(side="right")

btn_iniciar = ttk.Button(app, text="Iniciar Contagem", command=processar_contagem)
btn_iniciar.pack(pady=5)

lbl_status = ttk.Label(app, text="Aguardando início...", font=("Arial", 10, "italic"))
lbl_status.pack(pady=2)

frame_log = ttk.Frame(app, padding=10)
frame_log.pack(fill="both", expand=True)

text_log = tk.Text(frame_log, wrap="word", font=("Consolas", 9))
text_log.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_log, command=text_log.yview)
scrollbar.pack(side="right", fill="y")
text_log.config(yscrollcommand=scrollbar.set)

btn_exportar = ttk.Button(app, text="Salvar Relatório (.txt)", command=salvar_relatorio)
btn_exportar.pack(pady=10)

app.after(100, consumir_eventos)
app.mainloop()
