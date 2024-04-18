from UImain import *
import os

root = tk.Tk()

osName = "windows" if os.name == "nt" else "linux"
ui = Ui(root, "My Window", 1280, 720, False, "imgs\Icon.ico", "windows")

ui.run()