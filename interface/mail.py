"""Messagerie simulée avec une présentation inspirée d'Outlook."""

import tkinter as tk

from interface.theme import COLORS, center_window


class MailWindow:
    """Fenêtre de messagerie avec deux messages d'enquête fictifs."""

    def __init__(self, parent: tk.Misc) -> None:
        self.window = tk.Toplevel(parent)
        self.window.title("Messagerie — Poste d'investigation")
        self.window.transient(parent)
        self.window.configure(bg=COLORS["background"])
        center_window(self.window, 1160, 780)
        self.message_items = []
        self._build_interface()

    def _build_interface(self) -> None:
        header = tk.Frame(self.window, bg=COLORS["taskbar"], height=54)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text="✉  MESSAGERIE",
            bg=COLORS["taskbar"], fg=COLORS["on_dark"],
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left", padx=20)
        tk.Label(
            header, text="Boîte de réception  •  Compte sécurisé",
            bg=COLORS["taskbar"], fg=COLORS["on_dark_muted"],
            font=("Segoe UI", 9),
        ).pack(side="right", padx=20)

        body = tk.Frame(self.window, bg=COLORS["background"])
        body.pack(fill="both", expand=True, padx=18, pady=18)

        sidebar = tk.Frame(body, bg=COLORS["card"], width=185)
        sidebar.pack(side="left", fill="y", padx=(0, 14))
        sidebar.pack_propagate(False)
        tk.Label(
            sidebar, text="DOSSIERS", bg=COLORS["card"],
            fg=COLORS["muted"], font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=16, pady=(18, 12))
        for folder in ("Boîte de réception  (2)", "Messages envoyés", "Archives"):
            tk.Label(
                sidebar, text=folder, bg=COLORS["card"], fg=COLORS["text"],
                font=("Segoe UI", 9), anchor="w",
            ).pack(fill="x", padx=16, pady=7)

        messages = tk.Frame(body, bg=COLORS["card"], width=265)
        messages.pack(side="left", fill="y", padx=(0, 14))
        messages.pack_propagate(False)
        tk.Label(
            messages, text="MESSAGES RÉCENTS", bg=COLORS["card"],
            fg=COLORS["muted"], font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=14, pady=(18, 12))

        self._add_message_card(
            messages, "URGENT — Attaque informatique",
            "Sophie Martin · HexaTech Industries", "Aujourd'hui · 09:14",
            "victim", selected=True,
        )
        self._add_message_card(
            messages, "Consignes de mission — Opération Lockdown",
            "Agent spécial Thomas Reed · FBI Cyber Division", "Aujourd'hui · 09:30",
            "supervisor",
        )

        self.reading = tk.Frame(
            body, bg=COLORS["surface"],
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        self.reading.pack(side="left", fill="both", expand=True)
        self._render_message("victim")

    def _add_message_card(
        self, parent: tk.Frame, subject: str, sender: str,
        date: str, message_id: str, selected: bool = False,
    ) -> None:
        bg = COLORS["card_hover"] if selected else COLORS["card"]
        card = tk.Frame(
            parent, bg=bg,
            highlightbackground=COLORS["accent"] if selected else COLORS["border"],
            highlightthickness=1, padx=10, pady=12, cursor="hand2",
        )
        card.pack(fill="x", padx=8, pady=4)
        title = tk.Label(
            card, text=subject, bg=bg, fg=COLORS["text"],
            font=("Segoe UI", 9, "bold"), wraplength=225,
            justify="left", cursor="hand2",
        )
        title.pack(anchor="w")
        sender_label = tk.Label(
            card, text=sender, bg=bg, fg=COLORS["muted"],
            font=("Segoe UI", 8), wraplength=225,
            justify="left", cursor="hand2",
        )
        sender_label.pack(anchor="w", pady=(5, 2))
        date_label = tk.Label(
            card, text=date, bg=bg, fg=COLORS["accent"],
            font=("Segoe UI", 8), cursor="hand2",
        )
        date_label.pack(anchor="w")
        self.message_items.append((message_id, card, title, sender_label, date_label))
        for widget in (card, title, sender_label, date_label):
            widget.bind("<Button-1>", lambda _event, mid=message_id: self._select_message(mid))

    def _select_message(self, message_id: str) -> None:
        for mid, card, title, sender, date in self.message_items:
            bg = COLORS["card_hover"] if mid == message_id else COLORS["card"]
            card.configure(
                bg=bg,
                highlightbackground=COLORS["accent"] if mid == message_id else COLORS["border"],
            )
            for widget in (title, sender, date):
                widget.configure(bg=bg)
        self._render_message(message_id)

    def _render_message(self, message_id: str) -> None:
        for child in self.reading.winfo_children():
            child.destroy()

        if message_id == "victim":
            subject = "URGENT — Attaque informatique"
            sender = "Sophie Martin <s.martin@hexatech.com>"
            recipient = "FBI Cyber Division <thomas.reed@fbi-cyber.com>"
            date = "Mercredi 4 novembre 2026 à 09:14"
            body = (
                "Bonjour, ici Sophie Martin, responsable informatique de la société HexaTech Industries.\n\n"
                "Je vous contacte parce que nous venons de subir une cyberattaque et que nous ne savons absolument pas comment réagir.\n\n"
                "Ce matin, vers 8 heures 45, plusieurs de nos employés ont commencé à signaler des problèmes d'accès à leurs fichiers. Au début, nous avons pensé à une simple panne informatique. Mais quelques minutes plus tard, nos serveurs sont devenus inaccessibles et certains ordinateurs ont affiché un message demandant le paiement d'une rançon.\n\n"
                "Le message mentionne un groupe appelé LockBit. Il affirme que nos données ont été chiffrées et menace de les publier si nous ne payons pas.\n\n"
                "Nous avons également remarqué que plusieurs dossiers partagés ont disparu ou ne sont plus accessibles. Notre service informatique a tenté de comprendre ce qui se passait, mais nous avons préféré arrêter toute intervention pour éviter d'aggraver la situation.\n\n"
                "Nous avons quelques informations qui pourraient vous aider. Un employé nous a signalé une activité inhabituelle sur son ordinateur hier soir. Nous avons également retrouvé plusieurs connexions suspectes dans nos journaux informatiques.\n\n"
                "Je ne sais pas si ces événements sont liés, mais je pense qu'il est important que vous les examiniez.\n\n"
                "Nous avons besoin de comprendre comment les attaquants sont entrés dans notre réseau, quels systèmes ont été compromis et surtout qui se trouve derrière cette attaque.\n\n"
                "Je vous en prie, aidez-nous. Nous avons besoin de réponses rapidement.\n\n"
                "Merci.\n\n"
                "Sophie Martin\nResponsable informatique\nHexaTech Industries"
            )
        else:
            subject = "Consignes de mission — Opération Lockdown"
            sender = "Agent spécial Thomas Reed <thomas.reed@fbi-cyber.com>"
            recipient = "Cellule d'investigation numérique <cellule@fbi-cyber.com>"
            date = "Mercredi 4 novembre 2026 à 09:30"
            body = (
                "Bonjour,\n\n"
                "Vous êtes officiellement affectés à l'enquête concernant la cyberattaque subie par HexaTech Industries. Le nom LockBit apparaît dans le message laissé aux employés, mais cette revendication doit être vérifiée.\n\n"
                "Votre mission est de reconstituer le déroulement de l'incident, d'analyser les traces disponibles et de présenter des conclusions appuyées par des preuves. Vous disposez d'environ 45 minutes. Suivez les cinq étapes ci-dessous.\n\n"
                "1. EXAMINER L'INCIDENT\n"
                "Consultez le dossier d'enquête, le signalement et les pièces jointes. Identifiez les faits connus, les horaires et les systèmes touchés.\n\n"
                "2. RECONSTITUER L'INTRUSION\n"
                "Analysez les journaux informatiques. Repérez les connexions inhabituelles, les événements suspects et leur chronologie. Cherchez comment les attaquants ont pu accéder au réseau.\n\n"
                "3. ÉTUDIER L'INFRASTRUCTURE\n"
                "Examinez les adresses IP, les noms de domaine et les indices techniques. Utilisez les outils OSINT et la carte. Une adresse IP ne suffit pas à identifier une personne.\n\n"
                "4. CROISER LES INDICES\n"
                "Comparez vos découvertes avec les informations disponibles sur LockBit. Distinguez les faits vérifiés, les hypothèses et les éléments inconnus.\n\n"
                "5. RÉDIGER LE RAPPORT\n"
                "Présentez le scénario le plus probable, les preuves qui le soutiennent, les infrastructures repérées et les limites de votre analyse.\n\n"
                "RÈGLES : vous travaillez sur une simulation. Ne modifiez pas les preuves et n'effectuez aucune action sur un système réel. Recoupez les informations et ne formulez aucune accusation sans preuves suffisantes.\n\n"
                "Bonne enquête,\nAgent spécial Thomas Reed\nFBI Cyber Division"
            )

        # En-tête de courriel structuré comme dans un client de messagerie classique.
        top = tk.Frame(self.reading, bg=COLORS["surface"])
        top.pack(fill="x", padx=22, pady=(20, 8))
        tk.Label(
            top, text=subject, bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 16, "bold"), wraplength=510, justify="left",
        ).pack(anchor="w", pady=(0, 14))

        metadata = tk.Frame(
            top, bg=COLORS["card"], padx=14, pady=12,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        metadata.pack(fill="x")
        self._metadata_row(metadata, "De", sender)
        self._metadata_row(metadata, "À", recipient)
        self._metadata_row(metadata, "Date", date)
        self._metadata_row(metadata, "Objet", subject)

        separator = tk.Frame(self.reading, bg=COLORS["border"], height=1)
        separator.pack(fill="x", padx=22, pady=(8, 12))

        content_frame = tk.Frame(self.reading, bg=COLORS["surface"])
        content_frame.pack(fill="both", expand=True, padx=22, pady=(0, 8))
        scrollbar = tk.Scrollbar(content_frame)
        scrollbar.pack(side="right", fill="y")
        text_area = tk.Text(
            content_frame, wrap="word", yscrollcommand=scrollbar.set,
            bg=COLORS["surface"], fg=COLORS["text"],
            insertbackground=COLORS["text"], relief="flat",
            highlightthickness=0, borderwidth=0, takefocus=0,
            padx=2, pady=4, font=("Segoe UI", 10),
            spacing1=1, spacing3=8, state="normal",
        )
        text_area.pack(side="left", fill="both", expand=True)
        scrollbar.configure(command=text_area.yview)
        text_area.insert("1.0", body)
        text_area.configure(state="disabled")

        if message_id == "victim":
            attachments = tk.Frame(self.reading, bg=COLORS["surface"])
            attachments.pack(fill="x", padx=18, pady=(0, 12))
            tk.Label(
                attachments, text="PIÈCES JOINTES",
                bg=COLORS["surface"], fg=COLORS["accent"],
                font=("Segoe UI", 9, "bold"),
            ).pack(anchor="w", padx=4, pady=(0, 7))
            row = tk.Frame(attachments, bg=COLORS["surface"])
            row.pack(anchor="w")
            self._attachment_button(
                row, "rapport_incident.txt", "Rapport d'incident — HexaTech Industries",
                "Date du signalement : 4 novembre 2026\nDébut estimé : entre 01:00 et 03:00\n"
                "Systèmes touchés : serveur de fichiers et deux serveurs applicatifs\n"
                "Symptômes : fichiers renommés, accès aux partages impossible, message de rançon affiché sur plusieurs postes.\n"
                "Hypothèse initiale : attaque par rançongiciel. L'origine de l'intrusion n'est pas encore déterminée.",
            )
            self._attachment_button(
                row, "notes_equipe_it.txt", "Notes de l'équipe informatique",
                "02:18 — Première alerte remontée par un utilisateur.\n"
                "02:31 — Le serveur de fichiers ne répond plus.\n"
                "02:46 — Plusieurs postes affichent le même message de rançon.\n"
                "03:05 — Début de l'isolation de certains équipements.\n"
                "08:40 — Les équipes constatent que les sauvegardes en ligne ne sont plus accessibles.\n\n"
                "Attention : ces horaires sont des heures de détection, pas nécessairement celles du début de l'intrusion.",
            )

        tk.Label(
            self.reading,
            text="Simulation pédagogique : entreprise, adresses et documents fictifs.",
            bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8, "italic"),
        ).pack(side="bottom", anchor="w", padx=22, pady=(0, 12))

    def _metadata_row(self, parent: tk.Frame, label: str, value: str) -> None:
        row = tk.Frame(parent, bg=COLORS["card"])
        row.pack(fill="x", pady=2)
        tk.Label(
            row, text=f"{label} :", width=8, anchor="w",
            bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")
        tk.Label(
            row, text=value, anchor="w", justify="left",
            bg=COLORS["card"], fg=COLORS["text"],
            font=("Segoe UI", 9), wraplength=480,
        ).pack(side="left", fill="x", expand=True)

    def _attachment_button(self, parent: tk.Frame, label: str, title: str, content: str) -> None:
        button = tk.Frame(
            parent, bg=COLORS["card"], padx=12, pady=9,
            highlightbackground=COLORS["border"], highlightthickness=1,
            cursor="hand2",
        )
        button.pack(side="left", padx=4)
        caption = tk.Label(
            button, text="📄  " + label, bg=COLORS["card"],
            fg=COLORS["text"], font=("Segoe UI", 9), cursor="hand2",
        )
        caption.pack()
        for widget in (button, caption):
            widget.bind("<Button-1>", lambda _event, t=title, body=content: self._show_attachment(t, body))
            widget.bind(
                "<Enter>",
                lambda _event, frame=button, text=caption: (
                    frame.configure(bg=COLORS["card_hover"]),
                    text.configure(bg=COLORS["card_hover"]),
                ),
            )
            widget.bind(
                "<Leave>",
                lambda _event, frame=button, text=caption: (
                    frame.configure(bg=COLORS["card"]),
                    text.configure(bg=COLORS["card"]),
                ),
            )

    def _show_attachment(self, title: str, content: str) -> None:
        window = tk.Toplevel(self.window)
        window.title(title)
        window.configure(bg=COLORS["background"])
        center_window(window, 620, 390)
        tk.Label(
            window, text=title, bg=COLORS["background"],
            fg=COLORS["text"], font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 10))
        text_area = tk.Text(
            window, wrap="word", bg=COLORS["surface"],
            fg=COLORS["text"], insertbackground=COLORS["text"],
            relief="flat", highlightthickness=0, borderwidth=0, takefocus=0,
            padx=14, pady=14, font=("Consolas", 10),
        )
        text_area.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        text_area.insert("1.0", content)
        text_area.configure(state="disabled")
