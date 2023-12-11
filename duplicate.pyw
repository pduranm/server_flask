from flask import Flask, render_template, request, flash
from flaskwebgui import FlaskUI
import tkinter as tk
from tkinter import ttk, filedialog
from customtkinter import CTkEntry, CTkButton, CTkFont
from pytube import YouTube, Playlist
from threading import Thread

app = Flask(__name__)
FlaskUI(app, width=530, height=200)

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

def download_video_flask():
    url = request.form['video_url']
    exit_dir = request.form['exit_path']
    video_quality = request.form['video_quality']

    video = YouTube(url)
    stream = video.streams.filter(res=video_quality).first()

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

def download_playlist_flask():
    playlist_url = request.form['playlist_url']
    exit_dir = request.form['exit_path']
    video_quality = request.form['video_quality']

    playlist = Playlist(playlist_url)

    def download():
        for video in playlist.videos:
            stream = video.streams.filter(res=video_quality).first()
            stream.download(output_path=exit_dir)

        progress_var.set(100)
        download_button.configure(state=tk.NORMAL)
        window.after(100, lambda: flash("Descarga de la lista de reproducción completada"))

    download_thread = Thread(target=download)
    download_thread.start()

    download_button.configure(state=tk.DISABLED)

    def update_progress():
        while download_thread.is_alive():
            window.after(100, lambda: progress_var.set(int(playlist.download_progress() * 100)))
            window.update()
        window.after(100, lambda: progress_var.set(100))

    progress_thread = Thread(target=update_progress)
    progress_thread.start()

    return 'Descarga de la lista de reproducción iniciada'

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
    text="Descargar Video",
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

download_playlist_button = CTkButton(
    master=window,
    command=download_playlist_flask,
    text="Descargar Lista de Reproducción",
    text_color="white",
    hover=True,
    hover_color="black",
    font=custom_font,
    height=35,
    width=200,
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
download_button.place(x=100, y=110)
download_playlist_button.place(x=240, y=110)

# Resto del código de Flask...
# ...

# Rutas para renderizar la página principal y manejar la descarga de video y lista de reproducción
@app.route('/')
def index():
    return render_template('index.html')  # Asegúrate de tener un archivo HTML adecuado

@app.route('/download_video', methods=['POST'])
def download_video_flask_route():
    return download_video_flask()

@app.route('/download_playlist', methods=['POST'])
def download_playlist_flask_route():
    return download_playlist_flask()

if __name__ == '__main__':
    app.run()

