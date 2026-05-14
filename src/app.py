import os
import shutil
import subprocess
import customtkinter as ctk
from datetime import datetime

from config import load_json, save_json, CONFIG_FILE, HISTORY_FILE, DEFAULT_CONFIG
from lang import _, set_lang
from ui.sidebar import SidebarFrame
from ui.content import MainContentFrame


def _ensure_ffmpeg():
    if shutil.which("ffmpeg"):
        return True
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True)
        return True
    except FileNotFoundError:
        pass
    try:
        from imageio_ffmpeg import get_ffmpeg_exe
        exe = get_ffmpeg_exe()
        os.environ["PATH"] = os.path.dirname(exe) + os.pathsep + os.environ.get("PATH", "")
        return True
    except Exception:
        return False


class ConvertorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config = load_json(CONFIG_FILE, DEFAULT_CONFIG)
        if not os.path.exists(CONFIG_FILE):
            save_json(CONFIG_FILE, self.config)

        set_lang(self.config.get("language", "en"))

        self.history = load_json(HISTORY_FILE, [])

        self.title(_("app_title"))
        self.geometry("1280x800")
        self.minsize(1100, 680)
        self.configure(fg_color="#000000")

        ico_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SidebarFrame(self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main_area = MainContentFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew")

        self.after(200, self._check_ffmpeg)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _check_ffmpeg(self):
        if not _ensure_ffmpeg():
            import tkinter.messagebox as mb
            ret = mb.askyesno(
                _("app_title"),
                "FFmpeg is required for video & audio conversion.\n\n"
                "Download and install FFmpeg automatically?\n"
                "(~30 MB, https://ffmpeg.org)"
            )
            if ret:
                self._status_label = ctk.CTkLabel(
                    self.main_area.container, text="Downloading FFmpeg...",
                    font=ctk.CTkFont(family="Consolas", size=12),
                    text_color="#555555",
                )
                self._status_label.pack(pady=20)
                self.update()
                self._do_install_ffmpeg()

    def _do_install_ffmpeg(self):
        try:
            from imageio_ffmpeg import get_ffmpeg_exe
            exe = get_ffmpeg_exe()
            dst = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ffmpeg")
            os.makedirs(dst, exist_ok=True)
            dst_exe = os.path.join(dst, "ffmpeg.exe")
            if not os.path.exists(dst_exe):
                import shutil
                shutil.copy2(exe, dst_exe)
            os.environ["PATH"] = dst + os.pathsep + os.environ.get("PATH", "")
            import tkinter.messagebox as mb
            mb.showinfo(_("app_title"), "FFmpeg installed successfully!")
        except Exception as e:
            import tkinter.messagebox as mb
            mb.showerror(_("app_title"), f"Failed to install FFmpeg:\n{e}")

    def _on_close(self):
        save_json(CONFIG_FILE, self.config)
        save_json(HISTORY_FILE, self.history)
        self.destroy()

    def add_history(self, entry, category="convert"):
        if not self.config.get("save_history", True):
            return
        self.history.insert(0, {
            "src": entry.get("src", ""),
            "dst": entry.get("dst", ""),
            "cat": category,
            "t": datetime.now().isoformat(),
        })
        self.history = self.history[:50]
        save_json(HISTORY_FILE, self.history)

    def show_home(self):
        self.main_area.show_home()

    def show_image_convert(self):
        self.main_area.show_image_convert()

    def show_document_convert(self):
        self.main_area.show_document_convert()

    def show_audio_convert(self):
        self.main_area.show_audio_convert()

    def show_archive_tool(self):
        self.main_area.show_archive_tool()

    def show_data_convert(self):
        self.main_area.show_data_convert()

    def show_video_convert(self):
        self.main_area.show_video_convert()

    def show_history(self):
        self.main_area.show_history()

    def show_settings(self):
        self.main_area.show_settings()
