# 🖋️ Font Installer GUI for Windows

A modern Python application that automates installing fonts from ZIP files or folders. Built with a clean `CustomTkinter` interface, it ensures fonts are properly extracted, registered, and available immediately in applications like Photoshop.

---

## 🚀 Features

- 📁 Select multiple ZIP files or a folder containing ZIPs
- 📦 Extracts `.ttf` and `.otf` fonts from archives
- 💾 Installs fonts to system or user font directories
- 🧠 Adds fonts to the Windows Registry
- 🔄 Automatically refreshes font cache and restarts Explorer
- 🛡️ Admin rights check with auto-elevation when needed
- 📊 Progress bar and scrollable activity log
- ☑️ "Install for all users" toggle

---

## 📥 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/font-installer-gui.git
   cd font-installer-gui

2. **Install dependencies:**

   ```bash
   
   pip install -r requirements.txt
3. **Run the application:**

   ```bash
   python font_installer_gui.py

4. **🧾 Requirements**
Python 3.9 or newer

Windows 10 or 11

Admin privileges (for full system font install)

   **🗃️ requirements.txt**:

         customtkinter

   **Install with:**

      pip install -r requirements.txt

5. **🖥️ How to Use:**
Launch the app.

   Click "Select ZIPs" to choose individual font archives.

   Or click "Select Folder" to process all ZIPs in a directory.

   Optionally check "Install for all users" (requires admin).

   Watch the log and progress bar for updates.

   When done:

   Fonts are installed.

   Registry is updated.

   Font cache is refreshed.

   Windows Explorer restarts to reflect changes instantly.

6. **⚠️ Troubleshooting**
   Fonts may not appear in software like Photoshop until Explorer is restarted (handled automatically).

   Without admin rights, fonts are installed for the current user only.

7. **🪪 License**
   MIT License

8. **🙌 Credits**
   Developed with ❤️ using Python and CustomTkinter
