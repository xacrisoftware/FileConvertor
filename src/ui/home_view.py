import os
import customtkinter as ctk
from config import load_icon
from lang import _
from config import IMAGE_EXTENSIONS, AUDIO_EXTENSIONS, DOCUMENT_EXTENSIONS, ARCHIVE_READ_EXTENSIONS, DATA_EXTENSIONS, VIDEO_EXTENSIONS

_FILE_HANDLERS = {}
for _ext_map, _handler in [
    (IMAGE_EXTENSIONS, "show_image_convert"),
    (AUDIO_EXTENSIONS, "show_audio_convert"),
    (DOCUMENT_EXTENSIONS, "show_document_convert"),
    (ARCHIVE_READ_EXTENSIONS, "show_archive_tool"),
    (DATA_EXTENSIONS, "show_data_convert"),
    (VIDEO_EXTENSIONS, "show_video_convert"),
]:
    for _ext in _ext_map:
        _FILE_HANDLERS[_ext] = _handler


class HomeView:
    def __init__(self, parent_frame, app):
        self.frame = parent_frame
        self.app = app
        self.c = parent_frame.container
        self._build()

    def _build(self):
        c = self.c
        c.columnconfigure(0, weight=1)

        ctk.CTkLabel(c, text="", height=40).grid(row=0, column=0)

        icon = load_icon("convert", (28, 28))
        ctk.CTkLabel(
            c, text=f"  {_('app_title')}", image=icon,
            font=ctk.CTkFont(family="Consolas", size=22, weight="bold"),
            text_color="#ffffff", compound="left",
        ).grid(row=1, column=0)
        ctk.CTkLabel(
            c, text=_("convert_anything"),
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#555555",
        ).grid(row=2, column=0, pady=(0, 28))

        sf = ctk.CTkFrame(c, fg_color="transparent")
        sf.grid(row=3, column=0, padx=80, sticky="ew")
        sf.columnconfigure(0, weight=1)

        self._drop_zone = self._make_dropzone(sf)
        self._drop_zone.grid(row=0, column=0, sticky="ew")

        qf = ctk.CTkFrame(c, fg_color="transparent")
        qf.grid(row=4, column=0, pady=(20, 0))

        actions = [
            ("image", _("images"), self.app.show_image_convert),
            ("file", _("documents"), self.app.show_document_convert),
            ("video", _("video"), self.app.show_video_convert),
            ("music", _("audio"), self.app.show_audio_convert),
            ("folder", _("archives"), self.app.show_archive_tool),
            ("database", _("data"), self.app.show_data_convert),
        ]
        for icon_name, text, cmd in actions:
            ic = load_icon(icon_name, (14, 14))
            ctk.CTkButton(
                qf, text=f"  {text}", image=ic,
                font=ctk.CTkFont(family="Consolas", size=12),
                fg_color="#0a0a0a", hover_color="#141414",
                text_color="#999999", corner_radius=0, height=34,
                command=cmd, compound="left",
            ).pack(side="left", padx=3)

    def _make_dropzone(self, parent):
        dz = ctk.CTkFrame(parent, fg_color="#0a0a0a", corner_radius=0,
                          border_width=2, border_color="#1a1a1a",
                          cursor="hand2", height=160)
        dz.pack_propagate(False)
        dz.columnconfigure(0, weight=1)
        dz.rowconfigure(0, weight=1)

        inner = ctk.CTkFrame(dz, fg_color="transparent")
        inner.grid(row=0, column=0)

        ic = load_icon("upload", (32, 32))
        ctk.CTkLabel(inner, text="", image=ic).pack(pady=(0, 4))

        self._dz_text = ctk.CTkLabel(
            inner,
            text=_("drop_file"),
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color="#555555", justify="center",
        )
        self._dz_text.pack()

        self._dz_file = ctk.CTkLabel(
            inner, text="",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#888888",
        )

        def on_click(e=None):
            import tkinter.filedialog as fd
            fp = fd.askopenfilename(title=_("select_file"))
            if fp:
                self._handle_file(fp)

        dz.bind("<Button-1>", on_click)
        inner.bind("<Button-1>", on_click)
        dz.bind("<Enter>", lambda e: dz.configure(border_color="#333333"))
        dz.bind("<Leave>", lambda e: dz.configure(border_color="#1a1a1a"))
        return dz

    def _handle_file(self, fp):
        self._dz_text.pack_forget()
        self._dz_file.configure(text=f"  {os.path.basename(fp)}")
        self._dz_file.pack()
        self._drop_zone.configure(border_color="#2a5a2a")

        ext = os.path.splitext(fp)[1].lower()
        if fp.lower().endswith(".tar.gz"):
            ext = ".tar.gz"
        handler = _FILE_HANDLERS.get(ext)
        if handler:
            self.c.after(200, getattr(self.app, handler))
