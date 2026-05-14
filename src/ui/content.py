import customtkinter as ctk
from config import load_icon
from lang import _, set_lang, get_lang
from ui.home_view import HomeView
from ui.image_view import ImageConvertView
from ui.document_view import DocumentConvertView
from ui.audio_view import AudioConvertView
from ui.archive_view import ArchiveToolView
from ui.data_view import DataConvertView
from ui.video_view import VideoConvertView

_SIDEBAR_KEY_MAP = {
    "home": ["home"],
    "image": ["image", "png", "jpg", "webp", "bmp", "gif", "tiff", "ico"],
    "file": ["document", "pdf", "docx", "txt"],
    "video": ["video", "mp4", "avi", "mov", "mkv", "webm"],
    "music": ["audio", "mp3", "wav", "ogg", "flac"],
    "folder": ["archive", "zip", "tar"],
    "database": ["data", "csv", "json"],
    "history": ["history"],
    "settings": ["settings"],
}


class MainContentFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#000000", corner_radius=0)
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, fg_color="#050505", height=48, corner_radius=0)
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_columnconfigure(1, weight=1)
        self.top_bar.grid_propagate(False)

        icon = load_icon("convert", (18, 18))
        ctk.CTkLabel(
            self.top_bar, text=f"  {_('app_title')}",
            image=icon,
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
            text_color="#ffffff", compound="left",
        ).grid(row=0, column=0, padx=(16, 8), pady=10, sticky="w")

        self.global_entry = ctk.CTkEntry(
            self.top_bar,
            placeholder_text=_("search_tool"),
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color="#0a0a0a", border_color="#1a1a1a",
            text_color="#cccccc", height=28, width=260,
        )
        self.global_entry.grid(row=0, column=1, padx=8, pady=10, sticky="e")
        self.global_entry.bind("<Return>", self._on_search)

        gs_icon = load_icon("search", (14, 14))
        ctk.CTkButton(
            self.top_bar, text="", image=gs_icon,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#0a0a0a", hover_color="#1a1a1a",
            text_color="#ffffff", width=32, height=28,
            corner_radius=0, command=self._on_search_click,
        ).grid(row=0, column=2, padx=(0, 12), pady=10)

        self.container = ctk.CTkScrollableFrame(
            self, fg_color="#000000", corner_radius=0,
            scrollbar_button_color="#1a1a1a",
            scrollbar_button_hover_color="#ffffff",
        )
        self.container.grid(row=1, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)

        self.show_home()

    def _nav_to(self, sidebar_key, show_func):
        self.global_entry.delete(0, "end")
        if hasattr(self.parent, "sidebar") and hasattr(self.parent.sidebar, "_set_active"):
            self.parent.sidebar._set_active(sidebar_key)
        show_func()

    def _on_search(self, e=None):
        q = self.global_entry.get().strip().lower()
        if not q:
            return
        for key, keywords in _SIDEBAR_KEY_MAP.items():
            for kw in keywords:
                if kw in q:
                    handler_map = {
                        "home": self.show_home,
                        "image": self.show_image_convert,
                        "file": self.show_document_convert,
                        "video": self.show_video_convert,
                        "music": self.show_audio_convert,
                        "folder": self.show_archive_tool,
                        "database": self.show_data_convert,
                        "history": self.show_history,
                        "settings": self.show_settings,
                    }
                    h = handler_map.get(key)
                    if h:
                        self._nav_to(key, h)
                    return

    def _on_search_click(self):
        self._on_search()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_home(self):
        self.clear()
        HomeView(self, self.parent)

    def show_image_convert(self):
        self.clear()
        ImageConvertView(self, self.parent)

    def show_document_convert(self):
        self.clear()
        DocumentConvertView(self, self.parent)

    def show_audio_convert(self):
        self.clear()
        AudioConvertView(self, self.parent)

    def show_archive_tool(self):
        self.clear()
        ArchiveToolView(self, self.parent)

    def show_data_convert(self):
        self.clear()
        DataConvertView(self, self.parent)

    def show_video_convert(self):
        self.clear()
        VideoConvertView(self, self.parent)

    def show_history(self):
        self.clear()
        c = self.container

        ctk.CTkLabel(
            c, text=f">_ {_('history_title')}",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(16, 4))
        ctk.CTkFrame(c, height=1, fg_color="#1a1a1a").grid(row=1, column=0, sticky="ew", pady=(0, 16))

        if not self.parent.history:
            ctk.CTkLabel(
                c, text=f"[ {_('history_empty')} ]",
                font=ctk.CTkFont(family="Consolas", size=13),
                text_color="#444444",
            ).grid(row=2, column=0, pady=20)
            return

        cat_info = {
            "image": ("show_image_convert", "image"),
            "document": ("show_document_convert", "file"),
            "video": ("show_video_convert", "video"),
            "audio": ("show_audio_convert", "music"),
            "archive": ("show_archive_tool", "folder"),
            "data": ("show_data_convert", "database"),
        }

        for i, h in enumerate(self.parent.history):
            card = ctk.CTkFrame(c, fg_color="#050505", corner_radius=0, border_width=1, border_color="#1a1a1a")
            card.grid(row=2 + i, column=0, sticky="ew", pady=2)
            card.columnconfigure(1, weight=1)

            ic = load_icon("history", (14, 14))
            ctk.CTkLabel(card, text="", image=ic).grid(row=0, column=0, padx=(10, 4), pady=8)

            src = h.get("src", "?")
            dst = h.get("dst", "?")
            cat = h.get("cat", "")
            ctk.CTkLabel(
                card, text=f"  {src}  →  {dst}   [{cat}]",
                font=ctk.CTkFont(family="Consolas", size=12),
                text_color="#cccccc", anchor="w",
            ).grid(row=0, column=1, sticky="w")

            info = cat_info.get(cat)
            if info:
                method_name, sidebar_key = info
                method = getattr(self, method_name)
                ctk.CTkButton(
                    card, text=f"[ {_('open')} ]",
                    font=ctk.CTkFont(family="Consolas", size=10),
                    fg_color="transparent", hover_color="#111111",
                    text_color="#555555", corner_radius=0,
                    command=lambda m=method, k=sidebar_key: self._nav_to(k, m),
                ).grid(row=0, column=2, padx=(4, 10))

    def show_settings(self):
        self.clear()
        c = self.container
        app = self.parent

        ctk.CTkLabel(
            c, text=f">_ {_('settings_title')}",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(16, 4))
        ctk.CTkFrame(c, height=1, fg_color="#1a1a1a").grid(row=1, column=0, sticky="ew", pady=(0, 16))

        card = ctk.CTkFrame(c, fg_color="#050505", corner_radius=0, border_width=1, border_color="#1a1a1a")
        card.grid(row=2, column=0, sticky="ew", pady=4)
        card.columnconfigure(1, weight=1)

        row = 0
        ctk.CTkLabel(
            card, text=f"  {_('save_history')}",
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color="#cccccc", anchor="w",
        ).grid(row=row, column=0, padx=14, pady=10, sticky="w")

        hist_var = ctk.BooleanVar(value=app.config.get("save_history", True))
        ctk.CTkSwitch(
            card, text="", variable=hist_var,
            fg_color="#1a1a1a", progress_color="#ffffff",
            command=lambda: app.config.update(save_history=hist_var.get()),
        ).grid(row=row, column=1, padx=14, pady=10, sticky="e")
        row += 1

        ctk.CTkFrame(card, height=1, fg_color="#1a1a1a").grid(row=row, column=0, columnspan=2, sticky="ew")
        row += 1

        ctk.CTkLabel(
            card, text=f"  {_('image_quality')}",
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color="#cccccc", anchor="w",
        ).grid(row=row, column=0, padx=14, pady=10, sticky="w")

        quality_var = ctk.IntVar(value=app.config.get("image_quality", 90))
        ctk.CTkSlider(
            card, from_=10, to=100, variable=quality_var,
            fg_color="#1a1a1a", progress_color="#ffffff",
            command=lambda v: app.config.update(image_quality=int(v)),
        ).grid(row=row, column=1, padx=14, pady=10, sticky="ew")
        row += 1

        ctk.CTkLabel(
            card, text=f"  {_('audio_bitrate')}",
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color="#cccccc", anchor="w",
        ).grid(row=row, column=0, padx=14, pady=10, sticky="w")

        bitrate_var = ctk.StringVar(value=app.config.get("audio_bitrate", "192k"))
        ctk.CTkOptionMenu(
            card, values=["128k", "192k", "256k", "320k"],
            variable=bitrate_var,
            fg_color="#0a0a0a", button_color="#1a1a1a",
            button_hover_color="#333333",
            dropdown_fg_color="#0a0a0a",
            dropdown_hover_color="#111111",
            dropdown_text_color="#cccccc",
            text_color="#cccccc",
            font=ctk.CTkFont(family="Consolas", size=12),
            command=lambda v: app.config.update(audio_bitrate=v),
        ).grid(row=row, column=1, padx=14, pady=10, sticky="e")
        row += 1

        ctk.CTkFrame(card, height=1, fg_color="#1a1a1a").grid(row=row, column=0, columnspan=2, sticky="ew")
        row += 1

        ctk.CTkLabel(
            card, text=f"  {_('language')}",
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color="#cccccc", anchor="w",
        ).grid(row=row, column=0, padx=14, pady=10, sticky="w")

        lang_var = ctk.StringVar(value=get_lang())
        def _on_lang(v):
            set_lang(v)
            app.config["language"] = v
        ctk.CTkOptionMenu(
            card, values=["en", "ru"],
            variable=lang_var,
            fg_color="#0a0a0a", button_color="#1a1a1a",
            button_hover_color="#333333",
            dropdown_fg_color="#0a0a0a",
            dropdown_hover_color="#111111",
            dropdown_text_color="#cccccc",
            text_color="#cccccc",
            font=ctk.CTkFont(family="Consolas", size=12),
            width=60,
            command=_on_lang,
        ).grid(row=row, column=1, padx=14, pady=10, sticky="e")

        row += 1
        ctk.CTkFrame(card, height=1, fg_color="#1a1a1a").grid(row=row, column=0, columnspan=2, sticky="ew")
        row += 1

        ctk.CTkButton(
            card, text="[ CLEAR HISTORY ]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#0a0a0a", hover_color="#331111",
            text_color="#663333", height=32,
            corner_radius=0,
            command=lambda: self._clear_history(),
        ).grid(row=row, column=0, columnspan=2, padx=14, pady=10)

        ctk.CTkLabel(
            c, text="  * Language changes apply on next launch",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#444444",
        ).grid(row=3, column=0, sticky="w", pady=(4, 0))

    def _clear_history(self):
        import tkinter.messagebox as mb
        if mb.askyesno(_("app_title"), "Clear all conversion history?"):
            self.parent.history.clear()
            from config import save_json, HISTORY_FILE
            save_json(HISTORY_FILE, [])
            self.show_settings()
