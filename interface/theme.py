"""Palette partagée par les différentes fenêtres de l'application."""

COLORS = {
    "background": "#111827",
    "surface": "#172235",
    "card": "#1b2a40",
    "card_hover": "#223650",
    "text": "#edf2f7",
    "muted": "#9eacbf",
    "accent": "#55b7d9",
    "accent_dark": "#244c63",
    "green": "#65c69a",
    "border": "#2c4058",
    "taskbar": "#0c1421",
}



def center_window(window, preferred_width: int, preferred_height: int) -> None:
    """Dimensionne une fenêtre selon l'écran et la centre sur son parent."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    width = min(preferred_width, max(760, screen_width - 100))
    height = min(preferred_height, max(520, screen_height - 140))

    min_width = min(850, width)
    min_height = min(560, height)
    window.minsize(min_width, min_height)

    x = max(0, (screen_width - width) // 2)
    y = max(0, (screen_height - height) // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
