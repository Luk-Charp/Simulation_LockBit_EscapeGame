"""Bureau principal simulé de la cellule d'enquête."""

import tkinter as tk
from tkinter import messagebox

from interface.mail import MailWindow


# Palette commune de l'interface.
COLORS = {
    "background": "#101827",
    "background_light": "#18263a",
    "panel": "#1d2d43",
    "panel_hover": "#2a405d",
    "text": "#edf3fb",
    "muted": "#a7b6ca",
    "blue": "#55a6f7",
    "green": "#55d6a3",
    "border": "#30445e",
    "taskbar": "#0b1220",
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
        """Barre supérieure rappelant l'environnement d'une cellule cyber."""
        top_bar = tk.Frame(
            self.root,
            bg=COLORS["taskbar"],
            height=48,
            highlightthickness=0,
        )
        top_bar.pack(side="top", fill="x")
        top_bar.pack_propagate(False)

        tk.Label(
            top_bar,
            text="◈  FBI  /  CYBER DIVISION",
            bg=COLORS["taskbar"],
            fg=COLORS["text"],
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left", padx=20)

        tk.Label(
            top_bar,
            text="POSTE D'INVESTIGATION  •  OPÉRATION LOCKDOWN",
            bg=COLORS["taskbar"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).pack(side="right", padx=20)

    def _build_workspace(self) -> None:
        """Zone centrale du bureau et raccourcis des applications."""
        workspace = tk.Frame(self.root, bg=COLORS["background"])
        workspace.pack(fill="both", expand=True)

        content = tk.Frame(workspace, bg=COLORS["background"])
        content.place(relx=0.075, rely=0.105, relwidth=0.85, relheight=0.79)

        tk.Label(
            content,
            text="CELLULE D'INVESTIGATION NUMÉRIQUE",
            bg=COLORS["background"],
            fg=COLORS["blue"],
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Bienvenue, agent.",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=("Segoe UI", 30, "bold"),
        ).pack(anchor="w", pady=(12, 5))

        tk.Label(
            content,
            text=(
                "Une entreprise française a signalé une attaque informatique.\n"
                "Ouvrez les outils de votre poste pour commencer l'enquête."
            ),
            bg=COLORS["background"],
            fg=COLORS["muted"],
            justify="left",
            font=("Segoe UI", 12),
        ).pack(anchor="w", pady=(0, 30))

        apps_frame = tk.Frame(content, bg=COLORS["background"])
        apps_frame.pack(anchor="w")

        applications = [
            ("✉", "Messagerie", "Consulter les communications", "mail"),
            ("▤", "Dossier d'enquête", "Retrouver les indices", "case"),
            ("⌘", "Terminal", "Outils informatiques", "terminal"),
            ("◎", "OSINT", "Recherche en sources ouvertes", "osint"),
            ("🌐", "Carte", "Visualiser les pistes", "map"),
        ]

        for symbol, title, description, app_id in applications:
            self._create_app_card(
                apps_frame,
                symbol,
                title,
                description,
                app_id,
            )

        info_panel = tk.Frame(
            content,
            bg=COLORS["background_light"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=16,
            pady=13,
        )
        info_panel.pack(fill="x", anchor="w", pady=(34, 0))

        tk.Label(
            info_panel,
            text="BRIEFING DE MISSION",
            bg=COLORS["background_light"],
            fg=COLORS["blue"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        tk.Label(
            info_panel,
            text=(
                "Votre objectif : comprendre l'attaque, analyser les éléments disponibles "
                "et transmettre des conclusions étayées aux autorités compétentes."
            ),
            bg=COLORS["background_light"],
            fg=COLORS["text"],
            justify="left",
            wraplength=850,
        ).pack(anchor="w", pady=(6, 0))

    def _create_app_card(
        self,
        parent: tk.Frame,
        symbol: str,
        title: str,
        description: str,
        app_id: str,
    ) -> None:
        """Crée un raccourci cliquable pour une application du bureau."""
        card = tk.Frame(
            parent,
            bg=COLORS["panel"],
            width=154,
            height=142,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        card.pack(side="left", padx=(0, 12), pady=2)
        card.pack_propagate(False)

        icon_button = tk.Button(
            card,
            text=symbol,
            command=lambda selected=app_id: self._open_application(selected),
            bg=COLORS["panel"],
            fg=COLORS["blue"],
            activebackground=COLORS["panel_hover"],
            activeforeground=COLORS["text"],
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            font=("Segoe UI Symbol", 27, "bold"),
        )
        icon_button.pack(fill="x", pady=(12, 0))

        title_label = tk.Label(
            card,
            text=title,
            bg=COLORS["panel"],
            fg=COLORS["text"],
            font=("Segoe UI", 9, "bold"),
        )
        title_label.pack(pady=(5, 1))

        description_label = tk.Label(
            card,
            text=description,
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=("Segoe UI", 7),
            wraplength=135,
        )
        description_label.pack()

        # Le titre et la description déclenchent également l'application.
        for widget in (card, title_label, description_label):
            widget.bind(
                "<Button-1>",
                lambda _event, selected=app_id: self._open_application(selected),
            )
            widget.configure(cursor="hand2")

    def _open_application(self, app_id: str) -> None:
        """Ouvre l'outil sélectionné ou indique qu'il sera développé ensuite."""
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
        """Barre inférieure avec l'état de la simulation."""
        taskbar = tk.Frame(
            self.root,
            bg=COLORS["taskbar"],
            height=38,
        )
        taskbar.pack(side="bottom", fill="x")
        taskbar.pack_propagate(False)

        tk.Label(
            taskbar,
            text="●  SYSTÈME OPÉRATIONNEL",
            bg=COLORS["taskbar"],
            fg=COLORS["green"],
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=16)

        tk.Label(
            taskbar,
            text="SIMULATION PÉDAGOGIQUE  •  DONNÉES FICTIVES",
            bg=COLORS["taskbar"],
            fg=COLORS["muted"],
            font=("Segoe UI", 8),
        ).pack(side="right", padx=16)
