from flask import Flask, render_template, request, redirect, url_for, flash
from flaskwebgui import FlaskUI
import tkinter as tk
from tkinter import ttk, filedialog, font
from customtkinter import CTkEntry, CTkButton, CTkFont
from pytube import YouTube
from threading import Thread

app = Flask(__name__)

FlaskUI(app, width=530, height=200)
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Configuración de la interfaz gráfica de usuario
class FlaskApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

# Resto del código de tu aplicación (sin el bucle principal de Tkinter)
# ...

def select_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        exit_path.set(directory_path)
    pass

def download_video_flask():
    url = request.form['video_url']  # Obtén la URL del formulario
    exit_dir = request.form['exit_path']  # Obtén la ruta de salida del formulario

    video = YouTube(url)
    stream = video.streams.get_highest_resolution()

    def download():
        stream.download(output_path=exit_dir)
        progress_var.set(100)
        download_button.configure(state=tk.NORMAL)
        window.after(100, lambda: flash("Descarga completada"))

    download_thread = Thread(target=download)
    download_thread.start()

    download_button.configure(state=tk.DISABLED)

    def update_progress():
        while download_thread.is_alive():
            window.after(100, lambda: progress_var.set(int(stream.progress * 100)))
            window.update()
        window.after(100, lambda: progress_var.set(100))

    progress_thread = Thread(target=update_progress)
    progress_thread.start()

    return 'Descarga iniciada'

# Configuración de la ventana Tkinter
window = FlaskApp()
window.title("Descargar vídeos de Youtube")
window.geometry("530x200")
window.resizable(width=False, height=False)
window.configure(bg='#252525')

# Configuración de la fuente
custom_font = CTkFont(family='Helvetica', size=12)

video_url = CTkEntry(
    master=window,
    placeholder_text='Pon la URL aquí...',
    font=custom_font,
    width=345,
    height=35,
)

# Importa tkinter directamente
exit_path = tk.StringVar()

exit_path_entry = CTkEntry(
    master=window,
    placeholder_text='Pega aquí la ruta de guardado...',
    textvariable=exit_path,
    font=custom_font,
    width=345,
    height=35,
)

select_directory_button = CTkButton(
    master=window,
    command=select_directory,
    text="Seleccionar Carpeta",
    text_color="white",
    hover=True,
    hover_color="black",
    font=custom_font,
    height=35,
    width=150,
    border_width=2,
    corner_radius=4,
    border_color="#5d6266",
    bg_color="#262626",
    fg_color="#262626",
)

progress_var = tk.IntVar()

progress_bar = ttk.Progressbar(
    window,
    orient='horizontal',
    length=345,
    mode='determinate',
    variable=progress_var,
)

download_button = CTkButton(
    master=window,
    command=download_video_flask,
    text="Descargar",
    text_color="white",
    hover=True,
    hover_color="black",
    font=custom_font,
    height=35,
    width=120,
    border_width=2,
    corner_radius=4,
    border_color="#5d6266",
    bg_color="#262626",
    fg_color="#262626",
)

# Coloca los widgets en la ventana
video_url.place(x=18, y=20)
exit_path_entry.place(x=18, y=65)
select_directory_button.place(x=380, y=65)
progress_bar.place(x=18, y=110)
download_button.place(x=380, y=110)

# Ruta para renderizar la página principal
@app.route('/')
def index():
    return render_template('index.html')  # Asegúrate de tener un archivo HTML adecuado

# Ruta para manejar la descarga del video
@app.route('/download_video', methods=['POST'])
def download_video_flask_route():
    return download_video_flask()

if __name__ == '__main__':
    app.run()

# meter un input de números para poner cual es el numero exacto de videos de la playlist
# hacer un bucle para que vaya recorriendo la url que se introduce y sumando +1 al index para ir cambiando de vídeo.
