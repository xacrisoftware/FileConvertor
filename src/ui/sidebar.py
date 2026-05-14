import customtkinter as ctk
from config import load_icon
from lang import _


class SidebarFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=220, fg_color="#050505", corner_radius=0)
        self.pack_propagate(False)
        self._app = parent

        ctk.CTkLabel(
            self, text=f"  [ {_('app_title')} ]",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color="#ffffff", anchor="w",
        ).pack(pady=(20, 4), padx=14, fill="x")

        ctk.CTkFrame(self, height=1, fg_color="#1a1a1a").pack(fill="x", padx=14, pady=(0, 8))

        self._all_btns = {}

        self._add_btn("home", f"  {_('home')}", parent.show_home, "home")

        ctk.CTkFrame(self, height=1, fg_color="#1a1a1a").pack(fill="x", padx=14, pady=(6, 6))
        ctk.CTkLabel(
            self, text=f"  {_('conversion')}",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color="#555555",
        ).pack(fill="x", padx=14, pady=(0, 4))

        for key, icon_name, label_key, cmd in [
            ("image", "image", "images", parent.show_image_convert),
            ("file", "file", "documents", parent.show_document_convert),
            ("video", "video", "video", parent.show_video_convert),
            ("music", "music", "audio", parent.show_audio_convert),
            ("folder", "folder", "archives", parent.show_archive_tool),
            ("database", "database", "data", parent.show_data_convert),
        ]:
            self._add_btn(key, f"  {_(label_key)}", cmd, icon_name)

        ctk.CTkFrame(self, height=1, fg_color="#1a1a1a").pack(fill="x", padx=14, pady=(6, 6))

        self._add_btn("history", f"  {_('history')}", parent.show_history, "history")
        self._add_btn("settings", f"  {_('settings')}", parent.show_settings, "cog")

        ctk.CTkLabel(
            self, text="  v1.0 // 58 format options",
            font=ctk.CTkFont(family="Consolas", size=9),
            text_color="#333333", anchor="w",
        ).pack(side="bottom", pady=10, padx=14, fill="x")

    def _add_btn(self, key, text, cmd, icon_name=None):
        icon = load_icon(icon_name or key)
        btn = ctk.CTkButton(
            self, text=text, image=icon,
            font=ctk.CTkFont(family="Consolas", size=12),
            anchor="w", fg_color="transparent",
            text_color="#cccccc", hover_color="#111111",
            corner_radius=0, height=30, command=lambda k=key: (self._set_active(k), cmd()),
            compound="left",
        )
        btn.pack(fill="x", padx=10, pady=1)
        self._all_btns[key] = btn
        return btn

    def _set_active(self, key):
        for k, btn in self._all_btns.items():
            btn.configure(fg_color="#0f0f0f" if k == key else "transparent",
                         text_color="#ffffff" if k == key else "#cccccc")
