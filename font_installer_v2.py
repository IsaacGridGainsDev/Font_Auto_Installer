import os
import sys
import platform
import shutil
import zipfile
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
import ctypes
import winreg

# ===== Check if running as admin =====
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# ===== Main App Class =====
class FontInstallerApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Font Installer")
        self.geometry("600x400")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.full_install_var = tk.BooleanVar()

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Install Fonts from ZIP Files", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=10)

        self.install_button = ctk.CTkButton(self, text="Select ZIP File(s)", command=self.select_zip_files)
        self.install_button.pack(pady=10)

        self.install_scope_checkbox = ctk.CTkCheckBox(self, text="Install for all apps (requires admin)", variable=self.full_install_var)
        self.install_scope_checkbox.pack()

        self.progress = ttk.Progressbar(self, mode="determinate", length=500)
        self.progress.pack(pady=10)

        self.log_box = tk.Text(self, height=10, wrap="word", bg="#1a1a1a", fg="white")
        self.log_box.pack(padx=10, pady=10, fill="both", expand=True)

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.update()

    def select_zip_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("ZIP files", "*.zip")])
        if not file_paths:
            return

        total = len(file_paths)
        self.progress["maximum"] = total
        self.progress["value"] = 0

        for i, zip_path in enumerate(file_paths, 1):
            self.progress["value"] = i
            self.log(f"🔍 Processing: {os.path.basename(zip_path)}")
            try:
                self.install_fonts_from_zip(zip_path)
            except Exception as e:
                self.log(f"❌ Error installing {os.path.basename(zip_path)}: {e}")
        self.log("✅ All done!")

    def install_fonts_from_zip(self, zip_path):
        extract_dir = Path("temp_fonts")
        extract_dir.mkdir(exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        font_extensions = ('.ttf', '.otf')
        font_files = [f for f in extract_dir.rglob("*") if f.suffix.lower() in font_extensions]

        for font in font_files:
            try:
                if platform.system() == "Windows":
                    if self.full_install_var.get():
                        if not is_admin():
                            self.log("⚠️ Admin required. Relaunching with elevated permissions...")
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
                else:
                    self.log("❌ Unsupported OS for this tool.")
            except PermissionError:
                self.log(f"🚫 Permission denied: {font.name}")
            except Exception as e:
                self.log(f"❌ Failed to install {font.name}: {e}")

        shutil.rmtree(extract_dir)

    def register_font_windows(self, font_name, font_path):
        try:
            font_key_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, font_key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, font_name, 0, winreg.REG_SZ, str(font_path))
            self.log(f"🔠 Registered font: {font_name}")
        except Exception as e:
            self.log(f"❌ Registry error for {font_name}: {e}")


if __name__ == "__main__":
    app = FontInstallerApp()
    app.mainloop()
