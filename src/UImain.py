import tkinter as tk
import yaml

class Ui():
    def __init__(self, root, os="windows", configs="src\configs.yaml", icon=None, MainWindow = False):

        self.root = root

        if configs is not None:
            with open(configs, "r") as f:
                self.configs = yaml.load(f, Loader=yaml.FullLoader)
                self.configs = self.configs["Ui_config"]

        self.root.title(configs["title"])
        self.root.geometry(f"{configs["width"]}x{configs["height"]}")
        self.root.resizable(configs["resizable"], configs["resizable"])
        
        if icon == None:
            icon = configs["icon_path"]
           
        self.timesClicked = 0
        if os == "windows":
            self.root.iconbitmap(icon)

        if MainWindow:
            pass
        
    def run(self):    
        self.root.mainloop()
    
    
