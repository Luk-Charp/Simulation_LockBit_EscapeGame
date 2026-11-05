"""Point d'entrée de l'application Opération Lockdown."""

import tkinter as tk

from interface.desktop import Desktop


def main() -> None:
    """Crée la fenêtre principale et lance le bureau de l'enquête."""
    root = tk.Tk()
    root.title("Opération Lockdown — FBI Cyber Division")
    root.geometry("1280x800")
    root.minsize(980, 640)

    Desktop(root)

    root.mainloop()


if __name__ == "__main__":
    main()
