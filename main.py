"""Point d'entrée de l'application Opération Lockdown."""

import sys
from pathlib import Path
import tkinter as tk

from interface.desktop import Desktop
from interface.phone import VoicemailWindow
from interface.theme import COLORS


def show_splash(root: tk.Tk) -> None:
    """Affiche l'écran d'accueil pendant trois secondes."""
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.configure(bg=COLORS["taskbar"])
    width, height = 720, 560
    x = (splash.winfo_screenwidth() - width) // 2
    y = (splash.winfo_screenheight() - height) // 2
    splash.geometry(f"{width}x{height}+{x}+{y}")

    canvas = tk.Canvas(
        splash, width=width, height=height,
        bg=COLORS["taskbar"], highlightthickness=0
    )
    canvas.pack(fill="both", expand=True)

    # Le logo est stocké dans assets/images et chargé depuis le dossier du projet.
    logo_path = Path(__file__).resolve().parent / "assets" / "images" / "fbi_logo.png"
    try:
        logo_image = tk.PhotoImage(file=str(logo_path))
        # Le visuel est un bandeau large : réduction pour l'écran d'accueil.
        logo_image = logo_image.subsample(4, 4)
        canvas.create_image(width // 2, 190, image=logo_image, anchor="center")
        splash.logo_image = logo_image  # Conserver une référence Tkinter.
    except tk.TclError:
        canvas.create_text(
            width // 2, 190, text="FBI",
            fill="#ffffff", font=("Segoe UI", 72, "bold")
        )
        canvas.create_text(
            width // 2, 245,
            text="Ajoutez le fichier assets/images/fbi_logo.png",
            fill=COLORS["on_dark_muted"], font=("Segoe UI", 9)
        )

    canvas.create_text(
        width // 2, 350, text="CYBER DIVISION  •  DIGITAL INVESTIGATIONS",
        fill=COLORS["gold"], font=("Segoe UI", 10, "bold")
    )
    canvas.create_line(190, 382, 530, 382, fill=COLORS["gold"], width=2)
    canvas.create_text(
        width // 2, 420, text="OPÉRATION LOCKDOWN",
        fill="#ffffff", font=("Segoe UI", 13, "bold")
    )
    canvas.create_text(
        width // 2, 475, text="SIMULATION PÉDAGOGIQUE",
        fill=COLORS["on_dark_muted"], font=("Segoe UI", 8)
    )

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
