"""Palette institutionnelle inspirée de l'identité visuelle des agences fédérales américaines."""

COLORS = {
    "background": "#f2f5f9",
    "surface": "#ffffff",
    "card": "#e8eef5",
    "card_hover": "#dce6f0",
    "text": "#142b45",
    "muted": "#62758b",
    "accent": "#1c5688",
    "accent_dark": "#123b63",
    "green": "#287a57",
    "gold": "#c5a45b",
    "border": "#cbd5e1",
    "taskbar": "#102b49",
    "on_dark": "#ffffff",
    "on_dark_muted": "#c4d1df",
    "button_text": "#ffffff",
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
