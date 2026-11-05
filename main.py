"""Point d'entrée de la simulation de bureau Debian."""

import sys
import tkinter as tk

from interface.desktop import Desktop


def main() -> None:
    """Démarre directement sur le bureau Debian simulé."""
    root = tk.Tk()
    root.title("Debian GNU/Linux")
    root.minsize(1024, 680)

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
    root.mainloop()


if __name__ == "__main__":
    main()
