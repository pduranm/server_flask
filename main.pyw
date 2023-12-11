# env: executableTkinter
import tkinter
from tkinter import ttk, filedialog, messagebox, font
from customtkinter import CTkEntry, CTkButton, CTkFont
from pytube import YouTube
from threading import Thread

def select_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        exit_path.set(directory_path)

def download_video():
    url = video_url.get()
    exit_dir = exit_path.get()
    
    video = YouTube(url)
    stream = video.streams.get_highest_resolution()

    def download():
        stream.download(output_path=exit_dir)
        progress_var.set(100)  # Establece la barra de progreso al 100% después de la descarga
        download_button.configure(state=tkinter.NORMAL)  # Habilita el botón después de la descarga
        messagebox.showinfo("Descarga completada", "La descarga se ha completado.")

    # Inicia un hilo para la descarga
    download_thread = Thread(target=download)
    download_thread.start()

    # Deshabilita el botón durante la descarga
    download_button.configure(state=tkinter.DISABLED)

    # Actualiza la barra de progreso mientras se descarga
    def update_progress():
        while download_thread.is_alive():
            progress_var.set(int(stream.progress * 100))
            window.update()
        progress_var.set(100)  # Asegúrate de que la barra de progreso esté completa al finalizar

    # Inicia un hilo para actualizar la barra de progreso
    progress_thread = Thread(target=update_progress)
    progress_thread.start()

window = tkinter.Tk()
window.title("Descargar vídeos de Youtube")
window.geometry("530x200")  # Ajusta las dimensiones de la ventana según tu preferencia
window.resizable(width=False, height=False)
window.configure(bg='#252525')

# Configura el tamaño de la fuente
custom_font = CTkFont(family='Helvetica', size=12)  # Ajusta el tamaño según tus necesidades

video_url = CTkEntry(
    master=window,
    placeholder_text='Pon la URL aquí...',
    font=custom_font,
    width=345,
    height=35,
)

exit_path = tkinter.StringVar()

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

progress_var = tkinter.IntVar()

progress_bar = ttk.Progressbar(
    window,
    orient='horizontal',
    length=345,
    mode='determinate',
    variable=progress_var,
)

download_button = CTkButton(
    master=window,
    command=download_video,
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

# Configura el factor de escalado
window.tk.call('tk', 'scaling', 2.0)  # Ajusta el factor según tus necesidades

# placing the widgets
video_url.place(x=18, y=20)
exit_path_entry.place(x=18, y=65)
select_directory_button.place(x=380, y=65)
progress_bar.place(x=18, y=110)
download_button.place(x=380, y=110)

window.mainloop()
