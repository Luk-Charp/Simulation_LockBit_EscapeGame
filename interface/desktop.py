"""Bureau principal et navigation progressive de l'enquête."""

import tkinter as tk
from tkinter import messagebox

from interface.mail import MailWindow
from interface.case_file import CaseFileWindow
from interface.theme import COLORS


OBJECTIVES = (
    ("01", "Comprendre l'incident", "Lire le message de Sophie Martin et consulter le dossier initial."),
    ("02", "Reconstituer l'intrusion", "Examiner les journaux et retrouver les premières activités suspectes."),
    ("03", "Étudier l'infrastructure", "Analyser les adresses IP, les domaines et les connexions observées."),
    ("04", "Croiser les indices", "Comparer les découvertes avec les renseignements sur LockBit."),
    ("05", "Rédiger le rapport", "Présenter une chronologie et des conclusions justifiées."),
)


class Desktop:
    """Construit le bureau d'enquête et son parcours à étapes."""

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
        top = tk.Frame(self.root, bg=COLORS["taskbar"], height=66)
        top.pack(side="top", fill="x")
        top.pack_propagate(False)

        brand = tk.Frame(top, bg=COLORS["taskbar"])
        brand.pack(side="left", padx=30)
        tk.Label(
            brand, text="FBI", bg=COLORS["taskbar"], fg=COLORS["text"],
            font=("Segoe UI", 19, "bold"),
        ).pack(side="left")
        tk.Frame(brand, bg=COLORS["accent"], width=2, height=28).pack(
            side="left", padx=14, pady=18
        )
        tk.Label(
            brand, text="CYBER DIVISION", bg=COLORS["taskbar"],
            fg=COLORS["muted"], font=("Segoe UI", 9, "bold"),
        ).pack(side="left")

        right = tk.Frame(top, bg=COLORS["taskbar"])
        right.pack(side="right", padx=30)
        tk.Label(
            right, text="CELLULE D'INVESTIGATION",
            bg=COLORS["taskbar"], fg=COLORS["muted"],
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=(0, 18))
        tk.Label(
            right, text="OPÉRATION LOCKDOWN",
            bg=COLORS["taskbar"], fg=COLORS["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")

    def _build_workspace(self) -> None:
        workspace = tk.Frame(self.root, bg=COLORS["background"])
        workspace.pack(fill="both", expand=True)

        self._build_objective_sidebar(workspace)

        content = tk.Frame(workspace, bg=COLORS["background"])
        content.pack(side="left", fill="both", expand=True, padx=42, pady=34)

        intro = tk.Frame(content, bg=COLORS["background"])
        intro.pack(fill="x", pady=(0, 30))
        tk.Label(
            intro, text="CENTRE OPÉRATIONNEL  /  04 NOVEMBRE 2026",
            bg=COLORS["background"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            intro, text="Bienvenue, agent.",
            bg=COLORS["background"], fg=COLORS["text"],
            font=("Segoe UI", 30, "bold"),
        ).pack(anchor="w", pady=(10, 7))
        tk.Label(
            intro,
            text="Une cyberattaque a été signalée chez HexaTech Industries. "
                 "Votre cellule est chargée d'établir les faits et de reconstituer l'incident.",
            bg=COLORS["background"], fg=COLORS["muted"],
            font=("Segoe UI", 11), wraplength=900, justify="left",
        ).pack(anchor="w")

        section_header = tk.Frame(content, bg=COLORS["background"])
        section_header.pack(fill="x", pady=(0, 12))
        tk.Label(
            section_header, text="OUTILS D'INVESTIGATION",
            bg=COLORS["background"], fg=COLORS["text"],
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")
        tk.Label(
            section_header, text="05 APPLICATIONS DISPONIBLES",
            bg=COLORS["background"], fg=COLORS["muted"],
            font=("Segoe UI", 8, "bold"),
        ).pack(side="right")

        apps = tk.Frame(content, bg=COLORS["background"])
        apps.pack(fill="x")
        applications = [
            ("✉", "Messagerie", "Communications et signalements", "mail"),
            ("▤", "Dossier d'enquête", "Faits, chronologie et preuves", "case"),
            ("⌘", "Terminal", "Analyse des données", "terminal"),
            ("◎", "OSINT", "Renseignement en sources ouvertes", "osint"),
            ("⊕", "Cartographie", "Visualisation des pistes", "map"),
        ]
        for symbol, title, description, app_id in applications:
            self._create_app_card(apps, symbol, title, description, app_id)

        lower = tk.Frame(content, bg=COLORS["background"])
        lower.pack(fill="x", pady=(26, 0))

        briefing = tk.Frame(
            lower, bg=COLORS["surface"], padx=22, pady=20,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        briefing.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Label(
            briefing, text="BRIEFING DE MISSION",
            bg=COLORS["surface"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            briefing,
            text="Comprendre le déroulement de l'attaque, analyser les preuves disponibles "
                 "et formuler des conclusions étayées.",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 11), justify="left", wraplength=620,
        ).pack(anchor="w", pady=(10, 0))

        status = tk.Frame(
            lower, bg=COLORS["card"], padx=18, pady=18,
            highlightbackground=COLORS["border"], highlightthickness=1,
            width=230,
        )
        status.pack(side="right", fill="y")
        status.pack_propagate(False)
        tk.Label(
            status, text="STATUT DE L'AFFAIRE",
            bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w")
        tk.Label(
            status, text="EN COURS",
            bg=COLORS["card"], fg=COLORS["green"],
            font=("Segoe UI", 17, "bold"),
        ).pack(anchor="w", pady=(8, 2))
        tk.Label(
            status, text="Affaire #LK-2026-1104",
            bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 8),
        ).pack(anchor="w")

    def _build_objective_sidebar(self, parent: tk.Frame) -> None:
        sidebar = tk.Frame(
            parent, bg=COLORS["surface"], width=292,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        header = tk.Frame(sidebar, bg=COLORS["surface"])
        header.pack(fill="x", padx=20, pady=(24, 18))
        tk.Label(
            header, text="VOTRE PARCOURS",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header, text="Les objectifs se débloquent au fil de l'enquête.",
            bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8), wraplength=235, justify="left",
        ).pack(anchor="w", pady=(5, 0))

        self.progress_value = tk.Label(
            sidebar, text="0 / 5 ÉTAPES",
            bg=COLORS["surface"], fg=COLORS["accent"],
            font=("Segoe UI", 8, "bold"),
        )
        self.progress_value.pack(anchor="w", padx=20, pady=(0, 7))
        self.progress_canvas = tk.Canvas(
            sidebar, height=4, bg=COLORS["border"],
            highlightthickness=0, bd=0,
        )
        self.progress_canvas.pack(fill="x", padx=20, pady=(0, 20))

        for index, (number, title, description) in enumerate(OBJECTIVES):
            row = tk.Frame(sidebar, bg=COLORS["surface"], padx=10, pady=11)
            row.pack(fill="x", padx=12, pady=3)
            accent = tk.Frame(row, bg=COLORS["surface"], width=3)
            accent.pack(side="left", fill="y", padx=(0, 10))
            number_label = tk.Label(
                row, text=number, bg=COLORS["surface"],
                fg=COLORS["muted"], font=("Segoe UI", 9, "bold"), width=3,
            )
            number_label.pack(side="left", anchor="n")
            text_frame = tk.Frame(row, bg=COLORS["surface"])
            text_frame.pack(side="left", fill="x", expand=True, padx=(5, 0))
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
                (row, accent, number_label, title_label, status_label)
            )
            for widget in (row, accent, number_label, text_frame, title_label, status_label):
                widget.bind(
                    "<Button-1>",
                    lambda _event, selected=index: self._select_objective(selected),
                )

        self.objective_description = tk.Label(
            sidebar, text=OBJECTIVES[0][2],
            bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8), wraplength=240, justify="left",
        )
        self.objective_description.pack(anchor="w", padx=20, pady=(18, 12))

        self.complete_button = tk.Label(
            sidebar, text="VALIDER CETTE ÉTAPE",
            bg=COLORS["accent_dark"], fg=COLORS["text"],
            font=("Segoe UI", 8, "bold"), padx=10, pady=12,
            cursor="hand2",
        )
        self.complete_button.pack(fill="x", padx=16, pady=(0, 10))
        self.complete_button.bind(
            "<Button-1>", lambda _event: self._complete_selected_objective()
        )
        self.progress_label = tk.Label(
            sidebar, text="Progression de l'enquête",
            bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8),
        )
        self.progress_label.pack(anchor="w", padx=20, pady=(0, 16))

    def _select_objective(self, index: int) -> None:
        if index > len(self.completed_objectives):
            return
        self.selected_objective = index
        self.objective_description.configure(text=OBJECTIVES[index][2])
        self._refresh_objectives()

    def _complete_selected_objective(self) -> None:
        index = self.selected_objective
        if index in self.completed_objectives or index != len(self.completed_objectives):
            return
        confirmed = messagebox.askyesno(
            "Valider l'objectif",
            f"Avez-vous terminé l'objectif « {OBJECTIVES[index][1]} » ?\n\n"
            "La validation débloquera l'étape suivante.",
            parent=self.root,
        )
        if not confirmed:
            return
        self.completed_objectives.add(index)
        if len(self.completed_objectives) < len(OBJECTIVES):
            self.selected_objective = len(self.completed_objectives)
            self.objective_description.configure(text=OBJECTIVES[self.selected_objective][2])
        else:
            self.objective_description.configure(
                text="Tous les objectifs sont terminés. Préparez votre rapport final."
            )
        self._refresh_objectives()

    def _refresh_objectives(self) -> None:
        unlocked = len(self.completed_objectives)
        for index, (row, accent, number, title, status) in enumerate(self.objective_rows):
            done = index in self.completed_objectives
            available = index <= unlocked
            selected = index == self.selected_objective and available
            bg = COLORS["card"] if selected else COLORS["surface"]
            row.configure(bg=bg)
            accent.configure(bg=COLORS["accent"] if selected else COLORS["green"] if done else bg)
            for widget in (number, title, status):
                widget.configure(bg=bg)
            number.configure(fg=COLORS["green"] if done else COLORS["accent"] if available else COLORS["muted"])
            title.configure(fg=COLORS["text"] if available else COLORS["muted"])
            status.configure(
                text="TERMINÉ" if done else "EN COURS" if index == unlocked else "VERROUILLÉ",
                fg=COLORS["green"] if done else COLORS["accent"] if index == unlocked else COLORS["muted"],
            )

        count = len(self.completed_objectives)
        self.progress_value.configure(text=f"{count} / 5 ÉTAPES")
        self.progress_canvas.delete("all")
        self.progress_canvas.update_idletasks()
        width = self.progress_canvas.winfo_width()
        if width > 1:
            self.progress_canvas.create_rectangle(
                0, 0, width * count / 5, 4, fill=COLORS["accent"], outline="",
            )
        self.complete_button.configure(
            text="ENQUÊTE TERMINÉE" if count == 5 else "VALIDER CETTE ÉTAPE",
            bg=COLORS["card"] if count == 5 else COLORS["accent_dark"],
        )
        self.progress_label.configure(text=f"{count} objectif(s) validé(s) sur 5")

    def _create_app_card(
        self, parent: tk.Frame, symbol: str, title: str,
        description: str, app_id: str,
    ) -> None:
        card = tk.Frame(
            parent, bg=COLORS["surface"], width=158, height=154,
            highlightbackground=COLORS["border"], highlightthickness=1,
            cursor="hand2",
        )
        card.pack(side="left", padx=(0, 10), pady=2)
        card.pack_propagate(False)

        icon_wrap = tk.Frame(card, bg=COLORS["card"], width=42, height=42)
        icon_wrap.pack(anchor="w", padx=14, pady=(14, 12))
        icon_wrap.pack_propagate(False)
        icon = tk.Label(
            icon_wrap, text=symbol, bg=COLORS["card"], fg=COLORS["accent"],
            font=("Segoe UI Symbol", 20),
        )
        icon.place(relx=0.5, rely=0.5, anchor="center")
        heading = tk.Label(
            card, text=title, bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 9, "bold"), anchor="w",
        )
        heading.pack(fill="x", padx=14)
        subtitle = tk.Label(
            card, text=description, bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8), anchor="w", wraplength=130, justify="left",
        )
        subtitle.pack(fill="x", padx=14, pady=(5, 0))

        widgets = (card, icon_wrap, icon, heading, subtitle)
        for widget in widgets:
            widget.bind("<Button-1>", lambda _event, selected=app_id: self._open_application(selected))
            widget.bind("<Enter>", lambda _event, elements=widgets: self._set_card_color(elements, True))
            widget.bind("<Leave>", lambda _event, elements=widgets: self._set_card_color(elements, False))

    @staticmethod
    def _set_card_color(widgets: tuple, hovered: bool) -> None:
        card_bg = COLORS["card_hover"] if hovered else COLORS["surface"]
        icon_bg = COLORS["card"] if not hovered else COLORS["accent_dark"]
        for widget in widgets:
            widget.configure(bg=icon_bg if widget in widgets[1:3] else card_bg)

    def _open_application(self, app_id: str) -> None:
        if app_id == "mail":
            MailWindow(self.root)
        elif app_id == "case":
            CaseFileWindow(self.root)
        else:
            names = {"terminal": "Terminal", "osint": "OSINT", "map": "Cartographie"}
            name = names.get(app_id, "Application")
            messagebox.showinfo(
                name, f"L'application « {name} » sera développée dans une prochaine étape.",
                parent=self.root,
            )

    def _build_taskbar(self) -> None:
        taskbar = tk.Frame(self.root, bg=COLORS["taskbar"], height=38)
        taskbar.pack(side="bottom", fill="x")
        taskbar.pack_propagate(False)
        tk.Label(
            taskbar, text="●  SYSTÈME OPÉRATIONNEL",
            bg=COLORS["taskbar"], fg=COLORS["green"],
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=20)
        tk.Label(
            taskbar, text="SIMULATION PÉDAGOGIQUE  •  DONNÉES FICTIVES",
            bg=COLORS["taskbar"], fg=COLORS["muted"],
            font=("Segoe UI", 8),
        ).pack(side="right", padx=20)
