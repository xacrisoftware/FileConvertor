import os
import threading
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import customtkinter as ctk
from config import load_icon, format_size
from lang import _
from converters.archive_conv import (
    create_archive, extract_archive, get_archive_members,
    ArchiveError,
)


class ArchiveToolView:
    def __init__(self, parent_frame, app):
        self.frame = parent_frame
        self.app = app
        self.c = parent_frame.container
        self._working = False
        self._mode = "create"
        self._files = []
        self._src_path = None
        self._build()

    def _build(self):
        c = self.c
        c.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            c, text=">_ ARCHIVES",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(16, 2))
        ctk.CTkLabel(
            c, text=_("archive_formats"),
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#555555", anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(0, 12))
        ctk.CTkFrame(c, height=1, fg_color="#1a1a1a").grid(row=2, column=0, sticky="ew", pady=(0, 16))

        card = ctk.CTkFrame(c, fg_color="#050505", corner_radius=0, border_width=1, border_color="#1a1a1a")
        card.grid(row=3, column=0, sticky="ew", padx=60)
        card.columnconfigure(0, weight=1)

        self._tab_create = ctk.CTkButton(
            card, text=f"[ {_('create')} ]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#141414", hover_color="#ffffff",
            text_color="#ffffff", height=32, width=120,
            corner_radius=0, command=lambda: self._set_mode("create"),
        )
        self._tab_create.grid(row=0, column=0, padx=(14, 4), pady=(8, 4), sticky="w")

        self._tab_extract = ctk.CTkButton(
            card, text=f"[ {_('extract')} ]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#0a0a0a", hover_color="#1a1a1a",
            text_color="#666666", height=32, width=120,
            corner_radius=0, command=lambda: self._set_mode("extract"),
        )
        self._tab_extract.grid(row=0, column=0, padx=(140, 14), pady=(8, 4), sticky="w")

        self._body = ctk.CTkFrame(card, fg_color="transparent")
        self._body.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        self._body.columnconfigure(0, weight=1)

        self._build_create_ui()

        ctk.CTkFrame(card, height=1, fg_color="#1a1a1a").grid(row=2, column=0, sticky="ew", padx=14)

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

        self._action_btn = ctk.CTkButton(
            c, text=f"[ {_('run')} ]",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            fg_color="#141414", hover_color="#ffffff",
            text_color="#ffffff", height=42, width=260,
            corner_radius=0, command=self._run,
        )
        self._action_btn.grid(row=5, column=0, pady=(12, 4))

        self._result_frame = ctk.CTkFrame(c, fg_color="transparent")
        self._result_frame.grid(row=6, column=0, sticky="ew", pady=(4, 0))
        self._result_frame.columnconfigure(0, weight=1)

    def _set_mode(self, mode):
        self._mode = mode
        self._files = []
        self._src_path = None
        for w in self._body.winfo_children():
            w.destroy()
        if mode == "create":
            self._build_create_ui()
            self._tab_create.configure(fg_color="#141414", text_color="#ffffff")
            self._tab_extract.configure(fg_color="#0a0a0a", text_color="#666666")
        else:
            self._build_extract_ui()
            self._tab_extract.configure(fg_color="#141414", text_color="#ffffff")
            self._tab_create.configure(fg_color="#0a0a0a", text_color="#666666")
        for w in self._result_frame.winfo_children():
            w.destroy()
        self._status.configure(text="")

    def _build_create_ui(self):
        body = self._body

        ctk.CTkLabel(
            body, text=f"  [ {_('files_to_archive')} ]",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#555555", anchor="w",
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=14, pady=(6, 0))

        self._file_list = ctk.CTkTextbox(
            body, height=50,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#000000", border_color="#1a1a1a",
            text_color="#cccccc",
        )
        self._file_list.grid(row=1, column=0, columnspan=2, padx=(14, 4), pady=(4, 4), sticky="ew")

        ctk.CTkButton(
            body, text=f"[ {_('add')} ]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#0a0a0a", hover_color="#1a1a1a",
            text_color="#ffffff", height=32, width=80,
            corner_radius=0, command=self._add_files,
        ).grid(row=1, column=2, padx=(4, 14), pady=(4, 4))

        fmt_frame = ctk.CTkFrame(body, fg_color="transparent")
        fmt_frame.grid(row=2, column=0, columnspan=3, pady=(4, 8))

        ctk.CTkLabel(
            fmt_frame, text=f"  {_('format')}",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#666666",
        ).pack(side="left", padx=(14, 0))

        self._fmt_menu = ctk.CTkOptionMenu(
            fmt_frame, values=["ZIP", "TAR", "TAR.GZ"],
            fg_color="#0a0a0a", button_color="#1a1a1a",
            button_hover_color="#333333",
            dropdown_fg_color="#0a0a0a",
            dropdown_hover_color="#111111",
            dropdown_text_color="#cccccc",
            text_color="#cccccc",
            font=ctk.CTkFont(family="Consolas", size=12),
            width=80,
        )
        self._fmt_menu.pack(side="left", padx=(6, 0))
        self._fmt_menu.set("ZIP")

    def _build_extract_ui(self):
        body = self._body

        ctk.CTkLabel(
            body, text=f"  [ {_('select_archive')} ]",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#555555", anchor="w",
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=14, pady=(6, 0))

        self._path_entry = ctk.CTkEntry(
            body,
            placeholder_text=_("select_file")+"...",
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#000000", border_color="#1a1a1a",
            text_color="#cccccc", height=36,
        )
        self._path_entry.grid(row=1, column=0, columnspan=2, padx=(14, 4), pady=(6, 6), sticky="ew")

        ctk.CTkButton(
            body, text="[ BROWSE ]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#0a0a0a", hover_color="#1a1a1a",
            text_color="#ffffff", height=36, width=90,
            corner_radius=0, command=self._browse_archive,
        ).grid(row=1, column=2, padx=(4, 14), pady=(6, 6))

        self._members_text = ctk.CTkLabel(
            body, text="",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#444444", anchor="w", justify="left",
        )
        self._members_text.grid(row=2, column=0, columnspan=3, sticky="w", padx=(14, 14), pady=(0, 8))

    def _add_files(self):
        files = fd.askopenfilenames(title="Выберите файлы для архивации")
        for fp in files:
            if fp not in self._files:
                self._files.append(fp)
                self._file_list.insert("end", f"{os.path.basename(fp)}\n")
        if files:
            total = sum(os.path.getsize(f) for f in self._files)
            self._status.configure(text=f"[ файлов: {len(self._files)} ({format_size(total)}) ]")

    def _browse_archive(self):
        fp = fd.askopenfilename(
            title="Выберите архив",
            filetypes=[("Archives", "*.zip *.tar *.tar.gz *.tgz")],
        )
        if fp:
            self._src_path = fp
            self._path_entry.delete(0, "end")
            self._path_entry.insert(0, fp)
            members = get_archive_members(fp)
            lines = "\n".join(f"  {m['name']} ({format_size(m['size'])})" for m in members[:15])
            if len(members) > 15:
                lines += f"\n  ... и ещё {len(members) - 15}"
            self._members_text.configure(text=lines)
            size = os.path.getsize(fp)
            self._status.configure(text=f"[ {os.path.basename(fp)} › {format_size(size)}, {len(members)} файлов ]")

    def _run(self):
        if self._working:
            return
        if self._mode == "create":
            self._create()
        else:
            self._extract()

    def _create(self):
        if not self._files:
            mb.showwarning(_("app_title"), f"{_('add')} {_('files_to_archive')}")
            return
        fmt = self._fmt_menu.get()
        ext_map = {"ZIP": ".zip", "TAR": ".tar", "TAR.GZ": ".tar.gz"}
        dst = fd.asksaveasfilename(
            defaultextension=ext_map[fmt],
            filetypes=[(fmt, f"*{ext_map[fmt]}")],
            initialfile=f"archive{ext_map[fmt]}",
            title="Сохранить архив как",
        )
        if not dst:
            return

        self._working = True
        self._action_btn.configure(state="disabled", text=f"[ {_('working')} ]")
        self._progress.set(0.5)
        files = list(self._files)

        def do():
            try:
                create_archive(dst, files, fmt)
                self.c.after(0, self._on_result, dst, None)
            except Exception as e:
                self.c.after(0, self._on_result, None, str(e))

        threading.Thread(target=do, daemon=True).start()

    def _extract(self):
        if not self._src_path:
            mb.showwarning(_("app_title"), _("select_archive"))
            return
        dst_dir = fd.askdirectory(
            initialdir=os.path.dirname(self._src_path),
            title="Выберите папку для распаковки",
        )
        if not dst_dir:
            return
        src = self._src_path

        self._working = True
        self._action_btn.configure(state="disabled", text=f"[ {_('working')} ]")
        self._progress.set(0.5)

        def do():
            try:
                extract_archive(src, dst_dir)
                self.c.after(0, self._on_result, dst_dir, None)
            except Exception as e:
                self.c.after(0, self._on_result, None, str(e))

        threading.Thread(target=do, daemon=True).start()

    def _on_result(self, path, error):
        self._working = False
        self._action_btn.configure(state="normal", text="[ RUN ]")
        if error:
            self._progress.set(0)
            self._status.configure(text=f"[ {_('error')}: {error[:50]} ]")
            mb.showerror(_("app_title"), error)
            return
        self._progress.set(1.0)

        if self._mode == "create":
            self._status.configure(text=f"[ {_('archive_created')}: {os.path.basename(path)} ]")
            self.app.add_history(
                {"src": f"{len(self._files)} files", "dst": os.path.basename(path)}, "archive"
            )
        else:
            self._status.configure(text=f"[ {_('extracted_to')}: {path} ]")
            self.app.add_history(
                {"src": os.path.basename(self._src_path), "dst": path}, "archive"
            )

        for w in self._result_frame.winfo_children():
            w.destroy()
        card = ctk.CTkFrame(self._result_frame, fg_color="#050505", corner_radius=0,
                            border_width=1, border_color="#2a5a2a")
        card.grid(row=0, column=0, sticky="ew")
        card.columnconfigure(1, weight=1)
        ic = load_icon("check", (14, 14))
        ctk.CTkLabel(card, text="", image=ic).grid(row=0, column=0, padx=(12, 4), pady=10)
        lbl = f"  ✓ {os.path.basename(path)}" if self._mode == "create" else f"  ✓ ok"
        ctk.CTkLabel(
            card, text=lbl,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).grid(row=0, column=1, sticky="w")
