import os
import zipfile
import shutil
import platform
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def install_fonts_from_zip(zip_path, font_dir):
    extract_dir = Path("temp_fonts")
    extract_dir.mkdir(exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    font_extensions = ('.ttf', '.otf')
    font_files = [f for f in extract_dir.rglob("*") if f.suffix.lower() in font_extensions]

    for font in font_files:
        dest = font_dir / font.name
        shutil.copy2(font, dest)

    shutil.rmtree(extract_dir)

def get_system_font_dir():
    system = platform.system()
    if system == "Windows":
        return Path(os.environ['WINDIR']) / "Fonts"
    elif system == "Darwin":
        return Path.home() / "Library" / "Fonts"
    elif system == "Linux":
        font_dir = Path.home() / ".fonts"
        font_dir.mkdir(exist_ok=True)
        return font_dir
    else:
        return None

def refresh_font_cache():
    if platform.system() in ["Linux", "Darwin"]:
        os.system("fc-cache -f")

def process_folder(folder_path):
    font_dir = get_system_font_dir()
    if not font_dir:
        messagebox.showerror("Error", "Unsupported OS.")
        return

    zip_files = list(Path(folder_path).glob("*.zip"))
    if not zip_files:
        messagebox.showinfo("No ZIPs Found", "No ZIP font archives found in this folder.")
        return

    for zip_path in zip_files:
        try:
            install_fonts_from_zip(zip_path, font_dir)
        except Exception as e:
            print(f"Failed to install from {zip_path}: {e}")

    refresh_font_cache()
    messagebox.showinfo("Success", "✅ All fonts installed successfully.")

# --- GUI Code ---
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def install_fonts():
    folder_path = folder_var.get()
    if not folder_path:
        messagebox.showwarning("Missing Folder", "Please select a folder.")
        return
    process_folder(folder_path)

root = tk.Tk()
root.title("Font Installer from ZIP")
root.geometry("400x200")
root.resizable(False, False)

folder_var = tk.StringVar()

tk.Label(root, text="Select Folder with ZIP Font Files:", font=("Arial", 12)).pack(pady=10)
tk.Entry(root, textvariable=folder_var, width=40).pack(pady=5)
tk.Button(root, text="Browse", command=browse_folder).pack(pady=5)
tk.Button(root, text="Install Fonts", command=install_fonts, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=15)

root.mainloop()
