# gui_bloqueante.py
import tkinter as tk
from tkinter import messagebox
from pydub import AudioSegment # Requiere pydub y ffmpeg
from pathlib import Path
import time
import os

# --- LÓGICA DE PROCESAMIENTO CPU/I/O-Bound (De tu archivo mp3_monoproceso.py) ---
# Hemos simplificado la función para que no necesite pasar Path en este contexto.

def normalize_and_export(path: Path):
    """
    Tarea CPU/I/O-Bound: Normaliza un WAV y lo exporta a MP3.
    """
    try:
        audio = AudioSegment.from_wav(path)
        # Normalización (proceso CPU-Bound en el código de pydub)
        normalized = audio.normalize() 
        out = path.with_suffix(".mp3")
        
        # Exportación (proceso I/O-Bound que usa FFmpeg)
        normalized.export(out, format="mp3")
        return out.name
    except FileNotFoundError:
        return f"ERROR: Archivo no encontrado: {path.name}"
    except Exception as e:
        return f"ERROR: Fallo al procesar {path.name}. {e}"


def run_audio_processing_blocking(status_label: tk.Label):
    """
    Ejecuta el procesamiento en el HILO PRINCIPAL de la GUI, causando el bloqueo.
    """
    INPUT_DIR = Path("audios") # Asume que hay un directorio 'audios'
    files = list(INPUT_DIR.glob("*.wav"))

    if not files:
        status_label.config(text="⚠️ No se encontraron archivos .wav en 'audios/'")
        return

    status_label.config(text=f"🔴 Iniciando procesamiento de {len(files)} archivos...")
    status_label.update() # Forzar la actualización visual

    t0 = time.perf_counter()
    
    # --- EJECUCIÓN BLOQUEANTE ---
    for f in files:
        result = normalize_and_export(f)
        print(f"Procesado: {result}")
    # --- FIN DE EJECUCIÓN BLOQUEANTE ---

    t1 = time.perf_counter()
    tiempo = t1 - t0
    
    status_label.config(text=f"🟢 ¡Proceso completado! Tiempo total: {tiempo:.2f} s")


# --- INTERFAZ GRÁFICA (Tkinter) ---

class App:
    def __init__(self, master):
        self.master = master
        master.title("Demostración de Bloqueo de GUI")

        # 1. Etiqueta de Estado
        self.status_label = tk.Label(master, 
                                     text="Listo para ejecutar.", 
                                     fg="blue", 
                                     pady=10)
        self.status_label.pack()

        # 2. Botón de Tarea Bloqueante
        self.process_button = tk.Button(master, 
                                        text="Procesar Audios (Bloqueante)", 
                                        command=lambda: run_audio_processing_blocking(self.status_label),
                                        bg="red", 
                                        fg="white",
                                        padx=20, pady=10)
        self.process_button.pack(pady=10)

        # 3. Botón de Tarea Rápida
        self.hello_button = tk.Button(master, 
                                      text="Decir Hola (Debe funcionar)", 
                                      command=self.show_hello_message,
                                      bg="green",
                                      padx=20, pady=10)
        self.hello_button.pack(pady=10)

    def show_hello_message(self):
        """Tarea simple que debe ejecutarse instantáneamente."""
        messagebox.showinfo("Hola", "¡Hola! La interfaz está respondiendo.")
        

if __name__ == "__main__":
    # Asegúrate de que existe el directorio de audios para evitar errores.
    if not Path("audios").exists():
         Path("audios").mkdir()
         print("Se ha creado el directorio 'audios/'. Coloca allí tus archivos .wav.")
    
    root = tk.Tk()
    app = App(root)
    root.mainloop()