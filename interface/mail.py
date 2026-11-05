"""Messagerie simulée contenant les premiers éléments de l'enquête."""

import tkinter as tk

from interface.theme import COLORS


class MailWindow:
    """Fenêtre de messagerie avec messages et pièces jointes fictifs."""

    def __init__(self, parent: tk.Misc) -> None:
        self.window = tk.Toplevel(parent)
        self.window.title("Messagerie — Poste d'investigation")
        self.window.geometry("1080x680")
        self.window.minsize(850, 560)
        self.window.configure(bg=COLORS["background"])
        self._build_interface()

    def _build_interface(self) -> None:
        header = tk.Frame(self.window, bg=COLORS["taskbar"], height=54)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text="✉  MESSAGERIE", bg=COLORS["taskbar"],
            fg=COLORS["text"], font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=20)
        tk.Label(
            header, text="Boîte de réception  •  Compte sécurisé",
            bg=COLORS["taskbar"], fg=COLORS["muted"], font=("Segoe UI", 9)
        ).pack(side="right", padx=20)

        body = tk.Frame(self.window, bg=COLORS["background"])
        body.pack(fill="both", expand=True, padx=18, pady=18)

        sidebar = tk.Frame(body, bg=COLORS["card"], width=185)
        sidebar.pack(side="left", fill="y", padx=(0, 14))
        sidebar.pack_propagate(False)
        tk.Label(
            sidebar, text="DOSSIERS", bg=COLORS["card"],
            fg=COLORS["muted"], font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=16, pady=(18, 12))
        for folder in ("Boîte de réception  (3)", "Messages envoyés", "Archives"):
            tk.Label(
                sidebar, text=folder, bg=COLORS["card"], fg=COLORS["text"],
                font=("Segoe UI", 9), anchor="w"
            ).pack(fill="x", padx=16, pady=7)

        messages = tk.Frame(body, bg=COLORS["card"], width=265)
        messages.pack(side="left", fill="y", padx=(0, 14))
        messages.pack_propagate(False)
        tk.Label(
            messages, text="MESSAGES RÉCENTS", bg=COLORS["card"],
            fg=COLORS["muted"], font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=14, pady=(18, 12))
        for subject, sender, date, urgent in (
            ("URGENT — Attaque informatique", "Sophie Martin · HexaTech Industries", "Aujourd'hui · 09:14", True),
            ("Disponibilité de l'équipe IT", "Marc Dubois · HexaTech Industries", "Hier · 16:42", False),
            ("Contrat de maintenance", "Support informatique", "Hier · 10:05", False),
        ):
            bg = COLORS["card_hover"] if urgent else COLORS["card"]
            item = tk.Frame(messages, bg=bg, highlightbackground=COLORS["border"], highlightthickness=1, padx=10, pady=12)
            item.pack(fill="x", padx=8, pady=4)
            tk.Label(item, text=subject, bg=bg, fg=COLORS["text"], font=("Segoe UI", 9, "bold"), wraplength=225, justify="left").pack(anchor="w")
            tk.Label(item, text=sender, bg=bg, fg=COLORS["muted"], font=("Segoe UI", 8), wraplength=225, justify="left").pack(anchor="w", pady=(5, 2))
            tk.Label(item, text=date, bg=bg, fg=COLORS["accent"] if urgent else COLORS["muted"], font=("Segoe UI", 8)).pack(anchor="w")

        reading = tk.Frame(body, bg=COLORS["surface"], highlightbackground=COLORS["border"], highlightthickness=1)
        reading.pack(side="left", fill="both", expand=True)
        tk.Label(
            reading, text="URGENT — Attaque informatique",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 17, "bold"), wraplength=520, justify="left"
        ).pack(anchor="w", padx=22, pady=(22, 8))
        details = (
            "De : Sophie Martin <s.martin@hexatech.example>\n"
            "À : FBI Cyber Division\n"
            "Date : 4 novembre 2026, 09:14\n"
            "Entreprise : HexaTech Industries (France)"
        )
        tk.Label(
            reading, text=details, bg=COLORS["surface"],
            fg=COLORS["muted"], font=("Segoe UI", 9), justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 18))

        message = (
            "Bonjour,\n\n"
            "Notre entreprise est victime d'une attaque informatique depuis cette nuit. "
            "Plusieurs serveurs sont devenus inaccessibles et de nombreux fichiers portent "
            "désormais une extension inhabituelle. Un message affiché sur les postes "
            "réclame une rançon et mentionne le groupe LockBit.\n\n"
            "Nos équipes ont isolé une partie du réseau, mais nous ne savons pas encore "
            "comment les attaquants sont entrés ni quelles données ont été consultées. "
            "Nous vous transmettons les premiers éléments dont nous disposons.\n\n"
            "Pouvez-vous nous aider à comprendre ce qui s'est passé et à préserver les "
            "preuves utiles à l'enquête ?\n\n"
            "Cordialement,\nSophie Martin\nResponsable informatique — HexaTech Industries"
        )
        tk.Label(
            reading, text=message, bg=COLORS["surface"],
            fg=COLORS["text"], font=("Segoe UI", 10),
            justify="left", anchor="nw", wraplength=590
        ).pack(fill="x", padx=22)

        tk.Label(
            reading, text="PIÈCES JOINTES", bg=COLORS["surface"],
            fg=COLORS["accent"], font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=22, pady=(22, 8))
        attachments = tk.Frame(reading, bg=COLORS["surface"])
        attachments.pack(anchor="w", padx=18)
        self._attachment_button(
            attachments, "rapport_incident.txt", "Rapport d'incident — HexaTech Industries",
            "Date du signalement : 4 novembre 2026\nDébut estimé : entre 01:00 et 03:00\n"
            "Systèmes touchés : serveur de fichiers et deux serveurs applicatifs\n"
            "Symptômes : fichiers renommés, accès aux partages impossible, message de rançon "
            "affiché sur plusieurs postes.\nHypothèse initiale : attaque par rançongiciel. "
            "L'origine de l'intrusion n'est pas encore déterminée."
        )
        self._attachment_button(
            attachments, "notes_equipe_it.txt", "Notes de l'équipe informatique",
            "02:18 — Première alerte remontée par un utilisateur.\n"
            "02:31 — Le serveur de fichiers ne répond plus.\n"
            "02:46 — Plusieurs postes affichent le même message de rançon.\n"
            "03:05 — Début de l'isolation de certains équipements.\n"
            "08:40 — Les équipes constatent que les sauvegardes en ligne ne sont plus accessibles.\n\n"
            "Attention : ces horaires sont des heures de détection, pas nécessairement celles du début de l'intrusion."
        )
        tk.Label(
            reading, text="Simulation pédagogique : entreprise, adresses et documents fictifs.",
            bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8, "italic")
        ).pack(side="bottom", anchor="w", padx=22, pady=16)

    def _attachment_button(self, parent: tk.Frame, label: str, title: str, content: str) -> None:
        tk.Button(
            parent, text="📄  " + label,
            command=lambda: self._show_attachment(title, content),
            bg=COLORS["card"], fg=COLORS["text"],
            activebackground=COLORS["card_hover"], activeforeground=COLORS["text"],
            relief="flat", padx=12, pady=9, cursor="hand2"
        ).pack(side="left", padx=4)

    def _show_attachment(self, title: str, content: str) -> None:
        window = tk.Toplevel(self.window)
        window.title(title)
        window.geometry("620x390")
        window.configure(bg=COLORS["background"])
        tk.Label(
            window, text=title, bg=COLORS["background"],
            fg=COLORS["text"], font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=18, pady=(18, 10))
        text_area = tk.Text(
            window, wrap="word", bg=COLORS["surface"],
            fg=COLORS["text"], insertbackground=COLORS["text"],
            relief="flat", padx=14, pady=14, font=("Consolas", 10)
        )
        text_area.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        text_area.insert("1.0", content)
        text_area.configure(state="disabled")
