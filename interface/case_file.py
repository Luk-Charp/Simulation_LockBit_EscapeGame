"""Dossier centralisant les informations et preuves de l'affaire."""

import tkinter as tk
from tkinter import ttk

from interface.theme import COLORS, center_window


class CaseFileWindow:
    """Fenêtre du dossier d'enquête consultable par les élèves."""

    def __init__(self, parent: tk.Misc) -> None:
        self.window = tk.Toplevel(parent)
        self.window.title("Dossier d'enquête — Opération Lockdown")
        self.window.transient(parent)
        self.window.configure(bg=COLORS["background"])
        center_window(self.window, 1100, 800)
        self._configure_style()
        self._build_interface()

    def _configure_style(self) -> None:
        style = ttk.Style(self.window)
        style.theme_use("clam")
        style.configure(
            "Case.TNotebook",
            background=COLORS["background"],
            borderwidth=0,
        )
        style.configure(
            "Case.TNotebook.Tab",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            padding=(16, 10),
            borderwidth=0,
            focuscolor=COLORS["surface"],
            lightcolor=COLORS["surface"],
            darkcolor=COLORS["surface"],
        )
        # Retire l'élément de focus natif qui laisse un cadre clair
        # autour de l'onglet sélectionné sur macOS.
        style.layout(
            "Case.TNotebook.Tab",
            [("Notebook.tab", {
                "sticky": "nswe",
                "children": [("Notebook.padding", {
                    "side": "top",
                    "sticky": "nswe",
                    "children": [("Notebook.label", {"side": "top", "sticky": ""})],
                })],
            })],
        )
        style.map(
            "Case.TNotebook.Tab",
            background=[("selected", COLORS["card"])],
            foreground=[("selected", COLORS["accent"])],
        )

    def _build_interface(self) -> None:
        header = tk.Frame(self.window, bg=COLORS["taskbar"], height=58)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text="DOSSIER D'ENQUÊTE",
            bg=COLORS["taskbar"], fg=COLORS["text"],
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left", padx=22)
        tk.Label(
            header, text="AFFAIRE #LK-2026-1104",
            bg=COLORS["taskbar"], fg=COLORS["muted"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side="right", padx=22)

        wrapper = tk.Frame(self.window, bg=COLORS["background"])
        wrapper.pack(fill="both", expand=True, padx=22, pady=20)

        summary = tk.Frame(
            wrapper, bg=COLORS["surface"],
            highlightbackground=COLORS["border"], highlightthickness=1,
            padx=18, pady=14,
        )
        summary.pack(fill="x", pady=(0, 16))
        tk.Label(
            summary, text="HEXATECH INDUSTRIES  /  FRANCE",
            bg=COLORS["surface"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            summary, text="Suspicion d'attaque par rançongiciel",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 17, "bold"),
        ).pack(anchor="w", pady=(5, 3))
        tk.Label(
            summary,
            text="Statut : enquête initiale  •  Signalement reçu le 4 novembre 2026",
            bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        notebook = ttk.Notebook(wrapper, style="Case.TNotebook", takefocus=False)
        notebook.pack(fill="both", expand=True)

        overview = tk.Frame(notebook, bg=COLORS["card"])
        timeline = tk.Frame(notebook, bg=COLORS["card"])
        evidence = tk.Frame(notebook, bg=COLORS["card"])
        notebook.add(overview, text="Vue d'ensemble")
        notebook.add(timeline, text="Chronologie")
        notebook.add(evidence, text="Éléments disponibles")

        self._build_overview(overview)
        self._build_timeline(timeline)
        self._build_evidence(evidence)

    def _section_title(self, parent: tk.Frame, title: str, subtitle: str) -> None:
        tk.Label(
            parent, text=title, bg=COLORS["card"], fg=COLORS["text"],
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor="w", padx=22, pady=(22, 5))
        tk.Label(
            parent, text=subtitle, bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 9), wraplength=850, justify="left",
        ).pack(anchor="w", padx=22, pady=(0, 16))

    def _build_overview(self, parent: tk.Frame) -> None:
        self._section_title(
            parent, "Contexte de l'incident",
            "Une entreprise française a signalé une indisponibilité de plusieurs systèmes "
            "informatiques et la présence d'un message réclamant une rançon.",
        )
        facts = (
            ("ENTREPRISE", "HexaTech Industries"),
            ("LOCALISATION", "France"),
            ("TYPE D'INCIDENT", "Suspicion de rançongiciel"),
            ("GROUPE MENTIONNÉ", "LockBit — revendication à vérifier"),
            ("DÉBUT ESTIMÉ", "Entre 01:00 et 03:00, le 4 novembre 2026"),
        )
        grid = tk.Frame(parent, bg=COLORS["card"])
        grid.pack(fill="x", padx=22)
        for label, value in facts:
            row = tk.Frame(grid, bg=COLORS["surface"], padx=12, pady=10)
            row.pack(fill="x", pady=3)
            tk.Label(
                row, text=label, bg=COLORS["surface"], fg=COLORS["muted"],
                font=("Segoe UI", 8, "bold"), width=22, anchor="w",
            ).pack(side="left")
            tk.Label(
                row, text=value, bg=COLORS["surface"], fg=COLORS["text"],
                font=("Segoe UI", 9), anchor="w",
            ).pack(side="left", fill="x", expand=True)

        note = tk.Frame(
            parent, bg=COLORS["accent_dark"], padx=14, pady=12,
        )
        note.pack(fill="x", padx=22, pady=(18, 12))
        tk.Label(
            note, text="POINT DE VIGILANCE",
            bg=COLORS["accent_dark"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            note,
            text=(
                "Le nom LockBit apparaît dans le message reçu par l'entreprise. "
                "Cela ne suffit pas à prouver qui est réellement à l'origine de l'attaque. "
                "Il faudra recouper plusieurs indices indépendants."
            ),
            bg=COLORS["accent_dark"], fg=COLORS["text"],
            font=("Segoe UI", 9), wraplength=850, justify="left",
        ).pack(anchor="w", pady=(5, 0))

    def _build_timeline(self, parent: tk.Frame) -> None:
        self._section_title(
            parent, "Premiers événements connus",
            "Les horaires ci-dessous proviennent des notes de l'équipe informatique. "
            "Ils indiquent les moments où les faits ont été observés.",
        )
        events = (
            ("02:18", "Première alerte", "Un utilisateur signale un comportement inhabituel."),
            ("02:31", "Serveur indisponible", "Le serveur de fichiers ne répond plus."),
            ("02:46", "Message de rançon", "Plusieurs postes affichent le même message."),
            ("03:05", "Mesures de confinement", "L'équipe commence à isoler certains équipements."),
            ("08:40", "Sauvegardes inaccessibles", "Les sauvegardes en ligne ne sont plus accessibles."),
        )
        for time, title, description in events:
            row = tk.Frame(parent, bg=COLORS["surface"], padx=14, pady=11)
            row.pack(fill="x", padx=22, pady=4)
            tk.Label(
                row, text=time, bg=COLORS["surface"], fg=COLORS["accent"],
                font=("Consolas", 11, "bold"), width=9, anchor="w",
            ).pack(side="left")
            detail = tk.Frame(row, bg=COLORS["surface"])
            detail.pack(side="left", fill="x", expand=True)
            tk.Label(
                detail, text=title, bg=COLORS["surface"], fg=COLORS["text"],
                font=("Segoe UI", 9, "bold"),
            ).pack(anchor="w")
            tk.Label(
                detail, text=description, bg=COLORS["surface"], fg=COLORS["muted"],
                font=("Segoe UI", 8), wraplength=700, justify="left",
            ).pack(anchor="w", pady=(2, 0))

        tk.Label(
            parent,
            text="Important : l'heure de détection d'un incident n'est pas forcément l'heure de l'intrusion.",
            bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 8, "italic"),
        ).pack(anchor="w", padx=22, pady=(12, 0))

    def _build_evidence(self, parent: tk.Frame) -> None:
        self._section_title(
            parent, "Pièces et informations reçues",
            "Ces éléments sont disponibles au début de l'enquête. "
            "Ouvrez la messagerie pour consulter le contenu des documents.",
        )
        items = (
            ("E-001", "Courriel de signalement", "Sophie Martin, responsable informatique", "Reçu"),
            ("E-002", "Rapport d'incident", "Description des systèmes touchés et des symptômes", "Reçu"),
            ("E-003", "Notes de l'équipe IT", "Premiers horaires observés le 4 novembre", "Reçu"),
            ("E-004", "Journaux techniques", "À obtenir lors de la prochaine étape", "En attente"),
        )
        for reference, title, description, status in items:
            row = tk.Frame(
                parent, bg=COLORS["surface"], padx=14, pady=12,
                highlightbackground=COLORS["border"], highlightthickness=1,
            )
            row.pack(fill="x", padx=22, pady=4)
            tk.Label(
                row, text=reference, bg=COLORS["surface"], fg=COLORS["accent"],
                font=("Consolas", 10, "bold"), width=9, anchor="w",
            ).pack(side="left")
            detail = tk.Frame(row, bg=COLORS["surface"])
            detail.pack(side="left", fill="x", expand=True)
            tk.Label(
                detail, text=title, bg=COLORS["surface"], fg=COLORS["text"],
                font=("Segoe UI", 9, "bold"),
            ).pack(anchor="w")
            tk.Label(
                detail, text=description, bg=COLORS["surface"], fg=COLORS["muted"],
                font=("Segoe UI", 8), wraplength=620, justify="left",
            ).pack(anchor="w", pady=(2, 0))
            tk.Label(
                row, text=status.upper(), bg=COLORS["surface"],
                fg=COLORS["green"] if status == "Reçu" else COLORS["muted"],
                font=("Segoe UI", 8, "bold"),
            ).pack(side="right", padx=(8, 0))
