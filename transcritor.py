import customtkinter as ctk
from tkinter import filedialog, messagebox
import whisper
import os
import threading
import warnings

# Removido o path fixo para ffmpeg
# os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU*")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Transcritor com Whisper by Leo Todeschini")
app.geometry("650x300")
app.resizable(False, False)

entrada_var = ctk.StringVar()
saida_var = ctk.StringVar()
status_var = ctk.StringVar(value="Pronto")

def escolher_arquivo():
    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo de áudio",
        filetypes=[("Áudio", "*.mp3 *.wav *.m4a *.ogg *.flac *.webm *.opus")]
    )
    if caminho:
        entrada_var.set(caminho)

def escolher_destino():
    caminho = filedialog.asksaveasfilename(
        title="Salvar transcrição como",
        defaultextension=".txt",
        filetypes=[("Texto", "*.txt")]
    )
    if caminho:
        saida_var.set(caminho)

def iniciar_transcricao():
    entrada = entrada_var.get()
    saida = saida_var.get()

    if not os.path.exists(entrada):
        messagebox.showerror("Erro", "Arquivo de entrada inválido.")
        return
    if not saida:
        messagebox.showerror("Erro", "Caminho de saída inválido.")
        return

    status_var.set("Transcrevendo, por favor aguarde...")
    progress_bar.start()
    button_transcrever.configure(state="disabled")

    def executar():
        try:
            model = whisper.load_model("base")
            result = model.transcribe(entrada)
            with open(saida, "w", encoding="utf-8") as f:
                f.write(result["text"])
            status_var.set("Transcrição finalizada com sucesso!")
        except Exception as e:
            status_var.set("Erro na transcrição.")
            messagebox.showerror("Erro", str(e))
        finally:
            progress_bar.stop()
            button_transcrever.configure(state="normal")

    threading.Thread(target=executar).start()

# Layout visual
frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

entry_audio = ctk.CTkEntry(frame, textvariable=entrada_var, width=380)
entry_audio.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")
button_audio = ctk.CTkButton(frame, text="Selecionar Arquivo", command=escolher_arquivo, width=120)
button_audio.grid(row=0, column=1, pady=10)

entry_saida = ctk.CTkEntry(frame, textvariable=saida_var, width=380)
entry_saida.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="ew")
button_saida = ctk.CTkButton(frame, text="Selecionar Destino", command=escolher_destino, width=120)
button_saida.grid(row=1, column=1, pady=10)

button_transcrever = ctk.CTkButton(frame, text="Iniciar Transcrição", command=iniciar_transcricao, height=40)
button_transcrever.grid(row=2, column=0, columnspan=2, pady=(20, 10))

progress_bar = ctk.CTkProgressBar(frame, mode="indeterminate")
progress_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")

status_label = ctk.CTkLabel(frame, textvariable=status_var, anchor="center")
status_label.grid(row=4, column=0, columnspan=2, pady=(0, 10))

app.mainloop()
