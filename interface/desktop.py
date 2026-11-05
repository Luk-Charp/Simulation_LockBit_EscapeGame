"""Bureau principal sobre de la cellule d'investigation."""

import tkinter as tk
from tkinter import messagebox

from interface.mail import MailWindow


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


class Desktop:
    """Construit le bureau sur lequel les élèves lanceront les outils."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.configure(bg=COLORS["background"])
        self.root.option_add("*Font", ("Segoe UI", 10))
        self._build_top_bar()
        self._build_workspace()
        self._build_taskbar()

    def _build_top_bar(self) -> None:
        top = tk.Frame(self.root, bg=COLORS["taskbar"], height=58)
        top.pack(side="top", fill="x")
        top.pack_propagate(False)

        brand = tk.Frame(top, bg=COLORS["taskbar"])
        brand.pack(side="left", padx=30)
        tk.Label(
            brand, text="FBI", bg=COLORS["taskbar"], fg=COLORS["text"],
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left")
        tk.Frame(brand, bg=COLORS["accent"], width=2, height=26).pack(
            side="left", padx=13, pady=15
        )
        tk.Label(
            brand, text="CYBER DIVISION", bg=COLORS["taskbar"],
            fg=COLORS["muted"], font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        tk.Label(
            top, text="OPÉRATION LOCKDOWN",
            bg=COLORS["taskbar"], fg=COLORS["text"],
            font=("Segoe UI", 10, "bold"),
        ).pack(side="right", padx=30)

    def _build_workspace(self) -> None:
        workspace = tk.Frame(self.root, bg=COLORS["background"])
        workspace.pack(fill="both", expand=True)

        content = tk.Frame(workspace, bg=COLORS["background"])
        content.place(relx=0.07, rely=0.105, relwidth=0.86, relheight=0.80)

        tk.Label(
            content, text="CELLULE D'INVESTIGATION NUMÉRIQUE",
            bg=COLORS["background"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        tk.Label(
            content, text="Bienvenue, agent.",
            bg=COLORS["background"], fg=COLORS["text"],
            font=("Segoe UI", 29, "bold"),
        ).pack(anchor="w", pady=(12, 6))

        tk.Label(
            content,
            text=(
                "Une entreprise française a signalé une attaque informatique. "
                "Consultez les outils mis à votre disposition pour débuter l'enquête."
            ),
            bg=COLORS["background"], fg=COLORS["muted"],
            font=("Segoe UI", 11), wraplength=900, justify="left",
        ).pack(anchor="w", pady=(0, 28))

        section = tk.Frame(content, bg=COLORS["background"])
        section.pack(fill="x", anchor="w")
        tk.Label(
            section, text="OUTILS D'INVESTIGATION",
            bg=COLORS["background"], fg=COLORS["muted"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        apps = tk.Frame(section, bg=COLORS["background"])
        apps.pack(anchor="w")
        applications = [
            ("✉", "Messagerie", "Consulter les communications", "mail"),
            ("▤", "Dossier d'enquête", "Centraliser les indices", "case"),
            ("⌘", "Terminal", "Analyser les données", "terminal"),
            ("◎", "OSINT", "Rechercher en sources ouvertes", "osint"),
            ("⊕", "Carte", "Visualiser les pistes", "map"),
        ]
        for symbol, title, description, app_id in applications:
            self._create_app_card(apps, symbol, title, description, app_id)

        briefing = tk.Frame(
            content, bg=COLORS["surface"],
            highlightbackground=COLORS["border"], highlightthickness=1,
            padx=20, pady=17,
        )
        briefing.pack(fill="x", pady=(30, 0))

        tk.Label(
            briefing, text="BRIEFING DE MISSION",
            bg=COLORS["surface"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            briefing,
            text=(
                "Votre objectif : comprendre le déroulement de l'attaque, "
                "analyser les preuves disponibles et formuler des conclusions "
                "étayées pour les autorités compétentes."
            ),
            bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 10), justify="left", wraplength=1050,
        ).pack(anchor="w", pady=(7, 0))

        progress = tk.Frame(content, bg=COLORS["background"])
        progress.pack(fill="x", pady=(28, 0))
        tk.Label(
            progress, text="DÉROULEMENT DE L'ENQUÊTE",
            bg=COLORS["background"], fg=COLORS["muted"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        stages = tk.Frame(progress, bg=COLORS["background"])
        stages.pack(fill="x")
        for index, stage in enumerate(
            ("Incident", "Intrusion", "Infrastructure", "Attribution", "Rapport")
        ):
            item = tk.Frame(stages, bg=COLORS["background"])
            item.pack(side="left", expand=True, fill="x")
            color = COLORS["accent"] if index == 0 else COLORS["muted"]
            tk.Label(
                item, text=f"{index + 1:02d}  /  {stage.upper()}",
                bg=COLORS["background"], fg=color,
                font=("Segoe UI", 8, "bold" if index == 0 else "normal"),
            ).pack(anchor="w")

    def _create_app_card(
        self, parent: tk.Frame, symbol: str, title: str,
        description: str, app_id: str,
    ) -> None:
        card = tk.Frame(
            parent, bg=COLORS["card"], width=185, height=142,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        card.pack(side="left", padx=(0, 12), pady=2)
        card.pack_propagate(False)

        icon = tk.Label(
            card, text=symbol, bg=COLORS["card"], fg=COLORS["accent"],
            font=("Segoe UI Symbol", 25),
        )
        icon.pack(anchor="w", padx=16, pady=(14, 8))

        heading = tk.Label(
            card, text=title, bg=COLORS["card"], fg=COLORS["text"],
            font=("Segoe UI", 10, "bold"), anchor="w",
        )
        heading.pack(fill="x", padx=16)

        subtitle = tk.Label(
            card, text=description, bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 8), anchor="w", wraplength=150, justify="left",
        )
        subtitle.pack(fill="x", padx=16, pady=(5, 0))

        widgets = (card, icon, heading, subtitle)
        for widget in widgets:
            widget.configure(cursor="hand2")
            widget.bind(
                "<Button-1>",
                lambda _event, selected=app_id: self._open_application(selected),
            )
            widget.bind(
                "<Enter>",
                lambda _event, elements=widgets: self._set_card_color(elements, COLORS["card_hover"]),
            )
            widget.bind(
                "<Leave>",
                lambda _event, elements=widgets: self._set_card_color(elements, COLORS["card"]),
            )

    @staticmethod
    def _set_card_color(widgets: tuple, color: str) -> None:
        for widget in widgets:
            widget.configure(bg=color)

    def _open_application(self, app_id: str) -> None:
        app_names = {
            "mail": "Messagerie",
            "case": "Dossier d'enquête",
            "terminal": "Terminal",
            "osint": "OSINT",
            "map": "Carte",
        }
        app_name = app_names.get(app_id, "Application")
        if app_id == "mail":
            MailWindow(self.root)
            return

        messagebox.showinfo(
            app_name,
            f"L'application « {app_name} » sera développée dans une prochaine étape.",
            parent=self.root,
        )

    def _build_taskbar(self) -> None:
        taskbar = tk.Frame(self.root, bg=COLORS["taskbar"], height=36)
        taskbar.pack(side="bottom", fill="x")
        taskbar.pack_propagate(False)

        tk.Label(
            taskbar, text="●  SYSTÈME OPÉRATIONNEL",
            bg=COLORS["taskbar"], fg=COLORS["green"],
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=18)
        tk.Label(
            taskbar, text="SIMULATION PÉDAGOGIQUE  •  DONNÉES FICTIVES",
            bg=COLORS["taskbar"], fg=COLORS["muted"],
            font=("Segoe UI", 8),
        ).pack(side="right", padx=18)
