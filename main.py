"""Point d'entrée de l'application Opération Lockdown."""

import sys
import tkinter as tk

from interface.desktop import Desktop
from interface.phone import VoicemailWindow
from interface.theme import COLORS


def draw_fbi_emblem(canvas: tk.Canvas, center_x: int, center_y: int, size: int) -> None:
    """Dessine un emblème FBI stylisé pour l'identité de la simulation."""
    radius = size // 2
    canvas.create_oval(center_x-radius, center_y-radius, center_x+radius, center_y+radius,
                       fill="#ffffff", outline=COLORS["gold"], width=max(2, size // 45))
    inner = radius - max(7, size // 18)
    canvas.create_oval(center_x-inner, center_y-inner, center_x+inner, center_y+inner,
                       fill=COLORS["taskbar"], outline=COLORS["accent"], width=max(2, size // 55))
    sw, sh = size * 0.52, size * 0.58
    points = [center_x-sw/2, center_y-sh*0.38, center_x+sw/2, center_y-sh*0.38,
              center_x+sw/2, center_y+sh*0.12, center_x, center_y+sh/2,
              center_x-sw/2, center_y+sh*0.12]
    canvas.create_polygon(points, fill="#ffffff", outline=COLORS["gold"], width=max(2, size // 65))
    canvas.create_rectangle(center_x-sw*0.42, center_y-sh*0.31, center_x+sw*0.42,
                            center_y+sh*0.05, fill=COLORS["accent"], outline="")
    canvas.create_text(center_x, center_y-sh*0.12, text="FBI", fill="#ffffff",
                       font=("Georgia", max(12, int(size * 0.20)), "bold"))
    canvas.create_polygon(center_x-sw*0.42, center_y+sh*0.05, center_x+sw*0.42,
                          center_y+sh*0.05, center_x, center_y+sh*0.42,
                          fill="#b52b36", outline="")


def show_splash(root: tk.Tk) -> None:
    """Affiche l'écran d'accueil pendant trois secondes."""
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.configure(bg=COLORS["taskbar"])
    width, height = 720, 560
    x = (splash.winfo_screenwidth() - width) // 2
    y = (splash.winfo_screenheight() - height) // 2
    splash.geometry(f"{width}x{height}+{x}+{y}")
    canvas = tk.Canvas(splash, width=width, height=height, bg=COLORS["taskbar"], highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    draw_fbi_emblem(canvas, width // 2, 205, 220)
    canvas.create_text(width//2, 365, text="FEDERAL BUREAU OF INVESTIGATION",
                       fill="#ffffff", font=("Segoe UI", 17, "bold"))
    canvas.create_text(width//2, 400, text="CYBER DIVISION  •  DIGITAL INVESTIGATIONS",
                       fill=COLORS["gold"], font=("Segoe UI", 10, "bold"))
    canvas.create_line(190, 432, 530, 432, fill=COLORS["gold"], width=2)
    canvas.create_text(width//2, 465, text="OPÉRATION LOCKDOWN",
                       fill="#ffffff", font=("Segoe UI", 13, "bold"))
    canvas.create_text(width//2, 520, text="SIMULATION PÉDAGOGIQUE",
                       fill=COLORS["on_dark_muted"], font=("Segoe UI", 8))

    def finish_loading() -> None:
        splash.destroy()
        root.deiconify()
        root.after(500, lambda: VoicemailWindow(root))

    root.after(3000, finish_loading)


def main() -> None:
    """Crée le bureau puis affiche le message vocal de briefing."""
    root = tk.Tk()
    root.title("Opération Lockdown — FBI Cyber Division")
    root.minsize(980, 640)
    if sys.platform == "darwin":
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height - 80}+0+0")
    else:
        try:
            root.state("zoomed")
        except tk.TclError:
            root.geometry("1280x800")
    root.withdraw()
    Desktop(root)
    show_splash(root)
    root.mainloop()


if __name__ == "__main__":
    main()
