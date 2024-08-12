import tkinter as tk
import cv2
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, db
import json
import time
from multiprocessing import Process, Queue

# Load Firebase credentials
key_Path = "Api_Key/Api_Key.json"
file = open(key_Path)
Api_Key = json.load(file)

cred = credentials.Certificate("Api_Key/credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': Api_Key["Firebase_URL"]
})

# Function to fetch color from Firebase
def fetch_color(queue):
    ref = db.reference('assistant_status')
    while True:
        last_message = None
        last_message_key = None
        if len(ref.get()) > 1:
            for key, val in ref.get().items():
                last_message = val
                last_message_key = key
        if last_message:
            queue.put(last_message["message"])
            ref.child(last_message_key).delete()
        time.sleep(0.5)

# Function to update video frames
def update_video(queue, video_source):
    vid = cv2.VideoCapture(video_source)
    while True:
        ret, frame = vid.read()
        if ret:
            queue.put(frame)
        else:
            vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
        time.sleep(0.01)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

def interpolate_color(start_color, end_color, factor):
    return tuple(int(start + (end - start) * factor) for start, end in zip(start_color, end_color))

# Define the VideoPlayerApp class
class VideoPlayerApp:
    def __init__(self, window, video_source=0):
        self.window = window
        self.window.title("Video Player")
        
        self.video_source = video_source

        # Set the fixed window size to fit the screen resolution
        self.window.geometry("1024x600")

        self.border_frame = tk.Frame(window, highlightthickness=10)
        self.border_frame.grid(row=0, column=0, sticky=tk.NSEW)
        
        # Set the canvas size to fit within the fixed window size
        self.canvas = tk.Canvas(self.border_frame, width=1024, height=600)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

        self.btn_frame = tk.Frame(self.border_frame)
        self.btn_frame.grid(row=0, column=1, sticky=tk.NS)

        self.btn_stop = tk.Button(self.btn_frame, text="Stop", command=self.stop_video)
        self.btn_stop.pack(pady=5, fill=tk.X)

        # Adding the Gestures button with expandable options
        self.gesture_var = tk.StringVar(self.btn_frame)
        self.gesture_var.set("Gestures")

        self.gesture_options = ["Gesture 1", "Gesture 2", "Gesture 3", "Gesture 4"]
        self.gesture_menu = tk.OptionMenu(self.btn_frame, self.gesture_var, *self.gesture_options, command=self.handle_gesture)
        self.gesture_menu.pack(pady=5, fill=tk.X)
        
        self.loc_var = tk.StringVar(self.btn_frame)
        self.loc_var.set("Location")

        self.loc_options = ["University_Building", "Tech_Park", "Hi_Tech", "SRM_Hotel", "SRM_School_of_Architecture", "Java_Green_Food_Court", "Basic_Engineering_Lab", "Dental_College", "SRM_Global_Hospital", "SRM_Medical_College", "Biotech_Block", "SRM_Mechanical_Block", "Civil_Engineering_Block", "Electrical_Science_Block", "Aerospace_Hanger", "Mechanical_Hanger"]
        self.loc_menu = tk.OptionMenu(self.btn_frame, self.loc_var, *self.loc_options, command=self.handle_loc)
        self.loc_menu.pack(pady=5, fill=tk.X)

        # Make the grid layout expand with the window size
        self.border_frame.grid_rowconfigure(0, weight=1)
        self.border_frame.grid_columnconfigure(0, weight=1)
        self.border_frame.grid_columnconfigure(1, weight=0)

        # Queues for inter-process communication
        self.video_queue = Queue()
        self.color_queue = Queue()

        # Start the processes
        self.video_process = Process(target=update_video, args=(self.video_queue, self.video_source))
        self.color_process = Process(target=fetch_color, args=(self.color_queue,))
        self.video_process.start()
        self.color_process.start()

        self.current_color = (0, 0, 0)
        self.target_color = (0, 0, 0)
        self.update()

    def set_border_color(self, color):
        self.border_frame.config(highlightbackground=color)

    def play_video(self):
        self.update()

    def pause_video(self):
        pass

    def stop_video(self):
        self.video_process.terminate()
        self.color_process.terminate()
        self.window.quit()

    def handle_gesture(self, gesture):
        self.gesture_var.set("Gestures")
        print(f"Selected {gesture}")
        self.show_notification(f"Selected {gesture}")
        ref = db.reference('messages')
        ref.push().set({
            'message': gesture,
            'timestamp': int(time.time())
        })
        print("Message sent to Firebase")
        
    def handle_loc(self, loc):
        self.loc_var.set("Location")
        pass

    def show_notification(self, message):
        notification = tk.Toplevel(self.window)
        notification.overrideredirect(True)
        notification.attributes("-topmost", True)

        # Calculate the position to center the notification at the bottom
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 100
        y = self.window.winfo_y() + self.window.winfo_height() - 50
        notification.geometry(f"200x40+{x}+{y}")

        # Set a translucent background
        notification.attributes("-transparentcolor", "white")

        # Add a label with the notification message
        label = tk.Label(notification, text=message, bg="white", fg="black", padx=10, pady=5, font=("Arial", 12, "bold"))
        label.pack(fill=tk.BOTH, expand=True)

        def fade_in(window, alpha=0):
            alpha += 0.1
            if alpha < 1:
                window.attributes("-alpha", alpha)
                self.window.after(50, fade_in, window, alpha)
            else:
                self.window.after(4000, fade_out, window)

        def fade_out(window, alpha=1):
            alpha -= 0.1
            if alpha > 0:
                window.attributes("-alpha", alpha)
                self.window.after(50, fade_out, window, alpha)
            else:
                window.destroy()

        notification.attributes("-alpha", 0)
        fade_in(notification)

    def update(self):
        # Update the border color if there's a new color in the queue
        if not self.color_queue.empty():
            color_hex = self.color_queue.get()
            self.target_color = hex_to_rgb(color_hex)

        if self.current_color != self.target_color:
            self.current_color = interpolate_color(self.current_color, self.target_color, 0.3)
            self.set_border_color(rgb_to_hex(self.current_color))

        # Update the video frame if there's a new frame in the queue
        if not self.video_queue.empty():
            frame = self.video_queue.get()
            frame_resized = cv2.resize(frame, (800, 450))  # Resize frame to fit the video size
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)))
            # Calculate the y-coordinate to center the video vertically on the canvas
            y_offset = (600 - 450) // 2
            self.canvas.create_image(0, y_offset, image=self.photo, anchor=tk.NW)
            self.canvas.config(width=1024, height=600)

        self.window.after(10, self.update)

if __name__ == '__main__':
    # Create an instance of the Tkinter window
    root = tk.Tk()

    # Create an instance of the VideoPlayerApp
    app = VideoPlayerApp(root, "temp/EVA_Display_Video.mp4")

    # Start the Tkinter event loop
    root.mainloop()
