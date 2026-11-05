"""Dossier centralisant les informations et preuves de l'affaire."""

import tkinter as tk
from tkinter import ttk

from interface.theme import COLORS, center_window


class CaseFileWindow:
    """Dossier d'enquête cohérent avec le signalement HexaTech."""

    def __init__(self, parent: tk.Misc) -> None:
        self.window = tk.Toplevel(parent)
        self.window.title("Dossier d'enquête — Opération Lockdown")
        self.window.transient(parent)
        self.window.configure(bg=COLORS["background"])
        center_window(self.window, 1100, 800)
        self._configure_style()
        self._scroll_canvases = []
        self._build_interface()
        self.window.bind_all("<MouseWheel>", self._on_trackpad_scroll, add="+")
        self.window.bind_all("<Button-4>", self._on_trackpad_scroll, add="+")
        self.window.bind_all("<Button-5>", self._on_trackpad_scroll, add="+")
        self.window.bind("<Destroy>", self._cleanup_scroll_bindings, add="+")

    def _configure_style(self) -> None:
        style = ttk.Style(self.window)
        style.theme_use("clam")
        style.configure(
            "Case.TNotebook", background=COLORS["background"], borderwidth=0,
        )
        style.configure(
            "Case.TNotebook.Tab",
            background=COLORS["surface"], foreground=COLORS["muted"],
            padding=(16, 10), borderwidth=0, focuscolor=COLORS["surface"],
            lightcolor=COLORS["surface"], darkcolor=COLORS["surface"],
        )
        style.layout(
            "Case.TNotebook.Tab",
            [("Notebook.tab", {
                "sticky": "nswe",
                "children": [("Notebook.padding", {
                    "side": "top", "sticky": "nswe",
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
            bg=COLORS["taskbar"], fg=COLORS["on_dark"],
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left", padx=22)
        tk.Label(
            header, text="AFFAIRE #LK-2026-1104",
            bg=COLORS["taskbar"], fg=COLORS["on_dark_muted"],
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
            summary, text="Cyberattaque présumée — suspicion de rançongiciel",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 17, "bold"),
        ).pack(anchor="w", pady=(5, 3))
        tk.Label(
            summary,
            text="Signalement de Sophie Martin reçu le 4 novembre 2026 à 09:14  •  Enquête initiale",
            bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        notebook = ttk.Notebook(wrapper, style="Case.TNotebook", takefocus=False)
        notebook.pack(fill="both", expand=True)
        overview, overview_content = self._create_scrollable_tab(notebook)
        timeline, timeline_content = self._create_scrollable_tab(notebook)
        evidence, evidence_content = self._create_scrollable_tab(notebook)
        notebook.add(overview, text="Vue d'ensemble")
        notebook.add(timeline, text="Chronologie")
        notebook.add(evidence, text="Éléments disponibles")
        self._build_overview(overview_content)
        self._build_timeline(timeline_content)
        self._build_evidence(evidence_content)

    def _create_scrollable_tab(self, notebook: ttk.Notebook):
        """Crée un onglet dont le contenu reste accessible même s'il dépasse la fenêtre."""
        tab = tk.Frame(notebook, bg=COLORS["card"])
        canvas = tk.Canvas(
            tab, bg=COLORS["card"], highlightthickness=0, borderwidth=0,
        )
        scrollbar = tk.Scrollbar(
            tab, orient="vertical", command=canvas.yview,
            bg=COLORS["surface"], troughcolor=COLORS["card"],
            activebackground=COLORS["accent"],
        )
        content = tk.Frame(canvas, bg=COLORS["card"])
        content_window = canvas.create_window(
            (0, 0), window=content, anchor="nw",
        )

        def update_scroll_region(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def resize_content(event):
            canvas.itemconfigure(content_window, width=event.width)

        content.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", resize_content)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._scroll_canvases.append(canvas)
        return tab, content

    def _on_trackpad_scroll(self, event):
        """Fait défiler l'onglet visible sous le pointeur, y compris avec le trackpad Mac."""
        try:
            pointer_x = self.window.winfo_pointerx()
            pointer_y = self.window.winfo_pointery()
        except tk.TclError:
            return

        for canvas in self._scroll_canvases:
            if not canvas.winfo_exists() or not canvas.winfo_ismapped():
                continue
            left, top = canvas.winfo_rootx(), canvas.winfo_rooty()
            right, bottom = left + canvas.winfo_width(), top + canvas.winfo_height()
            if not (left <= pointer_x <= right and top <= pointer_y <= bottom):
                continue

            delta = getattr(event, "delta", 0)
            if delta:
                # macOS transmet souvent des deltas très faibles (±1 ou ±2).
                # Windows transmet généralement des multiples de 120.
                units = max(1, int(abs(delta) / 120 * 3)) if abs(delta) >= 120 else max(1, int(abs(delta)))
                canvas.yview_scroll(-units if delta > 0 else units, "units")
            elif getattr(event, "num", None) == 4:
                canvas.yview_scroll(-1, "units")
            elif getattr(event, "num", None) == 5:
                canvas.yview_scroll(1, "units")
            return "break"
        return None

    def _cleanup_scroll_bindings(self, event) -> None:
        """Retire les bindings globaux lorsque la fenêtre du dossier est détruite."""
        if event.widget is not self.window:
            return
        for sequence in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            try:
                self.window.unbind_all(sequence)
            except tk.TclError:
                pass

    def _section_title(self, parent: tk.Frame, title: str, subtitle: str) -> None:
        tk.Label(
            parent, text=title, bg=COLORS["card"], fg=COLORS["text"],
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor="w", padx=22, pady=(22, 5))
        tk.Label(
            parent, text=subtitle, bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 9), wraplength=850, justify="left",
        ).pack(anchor="w", padx=22, pady=(0, 16))

    def _fact_rows(self, parent: tk.Frame, facts: tuple) -> None:
        grid = tk.Frame(parent, bg=COLORS["card"])
        grid.pack(fill="x", padx=22)
        for label, value in facts:
            row = tk.Frame(grid, bg=COLORS["surface"], padx=12, pady=9)
            row.pack(fill="x", pady=3)
            tk.Label(
                row, text=label, bg=COLORS["surface"], fg=COLORS["muted"],
                font=("Segoe UI", 8, "bold"), width=23, anchor="w",
            ).pack(side="left")
            tk.Label(
                row, text=value, bg=COLORS["surface"], fg=COLORS["text"],
                font=("Segoe UI", 9), anchor="w", justify="left",
                wraplength=700,
            ).pack(side="left", fill="x", expand=True)

    def _notice(self, parent: tk.Frame, title: str, text: str) -> None:
        note = tk.Frame(parent, bg=COLORS["accent_dark"], padx=14, pady=12)
        note.pack(fill="x", padx=22, pady=(16, 12))
        tk.Label(
            note, text=title, bg=COLORS["accent_dark"], fg=COLORS["on_dark"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            note, text=text, bg=COLORS["accent_dark"], fg=COLORS["on_dark_muted"],
            font=("Segoe UI", 9), wraplength=850, justify="left",
        ).pack(anchor="w", pady=(5, 0))

    def _build_overview(self, parent: tk.Frame) -> None:
        self._section_title(
            parent, "Situation signalée",
            "Le 4 novembre 2026, Sophie Martin, responsable informatique de HexaTech Industries, "
            "a contacté la FBI Cyber Division après la découverte d'une attaque affectant "
            "les fichiers et les serveurs de l'entreprise.",
        )
        self._fact_rows(parent, (
            ("ENTREPRISE", "HexaTech Industries"),
            ("CONTACT", "Sophie Martin — Responsable informatique"),
            ("LOCALISATION", "France"),
            ("PREMIERS PROBLÈMES", "4 novembre 2026, vers 08:45"),
            ("SYMPTÔMES", "Fichiers inaccessibles, serveurs indisponibles, dossiers partagés manquants"),
            ("MESSAGE DE RANÇON", "Mentionne LockBit et menace de publier les données"),
            ("INDICE ANTÉRIEUR", "Activité inhabituelle signalée sur le poste d'un employé la veille au soir"),
            ("ÉTAT DE L'ENQUÊTE", "Origine de l'intrusion et systèmes compromis non déterminés"),
        ))
        self._notice(
            parent, "HYPOTHÈSE À EXAMINER",
            "Les éléments évoquent une attaque par rançongiciel avec une possible menace "
            "de divulgation de données. La mention de LockBit est une revendication figurant "
            "dans le message reçu par l'entreprise : elle ne constitue pas, à elle seule, "
            "une preuve de l'identité des attaquants.",
        )
        self._notice(
            parent, "QUESTIONS PRIORITAIRES",
            "Comment l'accès initial a-t-il été obtenu ? L'activité inhabituelle de la veille "
            "est-elle liée à l'incident ? Quels systèmes ont été touchés ? Existe-t-il des "
            "indices d'un accès ou d'une extraction de données ?",
        )

    def _build_timeline(self, parent: tk.Frame) -> None:
        self._section_title(
            parent, "Chronologie provisoire",
            "Cette chronologie combine les déclarations de Sophie Martin et les premières "
            "informations communiquées par l'entreprise. Les heures exactes restent à confirmer "
            "par l'analyse des journaux.",
        )
        events = (
            ("03 NOV. — SOIR", "Activité inhabituelle signalée",
             "Un employé remarque un comportement inhabituel sur son ordinateur. L'heure précise et la nature de l'activité restent à établir."),
            ("04 NOV. — 08:45", "Premiers problèmes d'accès",
             "Plusieurs employés signalent qu'ils ne peuvent plus accéder normalement à leurs fichiers."),
            ("04 NOV. — QUELQUES MINUTES APRÈS", "Serveurs inaccessibles",
             "Les serveurs deviennent inaccessibles. Certains ordinateurs affichent une demande de rançon."),
            ("04 NOV. — MATIN", "Dossiers partagés indisponibles",
             "Plusieurs dossiers partagés ont disparu ou ne sont plus accessibles. Le message de rançon mentionne LockBit et menace de publier les données."),
            ("04 NOV. — AVANT 09:14", "Arrêt des interventions internes",
             "Le service informatique interrompt ses tentatives d'intervention afin de ne pas aggraver la situation et de préserver les éléments disponibles."),
            ("04 NOV. — 09:14", "Signalement transmis au FBI",
             "Sophie Martin envoie un courriel à la FBI Cyber Division pour demander de l'aide."),
            ("04 NOV. — 09:30", "Ouverture de l'enquête",
             "Le responsable de la cellule transmet les consignes : examiner l'incident, reconstituer l'intrusion, étudier les infrastructures, croiser les indices et rédiger un rapport."),
        )
        for time, title, description in events:
            row = tk.Frame(parent, bg=COLORS["surface"], padx=14, pady=10)
            row.pack(fill="x", padx=22, pady=3)
            tk.Label(
                row, text=time, bg=COLORS["surface"], fg=COLORS["accent"],
                font=("Consolas", 9, "bold"), width=25, anchor="nw",
                justify="left", wraplength=175,
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
            text="Important : l'heure à laquelle un problème est découvert ne correspond pas nécessairement au début de l'intrusion.",
            bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 8, "italic"), wraplength=850, justify="left",
        ).pack(anchor="w", padx=22, pady=(10, 0))

    def _build_evidence(self, parent: tk.Frame) -> None:
        self._section_title(
            parent, "Éléments disponibles au lancement",
            "Les éléments ci-dessous sont mentionnés dans le signalement initial ou doivent "
            "être récupérés au cours de l'enquête. Consultez la messagerie pour lire le courriel "
            "et ouvrir les deux pièces jointes.",
        )
        items = (
            ("E-001", "Courriel de Sophie Martin",
             "Signalement du 4 novembre à 09:14 : symptômes, demande de rançon, activité inhabituelle la veille et connexions suspectes.", "REÇU"),
            ("E-002", "rapport_incident.txt",
             "Résumé de l'incident : systèmes devenus inaccessibles, dossiers partagés indisponibles et revendication LockBit.", "JOINT AU COURRIEL"),
            ("E-003", "notes_equipe_it.txt",
             "Notes préliminaires de l'équipe informatique. Les heures et événements doivent être recoupés avec les journaux originaux.", "JOINT AU COURRIEL"),
            ("E-004", "Journaux informatiques",
             "Connexions suspectes évoquées par Sophie Martin. Les fichiers sources restent à examiner dans les outils de l'enquête.", "À ANALYSER"),
            ("E-005", "Signalement de l'employé",
             "Activité inhabituelle observée sur son ordinateur le 3 novembre au soir. Nature et lien éventuel avec l'attaque inconnus.", "À ÉTABLIR"),
            ("E-006", "Message de rançon",
             "Message affiché sur certains ordinateurs. Il revendique une attaque LockBit et menace de publier les données.", "À EXAMINER"),
        )
        for reference, title, description, status in items:
            row = tk.Frame(
                parent, bg=COLORS["surface"], padx=14, pady=10,
                highlightbackground=COLORS["border"], highlightthickness=1,
            )
            row.pack(fill="x", padx=22, pady=3)
            tk.Label(
                row, text=reference, bg=COLORS["surface"], fg=COLORS["accent"],
                font=("Consolas", 10, "bold"), width=8, anchor="nw",
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
                row, text=status, bg=COLORS["surface"], fg=COLORS["green"],
                font=("Segoe UI", 8, "bold"), wraplength=110, justify="right",
            ).pack(side="right", padx=(8, 0))
