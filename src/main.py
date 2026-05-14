import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

from app import ConvertorApp

if __name__ == "__main__":
    app = ConvertorApp()
    app.mainloop()
