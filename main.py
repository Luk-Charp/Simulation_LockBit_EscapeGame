"""Point d'entrée de l'application Opération Lockdown."""

import sys
import tkinter as tk

from interface.desktop import Desktop
from interface.phone import VoicemailWindow


def main() -> None:
    """Crée le bureau puis affiche le message vocal de briefing."""
    root = tk.Tk()
    root.title("Opération Lockdown — FBI Cyber Division")
    root.minsize(980, 640)

    # Ouvre directement la fenêtre en grand selon le système d'exploitation.
    if sys.platform == "darwin":
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height - 80}+0+0")
    else:
        try:
            root.state("zoomed")
        except tk.TclError:
            root.geometry("1280x800")

    Desktop(root)

    # Le message vocal s'ouvre automatiquement au lancement.
    root.after(400, lambda: VoicemailWindow(root))

    root.mainloop()


if __name__ == "__main__":
    main()
