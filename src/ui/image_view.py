import os
import threading
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import customtkinter as ctk
from config import load_icon, format_size
from lang import _
from converters.image_conv import (
    convert_image, get_format_from_ext, OUTPUT_FORMATS, SAVE_FORMAT_EXT,
)

EXT_MAP = SAVE_FORMAT_EXT


class ImageConvertView:
    def __init__(self, parent_frame, app):
        self.frame = parent_frame
        self.app = app
        self.c = parent_frame.container
        self._converting = False
        self._src_path = None
        self._stop_event = threading.Event()
        self._build()

    def _build(self):
        c = self.c
        c.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            c, text=">_ IMAGES",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(16, 2))
        ctk.CTkLabel(
            c, text=_("image_formats"),
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#555555", anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(0, 12))
        ctk.CTkFrame(c, height=1, fg_color="#1a1a1a").grid(row=2, column=0, sticky="ew", pady=(0, 16))

        card = ctk.CTkFrame(c, fg_color="#050505", corner_radius=0, border_width=1, border_color="#1a1a1a")
        card.grid(row=3, column=0, sticky="ew", padx=60)
        card.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text=f"  [ {_('file')} ]",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#555555", anchor="w",
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=14, pady=(8, 0))

        self._path_entry = ctk.CTkEntry(
            card,
            placeholder_text=_("select_file")+"...",
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#000000", border_color="#1a1a1a",
            text_color="#cccccc", height=36,
        )
        self._path_entry.grid(row=1, column=0, columnspan=2, padx=(14, 4), pady=(6, 6), sticky="ew")

        ctk.CTkButton(
            card, text=f"[ {_('browse')} ]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#0a0a0a", hover_color="#1a1a1a",
            text_color="#ffffff", height=36, width=90,
            corner_radius=0, command=self._browse,
        ).grid(row=1, column=2, padx=(4, 14), pady=(6, 6))

        sep1 = ctk.CTkFrame(card, height=1, fg_color="#1a1a1a")
        sep1.grid(row=2, column=0, columnspan=3, sticky="ew", padx=14)

        fmt_frame = ctk.CTkFrame(card, fg_color="transparent")
        fmt_frame.grid(row=3, column=0, columnspan=3, pady=(10, 6))

        self._in_label = ctk.CTkLabel(
            fmt_frame, text="PNG",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color="#cccccc", width=60,
        )
        self._in_label.pack(side="left", padx=(0, 8))

        arrow = ctk.CTkLabel(
            fmt_frame, text="→",
            font=ctk.CTkFont(family="Consolas", size=18),
            text_color="#555555",
        )
        arrow.pack(side="left", padx=4)

        self._out_menu = ctk.CTkOptionMenu(
            fmt_frame, values=OUTPUT_FORMATS,
            fg_color="#0a0a0a", button_color="#1a1a1a",
            button_hover_color="#333333",
            dropdown_fg_color="#0a0a0a",
            dropdown_hover_color="#111111",
            dropdown_text_color="#cccccc",
            text_color="#cccccc",
            font=ctk.CTkFont(family="Consolas", size=12),
            width=90, command=lambda f: self._update_out_name(),
        )
        self._out_menu.pack(side="left", padx=(8, 0))
        self._out_menu.set("PNG")

        swap_btn = ctk.CTkButton(
            fmt_frame, text="⇄",
            font=ctk.CTkFont(family="Consolas", size=14),
            fg_color="transparent", hover_color="#1a1a1a",
            text_color="#555555", width=30, height=30,
            corner_radius=0, command=self._swap_format,
        )
        swap_btn.pack(side="left", padx=8)

        sep2 = ctk.CTkFrame(card, height=1, fg_color="#1a1a1a")
        sep2.grid(row=4, column=0, columnspan=3, sticky="ew", padx=14)

        ctk.CTkLabel(
            card, text=f"  {_('save_as')}",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#555555", anchor="w",
        ).grid(row=5, column=0, columnspan=3, sticky="w", padx=14, pady=(8, 0))

        self._out_entry = ctk.CTkEntry(
            card,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#000000", border_color="#1a1a1a",
            text_color="#cccccc", height=36,
        )
        self._out_entry.grid(row=6, column=0, columnspan=2, padx=(14, 4), pady=(6, 10), sticky="ew")

        opt_frame = ctk.CTkFrame(card, fg_color="transparent")
        opt_frame.grid(row=7, column=0, columnspan=3, pady=(0, 10), padx=14, sticky="ew")
        opt_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(
            opt_frame, text=f"  {_('quality')}",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#666666",
        ).grid(row=0, column=0, sticky="w")

        self._quality_var = ctk.IntVar(value=self.app.config.get("image_quality", 90))
        self._quality_slider = ctk.CTkSlider(
            opt_frame, from_=10, to=100, variable=self._quality_var,
            fg_color="#1a1a1a", progress_color="#ffffff", height=4,
        )
        self._quality_slider.grid(row=0, column=1, padx=(8, 8), sticky="ew")

        self._qlabel = ctk.CTkLabel(
            opt_frame, text="90",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#888888", width=24,
        )
        self._qlabel.grid(row=0, column=2, sticky="w")
        self._quality_slider.configure(command=lambda v: self._qlabel.configure(text=str(int(v))))

        status_frame = ctk.CTkFrame(c, fg_color="transparent")
        status_frame.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        status_frame.columnconfigure(1, weight=1)

        self._status = ctk.CTkLabel(
            status_frame, text="",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#555555",
        )
        self._status.grid(row=0, column=0, sticky="w")

        self._progress = ctk.CTkProgressBar(
            status_frame, height=3,
            fg_color="#0a0a0a", progress_color="#ffffff",
            corner_radius=0,
        )
        self._progress.grid(row=0, column=1, padx=(12, 0), pady=4, sticky="ew")
        self._progress.set(0)

        self._convert_btn = ctk.CTkButton(
            c, text=f"[ {_('convert')} ]",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            fg_color="#141414", hover_color="#ffffff",
            text_color="#ffffff", height=42, width=260,
            corner_radius=0, command=self._convert,
        )
        self._convert_btn.grid(row=5, column=0, pady=(12, 4))

        self._cancel_btn = ctk.CTkButton(
            c, text="[ CANCEL ]",
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#0a0a0a", hover_color="#331111",
            text_color="#553333", height=28, width=100,
            corner_radius=0, command=self._cancel,
        )
        self._cancel_btn.grid(row=5, column=0, pady=(48, 4))
        self._cancel_btn.grid_remove()

        self._result_frame = ctk.CTkFrame(c, fg_color="transparent")
        self._result_frame.grid(row=6, column=0, sticky="ew", pady=(4, 0))
        self._result_frame.columnconfigure(0, weight=1)

    def _gen_out_name(self):
        if not self._src_path:
            return ""
        base, _ = os.path.splitext(self._src_path)
        fmt = self._out_menu.get()
        ext = EXT_MAP.get(fmt) or EXT_MAP.get("PNG")
        return os.path.basename(base) + "_converted" + ext

    def _update_out_name(self):
        self._out_entry.delete(0, "end")
        self._out_entry.insert(0, self._gen_out_name())

    def _browse(self):
        fp = fd.askopenfilename(title=_("select_file"))
        if fp:
            self._load_file(fp)

    def _load_file(self, fp):
        self._src_path = fp
        self._path_entry.delete(0, "end")
        self._path_entry.insert(0, fp)
        fmt = get_format_from_ext(fp)
        if fmt and fmt in EXT_MAP:
            self._in_label.configure(text=fmt)
            for f in OUTPUT_FORMATS:
                if f != fmt:
                    self._out_menu.set(f)
                    break
        self._update_out_name()
        self._status.configure(text=f"[ {os.path.basename(fp)} › {format_size(os.path.getsize(fp))} ]")

    def _swap_format(self):
        cur = self._out_menu.get()
        src = self._in_label.cget("text")
        self._out_menu.set(src)
        self._in_label.configure(text=cur)
        self._update_out_name()

    def _cancel(self):
        if self._converting:
            self._stop_event.set()
            self._converting = False
            self._convert_btn.configure(state="normal", text=f"[ {_('convert')} ]")
            self._cancel_btn.grid_remove()
            self._progress.set(0)
            self._status.configure(text="[ cancelled ]")

    def _convert(self):
        if self._converting:
            return
        src = self._src_path
        if not src:
            mb.showwarning(_("app_title"), _("select_file"))
            return
        out_name = self._out_entry.get().strip()
        if not out_name:
            mb.showwarning(_("app_title"), _("enter_name"))
            return
        out_fmt = self._out_menu.get()
        quality = self._quality_var.get()
        dst = os.path.join(os.path.dirname(src), out_name)

        if os.path.exists(dst):
            if not mb.askyesno(_("app_title"), f"Overwrite {os.path.basename(dst)}?"):
                return

        self._stop_event.clear()
        self._converting = True
        self._convert_btn.configure(state="disabled", text=f"[ {_('converting')} ]")
        self._cancel_btn.grid()
        self._progress.set(0.3)

        def do():
            try:
                if not self._stop_event.is_set():
                    convert_image(src, dst, out_fmt, quality=quality)
                if not self._stop_event.is_set():
                    self.c.after(0, self._on_result, dst, None)
                else:
                    self.c.after(0, self._cancel)
            except Exception as e:
                self.c.after(0, self._on_result, None, str(e))

        threading.Thread(target=do, daemon=True).start()

    def _on_result(self, dst, error):
        self._converting = False
        self._convert_btn.configure(state="normal", text=f"[ {_('convert')} ]")
        self._cancel_btn.grid_remove()
        if error:
            self._progress.set(0)
            self._status.configure(text=f"[ {_('error')}: {error[:50]} ]")
            mb.showerror(_("app_title"), error)
            return
        self._progress.set(1.0)
        self._status.configure(text=f"[ {_('done')}: {os.path.basename(dst)} ]")
        self.app.add_history(
            {"src": os.path.basename(self._src_path), "dst": os.path.basename(dst)}, "image"
        )
        for w in self._result_frame.winfo_children():
            w.destroy()

        card = ctk.CTkFrame(self._result_frame, fg_color="#050505", corner_radius=0,
                            border_width=1, border_color="#2a5a2a")
        card.grid(row=0, column=0, sticky="ew")
        card.columnconfigure(1, weight=1)

        ic = load_icon("check", (14, 14))
        ctk.CTkLabel(card, text="", image=ic).grid(row=0, column=0, padx=(12, 4), pady=10)

        ctk.CTkLabel(
            card, text=f"  ✓ {os.path.basename(dst)}",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=1, sticky="w")

        if os.path.exists(dst):
            ctk.CTkLabel(
                card, text=format_size(os.path.getsize(dst)),
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color="#555555", anchor="w",
            ).grid(row=0, column=2, padx=(4, 4))

        ctk.CTkButton(
            card, text="[ OPEN ]",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            fg_color="transparent", hover_color="#1a1a1a",
            text_color="#888888", corner_radius=0, width=60,
            command=lambda p=dst: os.startfile(p),
        ).grid(row=0, column=3, padx=(4, 12))
