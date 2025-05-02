import os
import sys
import shutil
import zipfile
import time
import platform
import ctypes
import subprocess
import winreg
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
from ctypes import wintypes

# ========== Check Admin ==========
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# ========== Refresh Font Cache ==========
def refresh_font_cache():
    HWND_BROADCAST = 0xFFFF
    WM_FONTCHANGE = 0x001D
    SMTO_ABORTIFHUNG = 0x0002
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_FONTCHANGE,
        0,
        0,
        SMTO_ABORTIFHUNG,
        1000,
        ctypes.byref(wintypes.DWORD())
    )

def restart_explorer():
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    subprocess.Popen(["explorer.exe"])

# ========== Main App Class ==========
class FontInstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Font Installer")
        self.geometry("620x480")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.full_install_var = tk.BooleanVar()

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Install Fonts from ZIP Files or Folder", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="📁 Select ZIP File(s)", command=self.select_zip_files).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="📂 Select Folder", command=self.select_folder).grid(row=0, column=1, padx=10)

        ctk.CTkCheckBox(self, text="Install for all users (requires admin)", variable=self.full_install_var).pack()

        self.progress = ttk.Progressbar(self, mode="determinate", length=500)
        self.progress.pack(pady=10)

        self.log_box = tk.Text(self, height=12, wrap="word", bg="#1a1a1a", fg="white")
        self.log_box.pack(padx=10, pady=10, fill="both", expand=True)

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.update()

    def select_zip_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("ZIP files", "*.zip")])
        self.install_from_zip_list(file_paths)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            zip_files = [str(f) for f in Path(folder_path).glob("*.zip")]
            self.install_from_zip_list(zip_files)

    def install_from_zip_list(self, zip_paths):
        if not zip_paths:
            self.log("No ZIP files selected.")
            return

        self.progress["maximum"] = len(zip_paths)
        self.progress["value"] = 0

        for i, zip_path in enumerate(zip_paths, 1):
            self.progress["value"] = i
            self.log(f"🔍 Processing: {os.path.basename(zip_path)}")
            try:
                self.install_fonts_from_zip(zip_path)
            except Exception as e:
                self.log(f"❌ Error: {e}")

        if self.full_install_var.get():
            self.log("🔄 Refreshing font cache and restarting Explorer...")
            refresh_font_cache()
            restart_explorer()
        else:
            self.log("🔄 Refreshing font cache...")
            refresh_font_cache()

        self.log("✅ All done!")

    def install_fonts_from_zip(self, zip_path):
        extract_dir = Path("temp_fonts")
        extract_dir.mkdir(exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        font_files = [f for f in extract_dir.rglob("*") if f.suffix.lower() in (".ttf", ".otf")]
        for font in font_files:
            try:
                if platform.system() != "Windows":
                    self.log("❌ Unsupported OS.")
                    continue

                if self.full_install_var.get():
                    if not is_admin():
                        self.log("⚠️ Admin required. Relaunching...")
                        ctypes.windll.shell32.ShellExecuteW(
                            None, "runas", sys.executable, " ".join(sys.argv), None, 1
                        )
                        sys.exit()
                    dest = Path("C:/Windows/Fonts") / font.name
                else:
                    dest = Path.home() / "AppData/Local/Microsoft/Windows/Fonts" / font.name
                    dest.parent.mkdir(parents=True, exist_ok=True)

                shutil.copy2(font, dest)
                self.register_font_windows(font.name, dest)
                self.log(f"✅ Installed: {font.name}")
            except PermissionError:
                self.log(f"🚫 Permission denied: {font.name}")
            except Exception as e:
                self.log(f"❌ Failed to install {font.name}: {e}")

        shutil.rmtree(extract_dir)

    def register_font_windows(self, font_name, font_path):
        try:
            key_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, font_name, 0, winreg.REG_SZ, str(font_path))
            self.log(f"🔠 Registered: {font_name}")
        except Exception as e:
            self.log(f"❌ Registry error: {font_name} - {e}")

# ========== Run ==========
if __name__ == "__main__":
    app = FontInstallerApp()
    app.mainloop()
