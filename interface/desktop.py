"""Bureau principal et navigation progressive de l'enquête."""

import tkinter as tk
from tkinter import messagebox

from interface.mail import MailWindow
from interface.case_file import CaseFileWindow
from interface.theme import COLORS, center_window


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
        self.desktop_root = root
        self.root = root
        self.desktop_root.title("Debian GNU/Linux")
        self.desktop_root.configure(bg="#26384f")
        self.desktop_root.option_add("*Font", ("Segoe UI", 10))
        self.completed_objectives = set()
        self.selected_objective = 0
        self.objective_rows = []
        self.investigation_window = None
        self._build_debian_desktop()

    def _draw_app_icon(self, parent: tk.Misc, app_id: str, size: int, background: str) -> tk.Canvas:
        """Dessine une icône vectorielle cohérente, sans police ni ressource externe."""
        canvas = tk.Canvas(
            parent, width=size, height=size, bg=background,
            highlightthickness=0, bd=0,
        )
        scale = size / 64
        def coords(values):
            return tuple(value * scale for value in values)
        colors = {
            "investigation": ("#173e67", "#f4c95d", "#ffffff"),
            "mail": ("#245b91", "#8fd3f4", "#ffffff"),
            "case": ("#a86a22", "#f5c66b", "#fff4d8"),
            "terminal": ("#263746", "#75d6b0", "#ffffff"),
            "osint": ("#245d72", "#79d6df", "#ffffff"),
            "map": ("#28634f", "#8cdbad", "#ffffff"),
        }
        primary, accent, light = colors.get(app_id, ("#40536a", "#ffffff", "#ffffff"))
        if app_id == "investigation":
            # Insigne rond, sans cadre carré parasite autour du logo.
            canvas.create_oval(
                *coords((5, 5, 59, 59)), fill=primary,
                outline=accent, width=max(2, int(3 * scale)),
            )
            canvas.create_polygon(
                *coords((16, 17, 48, 17, 45, 34, 32, 49, 19, 34)),
                fill=light, outline=accent, width=max(1, int(1.5 * scale)),
            )
            canvas.create_text(
                *coords((32, 28)), text="FBI", fill=primary,
                font=("Segoe UI", max(7, int(11 * scale)), "bold"),
            )
        else:
            canvas.create_rectangle(*coords((5, 5, 59, 59)), fill=primary, outline="")
            canvas.create_rectangle(*coords((5, 5, 59, 59)), outline="#ffffff", width=max(1, int(scale)))
        if app_id == "mail":
            canvas.create_rectangle(*coords((15, 19, 49, 45)), fill=light, outline="")
            canvas.create_line(*coords((15, 20, 32, 34, 49, 20)), fill=primary, width=max(2, int(3*scale)), smooth=True)
        elif app_id == "case":
            canvas.create_rectangle(*coords((12, 22, 52, 47)), fill=accent, outline="")
            canvas.create_rectangle(*coords((17, 16, 32, 25)), fill=accent, outline="")
            canvas.create_rectangle(*coords((12, 27, 52, 47)), fill=light, outline="")
            canvas.create_rectangle(*coords((12, 27, 52, 47)), outline=accent, width=max(1, int(2*scale)))
        elif app_id == "terminal":
            canvas.create_rectangle(*coords((12, 15, 52, 49)), fill="#101b29", outline=accent, width=max(1, int(2*scale)))
            canvas.create_line(*coords((19, 25, 26, 31, 19, 37)), fill=accent, width=max(2, int(3*scale)))
            canvas.create_line(*coords((30, 38, 42, 38)), fill=light, width=max(2, int(3*scale)))
        elif app_id == "osint":
            canvas.create_oval(*coords((14, 12, 45, 43)), outline=light, width=max(2, int(3*scale)))
            canvas.create_line(*coords((37, 36, 51, 51)), fill=accent, width=max(3, int(5*scale)))
            canvas.create_oval(*coords((21, 19, 38, 36)), outline=accent, width=max(1, int(2*scale)))
        elif app_id == "map":
            canvas.create_polygon(*coords((12, 17, 25, 12, 39, 18, 52, 12, 52, 45, 39, 51, 25, 45, 12, 51)), fill=light, outline="")
            canvas.create_line(*coords((25, 12, 25, 45)), fill=primary, width=max(1, int(2*scale)))
            canvas.create_line(*coords((39, 18, 39, 51)), fill=primary, width=max(1, int(2*scale)))
            canvas.create_oval(*coords((29, 23, 38, 32)), fill="#d94d58", outline="")
        return canvas

    def _build_debian_desktop(self) -> None:
        """Construit un bureau Linux sombre, lisible et organisé comme un poste de travail."""
        wallpaper = tk.Canvas(
            self.desktop_root, bg="#172b42", highlightthickness=0, bd=0,
        )
        wallpaper.pack(fill="both", expand=True)
        wallpaper.bind(
            "<Configure>",
            lambda event: self._center_wallpaper(wallpaper, event),
        )

        desktop_apps = [
            ("Opération Lockdown", "investigation"),
            ("Messagerie", "mail"),
            ("Dossier enquête", "case"),
            ("Terminal", "terminal"),
            ("OSINT", "osint"),
            ("Cartographie", "map"),
        ]
        for index, (title, app_id) in enumerate(desktop_apps):
            column, row = index // 3, index % 3
            shortcut = tk.Frame(
                self.desktop_root, bg="#263d57", width=142, height=112,
                cursor="hand2", highlightthickness=1,
                highlightbackground="#405a76",
            )
            shortcut.place(x=24 + column * 154, y=52 + row * 126)
            shortcut.pack_propagate(False)

            icon = self._draw_app_icon(shortcut, app_id, 48, "#263d57")
            icon.pack(pady=(10, 5))
            label = tk.Label(
                shortcut, text=title, bg="#263d57", fg="#f4f7fb",
                font=("Segoe UI", 9, "bold"), wraplength=128,
                justify="center", cursor="hand2",
            )
            label.pack(fill="x", padx=5)

            widgets = (shortcut, icon, label)
            shortcut.bind(
                "<Enter>",
                lambda _event, elements=widgets: self._set_shortcut_hover(elements, True),
            )
            shortcut.bind(
                "<Leave>",
                lambda _event, elements=widgets: self._set_shortcut_hover(elements, False),
            )
            label.bind(
                "<Enter>",
                lambda _event, elements=widgets: self._set_shortcut_hover(elements, True),
            )
            label.bind(
                "<Leave>",
                lambda _event, elements=widgets: self._set_shortcut_hover(elements, False),
            )
            for widget in widgets:
                widget.bind(
                    "<Double-Button-1>",
                    lambda _event, selected=app_id: self._open_application(selected),
                )
                widget.bind(
                    "<Button-1>",
                    lambda _event, frame=shortcut: self._select_desktop_icon(frame, True),
                )

        self._build_taskbar(self.desktop_root)

    @staticmethod
    def _center_wallpaper(canvas: tk.Canvas, event) -> None:
        """Dessine un fond structuré avec une zone d'accueil discrète."""
        canvas.delete("wallpaper")
        width, height = event.width, event.height

        # Bandes de fond pour donner de la profondeur sans image externe.
        canvas.create_rectangle(
            0, 0, width, height, fill="#172b42", outline="", tags="wallpaper",
        )
        canvas.create_polygon(
            width * 0.42, 0, width, 0, width, height, width * 0.70, height,
            fill="#1c344e", outline="", tags="wallpaper",
        )
        canvas.create_oval(
            width * 0.48, -height * 0.72, width * 1.22, height * 0.95,
            outline="#294763", width=2, tags="wallpaper",
        )
        canvas.create_oval(
            width * 0.56, -height * 0.60, width * 1.14, height * 0.80,
            outline="#233f5b", width=2, tags="wallpaper",
        )
        canvas.create_line(
            width * 0.66, 0, width * 0.34, height,
            fill="#203a55", width=2, tags="wallpaper",
        )

        # En-tête système en haut à gauche.
        canvas.create_text(
            26, 20, text="DEBIAN  /  CYBER WORKSTATION",
            anchor="nw", fill="#dce7f2",
            font=("Segoe UI", 9, "bold"), tags="wallpaper",
        )
        canvas.create_text(
            26, 40, text="ENVIRONNEMENT D'INVESTIGATION NUMÉRIQUE",
            anchor="nw", fill="#8fa6bd",
            font=("Segoe UI", 7), tags="wallpaper",
        )

        # Carte d'accueil à droite : le texte narratif reste strictement identique.
        panel_x = width * 0.48
        panel_y = height * 0.40
        canvas.create_rectangle(
            panel_x, panel_y, width - 42, panel_y + 142,
            fill="#203952", outline="#385570", width=1,
            tags="wallpaper",
        )
        canvas.create_rectangle(
            panel_x, panel_y, panel_x + 4, panel_y + 142,
            fill="#d6b15e", outline="", tags="wallpaper",
        )
        canvas.create_text(
            panel_x + 24, panel_y + 22,
            text="POSTE DE TRAVAIL SÉCURISÉ",
            anchor="nw", fill="#d6b15e",
            font=("Segoe UI", 8, "bold"), tags="wallpaper",
        )
        canvas.create_text(
            panel_x + 24, panel_y + 48,
            text="Opération Lockdown",
            anchor="nw", fill="#f4f7fb",
            font=("Segoe UI", 23, "bold"), tags="wallpaper",
        )
        canvas.create_text(
            panel_x + 24, panel_y + 88,
            text="HexaTech Industries  •  Affaire #LK-2026-1104",
            anchor="nw", fill="#b8c8d8",
            font=("Segoe UI", 9), tags="wallpaper",
        )
        canvas.create_text(
            panel_x + 24, panel_y + 116,
            text="Double-cliquez sur une application pour commencer.",
            anchor="nw", fill="#8fa6bd",
            font=("Segoe UI", 8), tags="wallpaper",
        )

    @staticmethod
    def _set_shortcut_hover(widgets: tuple, hovered: bool) -> None:
        background = "#36536f" if hovered else "#263d57"
        border = "#8eb4d8" if hovered else "#405a76"
        widgets[0].configure(bg=background, highlightbackground=border)
        widgets[1].configure(bg=background)
        widgets[2].configure(bg=background)

    @staticmethod
    def _select_desktop_icon(widget: tk.Widget, selected: bool) -> None:
        widget.configure(highlightbackground="#7ca6d8", highlightthickness=2)

    @staticmethod
    def _set_shortcut_hover(widgets: tuple, hovered: bool) -> None:
        background = "#344d68" if hovered else "#26384f"
        widgets[0].configure(bg=background, highlightbackground="#7ca6d8" if hovered else "#26384f")
        widgets[1].configure(bg=background)
        widgets[2].configure(bg=background)

    def _open_investigation(self) -> None:
        """Ouvre l'application d'enquête dans une fenêtre indépendante."""
        if self.investigation_window is not None and self.investigation_window.winfo_exists():
            self.investigation_window.deiconify()
            self.investigation_window.lift()
            return

        self.investigation_window = tk.Toplevel(self.desktop_root)
        self.root = self.investigation_window
        self.root.title("Opération Lockdown — FBI Cyber Division")
        self.root.configure(bg=COLORS["background"])
        self.root.minsize(980, 640)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width, height = min(1280, screen_width - 100), min(820, screen_height - 120)
        x, y = (screen_width - width) // 2, (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.option_add("*Font", ("Segoe UI", 10))
        self.objective_rows = []
        self._build_top_bar()
        self._build_workspace()
        self._refresh_objectives()
        self.root.protocol("WM_DELETE_WINDOW", self._close_investigation)

    def _close_investigation(self) -> None:
        if self.investigation_window is not None:
            self.investigation_window.destroy()
        self.investigation_window = None
        self.root = self.desktop_root

    def _build_top_bar(self) -> None:
        top = tk.Frame(self.root, bg=COLORS["taskbar"], height=66)
        top.pack(side="top", fill="x")
        top.pack_propagate(False)

        brand = tk.Frame(top, bg=COLORS["taskbar"])
        brand.pack(side="left", padx=30)
        logo = tk.Canvas(
            brand, width=48, height=48, bg=COLORS["taskbar"],
            highlightthickness=0,
        )
        logo.pack(side="left", pady=8)
        logo.create_oval(2, 2, 46, 46, outline=COLORS["gold"], width=2)
        logo.create_oval(6, 6, 42, 42, outline="#ffffff", width=1)
        logo.create_text(24, 24, text="FBI", fill="#ffffff", font=("Georgia", 12, "bold"))
        tk.Frame(brand, bg=COLORS["gold"], width=3, height=34).pack(
            side="left", padx=12, pady=16
        )
        identity = tk.Frame(brand, bg=COLORS["taskbar"])
        identity.pack(side="left")
        tk.Label(
            identity, text="FEDERAL BUREAU OF INVESTIGATION",
            bg=COLORS["taskbar"], fg=COLORS["on_dark"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            identity, text="CYBER DIVISION  •  DIGITAL INVESTIGATIONS",
            bg=COLORS["taskbar"], fg=COLORS["gold"],
            font=("Segoe UI", 7, "bold"),
        ).pack(anchor="w", pady=(2, 0))

        right = tk.Frame(top, bg=COLORS["taskbar"])
        right.pack(side="right", padx=30)
        tk.Label(
            right, text="CELLULE D'INVESTIGATION",
            bg=COLORS["taskbar"], fg=COLORS["on_dark_muted"],
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=(0, 18))
        tk.Label(
            right, text="OPÉRATION LOCKDOWN",
            bg=COLORS["taskbar"], fg=COLORS["gold"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")

    def _build_workspace(self) -> None:
        workspace = tk.Frame(self.root, bg=COLORS["background"])
        workspace.pack(fill="both", expand=True)

        self._build_objective_sidebar(workspace)

        content_shell = tk.Frame(workspace, bg=COLORS["background"])
        content_shell.pack(side="left", fill="both", expand=True)
        content_canvas = tk.Canvas(
            content_shell, bg=COLORS["background"], highlightthickness=0, bd=0,
        )
        content_scrollbar = tk.Scrollbar(
            content_shell, orient="vertical", command=content_canvas.yview,
        )
        content_canvas.configure(yscrollcommand=content_scrollbar.set)
        content_canvas.pack(side="left", fill="both", expand=True)
        content_scrollbar.pack(side="right", fill="y")
        content = tk.Frame(content_canvas, bg=COLORS["background"], padx=42, pady=34)
        content_window = content_canvas.create_window(
            (0, 0), window=content, anchor="nw",
        )
        content.bind(
            "<Configure>",
            lambda _event: content_canvas.configure(
                scrollregion=content_canvas.bbox("all")
            ),
        )
        content_canvas.bind(
            "<Configure>",
            lambda event: content_canvas.itemconfigure(
                content_window, width=event.width
            ),
        )

        intro = tk.Frame(content, bg=COLORS["background"])
        intro.pack(fill="x", pady=(0, 30))
        tk.Label(
            intro, text="FEDERAL BUREAU OF INVESTIGATION     /     CYBER DIVISION",
            bg=COLORS["background"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            intro, text="Bonjour, agents.",
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
                (row, accent, number_label, text_frame, title_label, status_label)
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
            sidebar, text="PASSER LE CHECKPOINT",
            bg=COLORS["accent_dark"], fg=COLORS["button_text"],
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

        # Le premier checkpoint est rédigé. Les suivants seront ajoutés
        # au même format avec les prochaines étapes de la mission.
        if index == 0:
            from interface.checkpoint import CheckpointWindow
            from missions.mission_01 import CHECKPOINT

            CheckpointWindow(
                self.root,
                CHECKPOINT,
                on_pass=lambda: self._mark_objective_complete(index),
            )
        else:
            messagebox.showinfo(
                "Checkpoint en préparation",
                "Le questionnaire de cette étape sera ajouté avec les prochains éléments de mission.",
                parent=self.root,
            )

    def _mark_objective_complete(self, index: int) -> None:
        if index in self.completed_objectives:
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
        for index, (row, accent, number, text_frame, title, status) in enumerate(self.objective_rows):
            done = index in self.completed_objectives
            available = index <= unlocked
            selected = index == self.selected_objective and available
            bg = COLORS["card"] if selected else COLORS["surface"]
            row.configure(bg=bg)
            accent.configure(bg=COLORS["accent"] if selected else COLORS["green"] if done else bg)
            for widget in (number, text_frame, title, status):
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
            text="ENQUÊTE TERMINÉE" if count == 5 else "PASSER LE CHECKPOINT",
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
        """Ouvre les applications depuis le bureau Debian."""
        if app_id == "investigation":
            self._open_investigation()
        elif app_id == "mail":
            MailWindow(self.desktop_root)
        elif app_id == "case":
            CaseFileWindow(self.desktop_root)
        else:
            names = {"terminal": "Terminal", "osint": "OSINT", "map": "Cartographie"}
            name = names.get(app_id, "Application")
            window = tk.Toplevel(self.desktop_root)
            window.title(name)
            window.configure(bg=COLORS["background"])
            center_window(window, 760, 520)
            header = tk.Frame(window, bg=COLORS["taskbar"], padx=24, pady=18)
            header.pack(fill="x")
            tk.Label(
                header, text="BUREAU D'INVESTIGATION  /  OUTIL",
                bg=COLORS["taskbar"], fg=COLORS["gold"],
                font=("Segoe UI", 8, "bold"),
            ).pack(anchor="w")
            tk.Label(
                header, text=name, bg=COLORS["taskbar"], fg=COLORS["on_dark"],
                font=("Segoe UI", 18, "bold"),
            ).pack(anchor="w", pady=(5, 0))
            panel = tk.Frame(
                window, bg=COLORS["surface"], padx=24, pady=22,
                highlightbackground=COLORS["border"], highlightthickness=1,
            )
            panel.pack(fill="both", expand=True, padx=24, pady=24)
            tk.Label(
                panel, text="Application en préparation",
                bg=COLORS["surface"], fg=COLORS["accent"],
                font=("Segoe UI", 11, "bold"),
            ).pack(anchor="w")
            tk.Label(
                panel,
                text="Cette application sera enrichie au fil du développement.",
                bg=COLORS["surface"], fg=COLORS["muted"],
                font=("Segoe UI", 10), wraplength=560, justify="left",
            ).pack(anchor="w", pady=(8, 0))

    def _build_taskbar(self, parent: tk.Misc | None = None) -> None:
        """Construit une véritable barre des tâches horizontale, inspirée de Linux."""
        taskbar = tk.Frame(
            parent or self.desktop_root, bg=COLORS["taskbar"], height=72,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        taskbar.pack(side="bottom", fill="x")
        taskbar.pack_propagate(False)

        # Lanceur d'applications à gauche.
        launcher = tk.Label(
            taskbar, text="▦", bg=COLORS["taskbar"], fg=COLORS["on_dark"],
            font=("Segoe UI Symbol", 25), width=3, cursor="hand2",
        )
        launcher.pack(side="left", padx=(12, 8), pady=7)
        launcher.bind(
            "<Button-1>",
            lambda _event: messagebox.showinfo(
                "Applications", "Double-cliquez une icône du bureau pour ouvrir une application.",
                parent=self.desktop_root,
            ),
        )
        tk.Frame(taskbar, bg=COLORS["border"], width=1).pack(
            side="left", fill="y", pady=13, padx=5
        )

        # Applications épinglées : grandes icônes, avec leur nom en petit dessous.
        app_group = tk.Frame(taskbar, bg=COLORS["taskbar"])
        app_group.pack(side="left", padx=8, pady=4)

        applications = [
            ("Messagerie", "mail"),
            ("Dossier", "case"),
            ("Terminal", "terminal"),
            ("OSINT", "osint"),
            ("Cartographie", "map"),
        ]
        self.dock_items = []
        for title, app_id in applications:
            item = tk.Frame(
                app_group, bg=COLORS["taskbar"], width=82, height=62,
                cursor="hand2",
            )
            item.pack(side="left", padx=2)
            item.pack_propagate(False)

            icon = self._draw_app_icon(item, app_id, 34, COLORS["taskbar"])
            icon.pack(pady=(3, 0))
            label = tk.Label(
                item, text=title, bg=COLORS["taskbar"], fg=COLORS["on_dark_muted"],
                font=("Segoe UI", 7), cursor="hand2",
            )
            label.pack()
            widgets = (item, icon, label)
            self.dock_items.append((app_id, widgets))
            for widget in widgets:
                widget.bind(
                    "<Button-1>",
                    lambda _event, selected=app_id: self._open_application(selected),
                )
                widget.bind(
                    "<Enter>",
                    lambda _event, elements=widgets: self._set_dock_hover(elements, True),
                )
                widget.bind(
                    "<Leave>",
                    lambda _event, elements=widgets: self._set_dock_hover(elements, False),
                )

        # Zone d'état à droite, séparée des applications.
        right = tk.Frame(taskbar, bg=COLORS["taskbar"])
        right.pack(side="right", padx=18, pady=0)
        tk.Label(
            right, text="●", bg=COLORS["taskbar"], fg=COLORS["green"],
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(0, 6))
        tk.Label(
            right, text="SYSTÈME OPÉRATIONNEL",
            bg=COLORS["taskbar"], fg=COLORS["on_dark_muted"],
            font=("Segoe UI", 7, "bold"),
        ).pack(side="left")

    @staticmethod
    def _set_dock_hover(widgets: tuple, hovered: bool) -> None:
        """Éclaire discrètement l'icône survolée dans la barre des tâches."""
        background = COLORS["accent_dark"] if hovered else COLORS["taskbar"]
        for widget in widgets:
            widget.configure(bg=background)
