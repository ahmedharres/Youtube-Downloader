import customtkinter as ctk 
from tkinter.ttk import Combobox
from pytube import YouTube
import os 

def download_video():
    url = entry_url.get()
    resolution = resolution_var.get()
    
    progress_lable.pack(pady=10)
    progress_bar.pack(pady=10)
    status_lable.pack(pady=10)
    
    try:
        # Print selected resolution
        print("Selected Resolution:", resolution) 

        yt = YouTube(url, on_progress_callback=on_progress)
       
        # Filter streams by the selected resolution
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()

        if stream:
            # Download video into a specific directory
            output_path = os.path.join("downloads", f"{yt.title}.mp4")
            stream.download(output_path="downloads")
        else:
            raise ValueError("No stream available with the selected resolution.")

        
    except Exception as e:
        status_lable.configure(text=f"Error: {str(e)}", text_color="white", fg_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = bytes_downloaded / total_size * 100
    
    progress_lable.configure(text=str(int(percentage_completed)) + "%")
    progress_lable.update()

    progress_bar.set(float(percentage_completed / 100 ))
# create a root window 
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
 
# title of the window
root.title("Youtube Downloader!")

# set min and max width and height
root.geometry("720x480")
root.minsize(720, 480)
root.maxsize(1080, 720)

# create frame to hold the content
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

# create a label and entry widget for video url
url_label = ctk.CTkLabel(content_frame, text="Enter Youtube URL Video")
entry_url = ctk.CTkEntry(content_frame, width=400, height=40) 
url_label.pack(pady=10)
entry_url.pack(pady=10)

# create a resolutions combo box

resolutions = ["720p","480p", "360p", "240p","144p"]
resolution_var = ctk.StringVar(value="720p")  # Set initial value
resolution_combobox = Combobox(content_frame, values=resolutions, textvariable=resolution_var, state="readonly",style='Dark.TCombobox')
resolution_combobox.pack(pady=10)


# create a download button
download_button = ctk.CTkButton(content_frame, text="Download", command=download_video)
download_button.pack(pady=10)

# create label to display download progress
progress_lable = ctk.CTkLabel(content_frame, text="0%")
progress_bar = ctk.CTkProgressBar(content_frame, width=400)
progress_bar.set(0)

# create status label
status_lable = ctk.CTkLabel(content_frame, text="")

root.mainloop()