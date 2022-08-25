from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as msgbox
import pytube.exceptions
from pytube import YouTube
import time
import threading

# https://www.youtube.com/watch?v=q3FLmCfB0lo
# https://www.youtube.com/watch?v=4v1jvLsjnHA
# https://www.youtube.com/watch?v=7PsEhvvyK8I


def select_download_location():
    download_location = filedialog.askdirectory()
    if download_location == "":
        pass
    else:
        download_location_label.configure(text=download_location)


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = round(bytes_downloaded / total_size * 100)
    download_progress_label.configure(text=f"Download Progress : {progress}%")


def download():
    download_location = download_location_label.cget('text')
    if download_location == "Select Download Location":
        msgbox.showwarning(title="Oops", message="Please select download location!")
    else:
        url = url_entry.get()
        try:
            yt = YouTube(url, on_progress_callback=on_progress)
            root.title("Fetching Video ... Please Wait")
            video = yt.streams.get_highest_resolution()
            title_label.configure(text=f"Title : {yt.title}")
            channel_label.configure(text=f"Channel : {yt.author}")
            file_size_label.configure(text=f"File Size : {round(video.filesize * 0.000001, 2)} MB")
            root.title("Downloading ...")
            video.download(download_location)
            root.title("Download Complete")
            time.sleep(2)
            root.title("YouTube Downloader")
        except pytube.exceptions.RegexMatchError:
            msgbox.showwarning(title="Invalid Link", message="Please check the link again!")


def download_thread():
    threading.Thread(target=download).start()


def close_window():
    if msgbox.askokcancel(title="Confirm Exit", message="Are you sure you want to exit?"):
        root.destroy()

BG = "#c4302b"
FG = "#ffffff"
FONT = ('Times New Roman', 12)
FONT2 = ('Times New Roman', 10)

root = Tk()
root.title("YouTube Downloader")
root.resizable(False, False)
root.configure(bg=BG)

canvas = Canvas(root, width=128, height=50)
image = PhotoImage(file='youtube.png')
canvas.create_image(64, 25, image=image)
canvas.configure(bg=BG, highlightthickness=0)
canvas.pack(pady=10)

download_location_label = Label(root, text="Select Download Location", bg=BG, fg=FG, font=FONT)
download_location_label.pack()

select_button = Button(root, text="Select", width=10, command=select_download_location)
select_button.pack(pady=10)

label = Label(root, text="Paste YouTube Link Below", bg=BG, fg=FG, font=FONT)
label.pack()

url_entry = Entry(root, width=50)
url_entry.pack(padx=100)

download_button = Button(root, text="Download", width=10, command=download_thread)
download_button.pack(pady=10)

label2 = Label(root, text="Video Information", bg=BG, fg=FG, font=FONT)
label2.pack()

title_label = Label(root, text="Title : ", bg=BG, fg=FG, font=FONT2)
channel_label = Label(root, text="Channel : ", bg=BG, fg=FG, font=FONT2)
file_size_label = Label(root, text="File Size : ", bg=BG, fg=FG, font=FONT2)
download_progress_label = Label(root, text="Download Progress : ", bg=BG, fg=FG, font=FONT2)

title_label.pack(padx=10, pady=5, anchor=W)
channel_label.pack(padx=10, anchor=W)
file_size_label.pack(padx=10, pady=5, anchor=W)
download_progress_label.pack(padx=10, pady=(0, 10), anchor=W)

root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()
