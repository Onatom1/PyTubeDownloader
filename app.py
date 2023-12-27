import tkinter
from tkinter import *
from tkinter import ttk, filedialog
import datetime
from PIL import ImageTk, Image, ImageOps, ImageDraw
import requests
from pytube import YouTube
from tkinter.ttk import Progressbar
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

# Cores utilizadas no programa
cor0 = "#444466"  # Preta
cor1 = "#feffff"  # Branca
cor2 = "#6f9fbd"  # Azul
cor3 = "#38576b"  # Valor
cor4 = "#403d3d"  # Letra

background = "#3b3b3b"  # Cor de fundo da interface

# Configuração da janela principal
janela = Tk()
janela.title('')
janela.geometry('500x300')
janela.configure(bg=background)

# Criação de um separador horizontal na janela
ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=250)

# Frame principal
frame_principal = Frame(janela, width=500, height=110, bg=background, pady=5, padx=0, relief="flat")
frame_principal.grid(row=1, column=0)

# Frame de quadros
frame_quadros = Frame(janela, width=500, height=300, bg=background, pady=12, padx=0, relief="flat")
frame_quadros.grid(row=2, column=0, sticky=NW)

# Logo do YouTube
logo = Image.open('image/youtube.png')
logo = logo.resize((50, 50), Image.BICUBIC)
logo = ImageTk.PhotoImage(logo)
l_logo = Label(frame_principal, image=logo, compound=LEFT, bg=background, fg="white", font=('Ivy 10 bold'), anchor="nw", relief=FLAT)
l_logo.place(x=5, y=10)

# Logo personalizada
img_0 = Image.open('image/log.png')
img_0 = img_0.resize((45, 45), Image.BICUBIC)
img_0 = ImageTk.PhotoImage(img_0)
logo_label = Label(frame_principal, image=img_0, bg=background)
logo_label.image = img_0
logo_label.place(x=440, y=10)

# Nome do aplicativo
app_nome = Label(frame_principal, text="YouTube Downloader app", width=30, height=1, padx=0, relief="flat", anchor="nw", font=('Ivy 15 bold'), bg=background, fg=cor1)
app_nome.place(x=65, y=15)

def search():
    global img
    url = e_url.get()
    yt = YouTube(url)
    l_concluido.place_forget()

    # Obtém informações sobre o vídeo
    title = yt.title
    view = yt.views
    duration = str(datetime.timedelta(seconds=yt.length))
    Description = yt.description
    cover = yt.thumbnail_url

    print(cover)

    # Exibe a imagem do vídeo
    img_ = Image.open(requests.get(cover, stream=True).raw)
    img_ = img_.resize((230, 150), Image.BICUBIC)
    img_ = ImageTk.PhotoImage(img_)

    img = img_
    l_image['image'] = img

    # Atualiza os rótulos com informações do vídeo
    l_title['text'] = "Titulo: " + str(title)
    l_view['text'] = "Views: " + str('{:,}'.format(view))
    l_time['text'] = "Duracao: " + str(duration)

    # Mostra os botões após a busca
    b_download_audio.place(x=360, y=110)
    b_download_video.place(x=360, y=140)

previousprogress = 0

def on_progress(stream, chunk, bytes_remaining):
    global previousprogress
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    liveprogress = (int)(bytes_downloaded / total_size * 100)
    if liveprogress > previousprogress:
        previousprogress = liveprogress
        print(liveprogress)
        bar.place(x=250, y=120)
        bar['value'] = liveprogress
        janela.update_idletasks()

def choose_download_directory():
    download_dir = filedialog.askdirectory()
    if download_dir:
        os.chdir(download_dir)

def download_audio():
    global previousprogress
    previousprogress = 0  # Reiniciar a barra de progresso
    l_concluido.place_forget()  # Ocultar o rótulo "Concluído"
    choose_download_directory()  # Perguntar ao usuário pelo diretório de download
    download(audio=True)

def download_video():
    global previousprogress
    previousprogress = 0  # Reiniciar a barra de progresso
    l_concluido.place_forget()  # Ocultar o rótulo "Concluído"
    choose_download_directory()  # Perguntar ao usuário pelo diretório de download
    download(audio=False)
    

def download(audio=False):
    url = e_url.get()
    yt = YouTube(url)
    yt.register_on_progress_callback(on_progress)

    title = yt.title
    title = "".join(c for c in title if c.isalnum() or c.isspace())
    title = title[:100]
    
    if audio:
        # Filtra streams de áudio e seleciona a de maior qualidade
        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        extension = "mp3"
    else:
        # Filtra streams de vídeo e seleciona a de maior resolução
        stream = yt.streams.filter(only_audio=False, progressive=True).order_by('resolution').desc().first()
        extension = "mp4"

    # Oculta o rótulo "Concluído" antes de iniciar o download
    l_concluido.place_forget()
    
    downloaded_file = stream.download(filename=title)
    
    new_file_name = f"{title}.{extension}"
    os.rename(downloaded_file, new_file_name)

    print(f"Download completo: {new_file_name}")

    # Substitui a barra de progresso por um rótulo de conclusão
    bar.place_forget()
    l_concluido.place(x=250, y=120)

# Rótulos e entrada de URL
l_url = Label(frame_principal, text="Digite a URL", height=1, pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 10 bold'), bg=background, fg=cor1)
l_url.place(x=10, y=80)

e_url = Entry(frame_principal, width=50, justify='left', relief=SOLID)
e_url.place(x=100, y=80)

b_search = Button(frame_principal, text="Search", width=10, height=1, bg=cor2, fg=cor1, font=('Ivy 7 bold'),relief=RAISED, overrelief=RIDGE, command=lambda: search())
b_search.place(x=404, y=80)

# Quadros de operações
l_image = Label(frame_quadros, compound=LEFT, bg=background, fg="white", font=('Ivy 10 bold'), anchor="nw", relief=FLAT)
l_image.place(x=10, y=10)

l_title = Label(frame_quadros, height=2, pady=0, padx=0, relief="flat", wraplength=225, compound=LEFT, justify='left',anchor=NW, font=('Ivy 10 bold'), bg=background, fg=cor1)
l_title.place(x=250, y=15)

l_view = Label(frame_quadros, height=1, pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 8 bold'), bg=background,fg=cor1)
l_view.place(x=250, y=60)

l_time = Label(frame_quadros, height=1, pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 8 bold'), bg=background,fg=cor1)
l_time.place(x=250, y=85)

# Rótulo de conclusão
l_concluido = Label(frame_quadros, text="Concluído!", font=('Ivy 10 bold'), bg=background, fg=cor1)

# Botões de download
b_download_audio = Button(frame_quadros, text="Download Áudio", width=15, height=1, bg=cor2, fg=cor1,font=('Ivy 10 bold'), relief=FLAT, overrelief=RIDGE, command=download_audio)
b_download_video = Button(frame_quadros, text="Download Vídeo", width=15, height=1, bg=cor2, fg=cor1,font=('Ivy 10 bold'), relief=FLAT, overrelief=RIDGE, command=download_video)
b_download_audio.place_forget()
b_download_video.place_forget()

# Estilo da barra de progresso
style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='#00E676')
style.configure("TProgressbar", thickness=6)

bar = Progressbar(frame_quadros, length=100, style='black.Horizontal.TProgressbar')

# Rodapé
rodape_label = Label(janela, text='By Yury Mota', font=('Verdana 7'), bg=background, fg='#feffff')
rodape_label.place(relx=0.08, rely=0.954, anchor=N)

# Inicia o loop principal da interface gráfica
janela.mainloop()