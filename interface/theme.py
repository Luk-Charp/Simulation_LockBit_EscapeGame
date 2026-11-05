"""Palette visuelle partagée par les fenêtres de l'application."""

COLORS = {
    "background": "#0b1220",
    "surface": "#111c2e",
    "card": "#16243a",
    "card_hover": "#1c304b",
    "text": "#f3f7fc",
    "muted": "#91a2b8",
    "accent": "#63c9e8",
    "accent_dark": "#173b50",
    "green": "#69d6a4",
    "border": "#263a54",
    "taskbar": "#080f1b",
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
