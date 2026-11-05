"""Bureau principal et navigation progressive de l'enquête."""

import tkinter as tk
from tkinter import messagebox

from interface.mail import MailWindow
from interface.case_file import CaseFileWindow
from interface.theme import COLORS


OBJECTIVES = (
    ("01", "Comprendre l'incident",
     "Lire le message de Sophie Martin et consulter le dossier initial."),
    ("02", "Reconstituer l'intrusion",
     "Examiner les journaux et retrouver les premières activités suspectes."),
    ("03", "Étudier l'infrastructure",
     "Analyser les adresses IP, les domaines et les connexions observées."),
    ("04", "Croiser les indices",
     "Comparer les découvertes avec les renseignements sur LockBit."),
    ("05", "Rédiger le rapport",
     "Présenter une chronologie et des conclusions justifiées."),
)


class Desktop:
    """Construit le bureau et le menu latéral des objectifs."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.configure(bg=COLORS["background"])
        self.root.option_add("*Font", ("Segoe UI", 10))
        self.completed_objectives = set()
        self.selected_objective = 0
        self.objective_rows = []
        self._build_top_bar()
        self._build_workspace()
        self._build_taskbar()
        self._refresh_objectives()

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

        self._build_objective_sidebar(workspace)

        content = tk.Frame(workspace, bg=COLORS["background"])
        content.pack(side="left", fill="both", expand=True, padx=34, pady=34)

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
            text="Une entreprise française a signalé une attaque informatique. "
                 "Consultez les outils mis à votre disposition pour débuter l'enquête.",
            bg=COLORS["background"], fg=COLORS["muted"],
            font=("Segoe UI", 11), wraplength=850, justify="left",
        ).pack(anchor="w", pady=(0, 24))

        tk.Label(
            content, text="OUTILS D'INVESTIGATION",
            bg=COLORS["background"], fg=COLORS["muted"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(0, 10))
        apps = tk.Frame(content, bg=COLORS["background"])
        apps.pack(anchor="w", fill="x")
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
        briefing.pack(fill="x", pady=(28, 0))
        tk.Label(
            briefing, text="BRIEFING DE MISSION",
            bg=COLORS["surface"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            briefing,
            text="Votre objectif : comprendre le déroulement de l'attaque, analyser les "
                 "preuves disponibles et formuler des conclusions étayées pour les autorités.",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 10), justify="left", wraplength=850,
        ).pack(anchor="w", pady=(7, 0))

    def _build_objective_sidebar(self, parent: tk.Frame) -> None:
        sidebar = tk.Frame(
            parent, bg=COLORS["taskbar"], width=270,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="PLAN D'ENQUÊTE", bg=COLORS["taskbar"],
            fg=COLORS["text"], font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=18, pady=(22, 4))
        tk.Label(
            sidebar, text="OBJECTIFS À ACCOMPLIR", bg=COLORS["taskbar"],
            fg=COLORS["muted"], font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=18, pady=(0, 18))

        for index, (number, title, description) in enumerate(OBJECTIVES):
            row = tk.Frame(
                sidebar, bg=COLORS["surface"], padx=10, pady=10,
                highlightbackground=COLORS["border"], highlightthickness=1,
            )
            row.pack(fill="x", padx=12, pady=4)
            number_label = tk.Label(
                row, text=number, bg=COLORS["surface"],
                fg=COLORS["muted"], font=("Consolas", 10, "bold"), width=3,
            )
            number_label.pack(side="left", anchor="n")
            text_frame = tk.Frame(row, bg=COLORS["surface"])
            text_frame.pack(side="left", fill="x", expand=True)
            title_label = tk.Label(
                text_frame, text=title, bg=COLORS["surface"],
                fg=COLORS["muted"], font=("Segoe UI", 9, "bold"),
                anchor="w", justify="left", wraplength=175,
            )
            title_label.pack(anchor="w")
            status_label = tk.Label(
                text_frame, text="VERROUILLÉ", bg=COLORS["surface"],
                fg=COLORS["muted"], font=("Segoe UI", 7, "bold"),
            )
            status_label.pack(anchor="w", pady=(4, 0))
            self.objective_rows.append(
                (row, number_label, title_label, status_label)
            )
            for widget in (row, number_label, text_frame, title_label, status_label):
                widget.bind(
                    "<Button-1>",
                    lambda _event, selected=index: self._select_objective(selected),
                )

        self.objective_description = tk.Label(
            sidebar, text="Sélectionnez l'objectif débloqué pour consulter les consignes.",
            bg=COLORS["taskbar"], fg=COLORS["muted"],
            font=("Segoe UI", 8), wraplength=225, justify="left",
        )
        self.objective_description.pack(anchor="w", padx=18, pady=(18, 10))

        self.complete_button = tk.Label(
            sidebar, text="VALIDER L'OBJECTIF",
            bg=COLORS["accent_dark"], fg=COLORS["text"],
            font=("Segoe UI", 8, "bold"), padx=10, pady=10,
            cursor="hand2",
        )
        self.complete_button.pack(fill="x", padx=14, pady=(0, 8))
        self.complete_button.bind(
            "<Button-1>", lambda _event: self._complete_selected_objective()
        )
        self.progress_label = tk.Label(
            sidebar, text="0 / 5 objectifs terminés",
            bg=COLORS["taskbar"], fg=COLORS["muted"],
            font=("Segoe UI", 8),
        )
        self.progress_label.pack(anchor="w", padx=18, pady=(4, 0))

    def _select_objective(self, index: int) -> None:
        if index > len(self.completed_objectives):
            return
        self.selected_objective = index
        self.objective_description.configure(
            text=OBJECTIVES[index][2]
        )
        self._refresh_objectives()

    def _complete_selected_objective(self) -> None:
        index = self.selected_objective
        if index in self.completed_objectives:
            return
        if index != len(self.completed_objectives):
            return

        title = OBJECTIVES[index][1]
        confirmed = messagebox.askyesno(
            "Valider l'objectif",
            f"Avez-vous terminé l'objectif « {title} » ?\n\n"
            "La validation débloquera l'étape suivante.",
            parent=self.root,
        )
        if not confirmed:
            return

        self.completed_objectives.add(index)
        if len(self.completed_objectives) < len(OBJECTIVES):
            self.selected_objective = len(self.completed_objectives)
            self.objective_description.configure(
                text=OBJECTIVES[self.selected_objective][2]
            )
        else:
            self.objective_description.configure(
                text="Tous les objectifs sont terminés. Préparez votre rapport final."
            )
        self._refresh_objectives()

    def _refresh_objectives(self) -> None:
        unlocked = len(self.completed_objectives)
        for index, (row, number, title, status) in enumerate(self.objective_rows):
            is_done = index in self.completed_objectives
            is_unlocked = index <= unlocked
            bg = COLORS["card_hover"] if index == self.selected_objective and is_unlocked else COLORS["surface"]
            row.configure(
                bg=bg,
                highlightbackground=COLORS["accent"] if index == self.selected_objective and is_unlocked else COLORS["border"],
            )
            for widget in (number, title, status):
                widget.configure(bg=bg)
            number.configure(
                fg=COLORS["green"] if is_done else COLORS["accent"] if is_unlocked else COLORS["muted"]
            )
            title.configure(
                fg=COLORS["text"] if is_unlocked else COLORS["muted"]
            )
            status.configure(
                text="TERMINÉ" if is_done else "EN COURS" if index == unlocked else "VERROUILLÉ",
                fg=COLORS["green"] if is_done else COLORS["accent"] if index == unlocked else COLORS["muted"],
            )
        if unlocked >= len(OBJECTIVES):
            self.complete_button.configure(text="ENQUÊTE TERMINÉE", bg=COLORS["card"])
            self.complete_button.unbind("<Button-1>")
        else:
            self.complete_button.configure(text="VALIDER L'OBJECTIF", bg=COLORS["accent_dark"])
        self.progress_label.configure(
            text=f"{len(self.completed_objectives)} / {len(OBJECTIVES)} objectifs terminés"
        )

    def _create_app_card(
        self, parent: tk.Frame, symbol: str, title: str,
        description: str, app_id: str,
    ) -> None:
        card = tk.Frame(
            parent, bg=COLORS["card"], width=155, height=142,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        card.pack(side="left", padx=(0, 9), pady=2)
        card.pack_propagate(False)
        icon = tk.Label(
            card, text=symbol, bg=COLORS["card"], fg=COLORS["accent"],
            font=("Segoe UI Symbol", 25),
        )
        icon.pack(anchor="w", padx=13, pady=(14, 8))
        heading = tk.Label(
            card, text=title, bg=COLORS["card"], fg=COLORS["text"],
            font=("Segoe UI", 9, "bold"), anchor="w",
        )
        heading.pack(fill="x", padx=13)
        subtitle = tk.Label(
            card, text=description, bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 7), anchor="w", wraplength=125, justify="left",
        )
        subtitle.pack(fill="x", padx=13, pady=(5, 0))
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
        if app_id == "mail":
            MailWindow(self.root)
        elif app_id == "case":
            CaseFileWindow(self.root)
        else:
            app_names = {
                "terminal": "Terminal", "osint": "OSINT", "map": "Carte",
            }
            app_name = app_names.get(app_id, "Application")
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
