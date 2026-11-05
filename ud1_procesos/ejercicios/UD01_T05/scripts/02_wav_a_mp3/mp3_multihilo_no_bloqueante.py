# gui_no_bloqueante_final.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from pydub import AudioSegment 
from pathlib import Path
import time
import threading 

# --- LÓGICA DE PROCESAMIENTO CPU/I/O-Bound (Función original de pydub) ---

def normalize_and_export(path: Path):
    """
    Tarea CPU/I/O-Bound: Normaliza un WAV y lo exporta a MP3.
    (Utiliza audio.normalize(), ahora funciona tras arreglar audioop)
    """
    try:
        audio = AudioSegment.from_wav(path)
        # Tarea CPU-Bound: Normalización que consume mucho tiempo
        normalized = audio.normalize() 
        out = path.with_suffix(".mp3")
        
        # Tarea I/O-Bound: Exportación (uso de FFmpeg)
        normalized.export(out, format="mp3")
        return out.name
    except Exception as e:
        return f"ERROR al procesar {path.name}: {e}"


def run_audio_processing(status_label: tk.Label, files):
    """
    Función que ejecuta la tarea pesada y actualiza la GUI.
    Se ejecuta DENTRO del hilo worker.
    """
    status_label.config(text=f"🔴 Iniciando procesamiento de {len(files)} archivos...")
    t0 = time.perf_counter()
    
    for i, f in enumerate(files):
        result = normalize_and_export(f)
        
        # La actualización de la GUI debe ser delegada al hilo principal (mainloop)
        # Usamos .after() para esto.
        status_label.after(1, status_label.config, {
            'text': f"⚙️ Procesando {f.name}... ({i+1}/{len(files)})"
        })
        
        print(f"Procesado: {result}")

    t1 = time.perf_counter()
    tiempo = t1 - t0
    
    # Actualización final de la GUI
    status_label.after(1, status_label.config, {
        'text': f"🟢 ¡Proceso completado! Tiempo total: {tiempo:.2f} s"
    })


# --- INTERFAZ GRÁFICA (Tkinter) ---

class App:
    def __init__(self, master):
        self.master = master
        master.title("Demostración de Hilos en GUI")

        self.INPUT_DIR = Path("audios") 
        self.files = list(self.INPUT_DIR.glob("*.wav"))

        if not self.files:
            tk.Label(master, text="⚠️ Coloca archivos .wav en la carpeta 'audios/'", fg="orange").pack(pady=10)
        
        # Etiqueta de estado
        self.status_label = tk.Label(master, text="Listo para ejecutar.", fg="blue", pady=10)
        self.status_label.pack()

        # Botones
        self.process_blocking_button = tk.Button(master, 
                                                 text="Procesar Audios (BLOQUEANTE)", 
                                                 command=self.run_blocking,
                                                 bg="red", fg="white", padx=20, pady=10)
        self.process_blocking_button.pack(pady=5)
        
        self.process_threading_button = tk.Button(master, 
                                                  text="Procesar Audios (THREADING)", 
                                                  command=self.run_threading,
                                                  bg="blue", fg="white", padx=20, pady=10)
        self.process_threading_button.pack(pady=5)

        self.hello_button = tk.Button(master, 
                                      text="Decir Hola (PRUEBA DE REACTIVIDAD)", 
                                      command=self.show_hello_message,
                                      bg="green", padx=20, pady=10)
        self.hello_button.pack(pady=20)

    # --- Lógica de Ejecución ---

    def _set_buttons_state(self, state):
        self.process_blocking_button.config(state=state)
        self.process_threading_button.config(state=state)

    def run_blocking(self):
        """Ejecuta la tarea en el hilo principal (BLOQUEA)."""
        self._set_buttons_state(tk.DISABLED)
        # Llama a la función directamente, bloqueando el mainloop
        run_audio_processing(self.status_label, self.files) 
        self._set_buttons_state(tk.NORMAL)


    def run_threading(self):
        """Lanza la tarea en un hilo secundario (NO BLOQUEA)."""
        self.status_label.config(text="🟡 Iniciando hilo secundario...")
        self._set_buttons_state(tk.DISABLED)
        
        # 1. Crear el hilo
        thread = threading.Thread(target=self.thread_worker, daemon=True)
        # 2. Iniciar el hilo
        thread.start()

    def thread_worker(self):
        """Función que se ejecuta en el hilo secundario."""
        
        # Ejecutar la tarea pesada
        run_audio_processing(self.status_label, self.files)
        
        # Al finalizar, usamos .after() para asegurar que la habilitación de botones
        # se ejecuta en el hilo principal de Tkinter (es la forma segura)
        self.master.after(100, self._set_buttons_state, tk.NORMAL)

    def show_hello_message(self):
        """Tarea simple que prueba la reactividad de la GUI."""
        messagebox.showinfo("Hola", "¡Hola! La interfaz está funcionando correctamente.")
        

if __name__ == "__main__":
    if not Path("audios").exists():
         Path("audios").mkdir()
         print("Se ha creado el directorio 'audios/'. Coloca allí tus archivos .wav.")
    
    root = tk.Tk()
    app = App(root)
    root.mainloop()