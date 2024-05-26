import tkinter as tk
import cv2
from PIL import Image, ImageTk

class VideoPlayerApp:
    def __init__(self, window, video_source=0):
        self.window = window
        self.window.title("Video Player")

        self.video_source = video_source

        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_frame = tk.Frame(window)
        self.btn_frame.pack(pady=10)

        self.btn_play = tk.Button(self.btn_frame, text="Play", command=self.play_video)
        self.btn_play.pack(side=tk.LEFT, padx=10)

        self.btn_pause = tk.Button(self.btn_frame, text="Pause", command=self.pause_video)
        self.btn_pause.pack(side=tk.LEFT, padx=10)

        self.btn_stop = tk.Button(self.btn_frame, text="Stop", command=self.stop_video)
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        self.update()

        self.window.mainloop()

    def play_video(self):
        self.update()

    def pause_video(self):
        pass

    def stop_video(self):
        self.vid.release()
        self.window.quit()

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        else:
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0) 

        self.window.after(10, self.update)

app = VideoPlayerApp(tk.Tk(), "temp\EVA_Display_Video.mp4")
