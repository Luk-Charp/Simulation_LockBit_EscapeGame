"""Palette et réglages partagés de l'interface."""

COLORS = {
    "background": "#eef2f7",
    "surface": "#ffffff",
    "card": "#e4ebf3",
    "card_hover": "#d7e3ef",
    "text": "#172b40",
    "muted": "#5e7185",
    "accent": "#245f91",
    "accent_dark": "#173f64",
    "green": "#267653",
    "gold": "#e0b858",
    "border": "#cbd5df",
    "taskbar": "#172b42",
    "on_dark": "#ffffff",
    "on_dark_muted": "#c4d1df",
    "button_text": "#ffffff",
}


def center_window(window, preferred_width: int, preferred_height: int) -> None:
    """Dimensionne et centre une fenêtre sans dépasser l'écran disponible."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width = min(preferred_width, max(320, screen_width - 32))
    height = min(preferred_height, max(320, screen_height - 72))
    window.minsize(min(560, width), min(420, height))
    x = max(0, (screen_width - width) // 2)
    y = max(0, (screen_height - height) // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
