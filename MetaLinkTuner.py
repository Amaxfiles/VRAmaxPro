import os
import sys
import subprocess
import winreg
import webbrowser
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# ---
COLOR_BG_DARK = "#0B132B"       
COLOR_CYAN = "#00FBEC"          
COLOR_BLUE_TECH = "#1F509E"     
COLOR_AMBER = "#FF9F29"         
COLOR_FRAME = "#1C2541"         

CONFIG_FILE = "vramax_config.txt"

def ressource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class VRAMaxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VRAmax PRO")
        self.geometry("600x850")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_DARK)
        self.current_lang = "en"
        self.is_loading_config = False
        self.cli_path = self.find_oculus_cli()
        
    

    def apply_settings(self):
        t = LANGUAGES[self.current_lang]
        try:
            bitrate = int(self.entry_bitrate.get())
        except ValueError:
            self.status_label.configure(text="Error: Invalid Bitrate", text_color="red")
            return

        override = self.entry_override.get()
        fov = self.entry_fov.get()
        current_cli = self.entry_dir.get().strip()

        if not os.path.exists(current_cli):
            self.status_label.configure(text=t["err_cli"], text_color="red")
            return

        cli_commands = f"service set-pixels-per-display-pixel-override {override}\n"
        if fov != "0.0" and fov != "0":
            cli_commands += f"service set-client-fov-tan-angle-multiplier {fov} {fov}\n"
        cli_commands += "server:asw.Off\n"

        try:
            process = subprocess.Popen([current_cli], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            process.communicate(input=cli_commands)
        except Exception as e:
            self.status_label.configure(text=f"CLI Error: {str(e)}", text_color="red")
            return

        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Oculus\RemoteHeadset", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(reg_key, "HEVC", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "BitrateMbps", 0, winreg.REG_DWORD, bitrate)
            winreg.SetValueEx(reg_key, "DBR", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(reg_key, "ResolutionWidth", 0, winreg.REG_DWORD, 4128)
            winreg.SetValueEx(reg_key, "LinkSharpening", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(reg_key)
            self.status_label.configure(text=t["succ_inject"], text_color=COLOR_CYAN)
        except Exception as e:
            self.status_label.configure(text=f"Registry Error: {str(e)}", text_color="red")

  

if __name__ == "__main__":
    app = VRAMaxApp()
    app.mainloop()
