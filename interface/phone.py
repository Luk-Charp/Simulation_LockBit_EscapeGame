"""Fenêtre de messagerie vocale affichée au démarrage."""

from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from interface.theme import COLORS, center_window

try:
    import pygame
except ImportError:
    pygame = None


TRANSCRIPT = """Bonjour, ici Sophie Martin, responsable informatique de la société HexaTech Industries.

Je vous contacte parce que nous venons de subir une cyberattaque et que nous ne savons absolument pas comment réagir.

Ce matin, vers 8 heures 45, plusieurs de nos employés ont commencé à signaler des problèmes d'accès à leurs fichiers. Au début, nous avons pensé à une simple panne informatique. Mais quelques minutes plus tard, nos serveurs sont devenus inaccessibles et certains ordinateurs ont affiché un message demandant le paiement d'une rançon.

Le message mentionne un groupe appelé LockBit. Il affirme que nos données ont été chiffrées et menace de les publier si nous ne payons pas.

Nous avons également remarqué que plusieurs dossiers partagés ont disparu ou ne sont plus accessibles. Notre service informatique a tenté de comprendre ce qui se passait, mais nous avons préféré arrêter toute intervention pour éviter d'aggraver la situation.

Nous avons quelques informations qui pourraient vous aider. Un employé nous a signalé une activité inhabituelle sur son ordinateur hier soir. Nous avons également retrouvé plusieurs connexions suspectes dans nos journaux informatiques.

Je ne sais pas si ces événements sont liés, mais je pense qu'il est important que vous les examiniez.

Nous avons besoin de comprendre comment les attaquants sont entrés dans notre réseau, quels systèmes ont été compromis et surtout qui se trouve derrière cette attaque.

Je vous en prie, aidez-nous. Nous avons besoin de réponses rapidement.

Je reste joignable si vous avez besoin d'informations supplémentaires.

Merci."""


class VoicemailWindow:
    """Lecteur audio et transcription du message laissé par Sophie Martin."""

    def __init__(self, parent: tk.Tk) -> None:
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Messagerie vocale — FBI Cyber Division")
        self.window.configure(bg=COLORS["background"])
        self.window.transient(parent)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        center_window(self.window, 900, 720)

        self.audio_path = (
            Path(__file__).resolve().parent.parent
            / "assets" / "audio" / "Sophie_Martin.mp3"
        )
        self.is_playing = False
        self.is_paused = False
        self._build_ui()
        self._load_audio()
        self.window.grab_set()
        self.window.focus_force()

    def _build_ui(self) -> None:
        header = tk.Frame(self.window, bg=COLORS["taskbar"], height=68)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="MESSAGERIE VOCALE",
            bg=COLORS["taskbar"], fg=COLORS["text"],
            font=("Segoe UI", 15, "bold"),
        ).pack(side="left", padx=25, pady=18)
        tk.Label(
            header, text="MESSAGE ENTRANT  •  04 NOV. 2026",
            bg=COLORS["taskbar"], fg=COLORS["muted"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side="right", padx=25)

        body = tk.Frame(self.window, bg=COLORS["background"], padx=28, pady=22)
        body.pack(fill="both", expand=True)

        sender = tk.Frame(
            body, bg=COLORS["surface"], padx=18, pady=14,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        sender.pack(fill="x")
        tk.Label(
            sender, text="Sophie Martin",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")
        tk.Label(
            sender, text="Responsable informatique — HexaTech Industries",
            bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(3, 0))

        player = tk.Frame(body, bg=COLORS["card"], padx=16, pady=14)
        player.pack(fill="x", pady=(16, 14))
        self.status_label = tk.Label(
            player, text="MESSAGE AUDIO",
            bg=COLORS["card"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        )
        self.status_label.pack(anchor="w")
        controls = tk.Frame(player, bg=COLORS["card"])
        controls.pack(fill="x", pady=(9, 0))
        # Frame + Label permettent de contrôler l'apparence sur macOS.
        self.play_button = tk.Frame(
            controls, bg=COLORS["accent_dark"], padx=16, pady=9, cursor="hand2"
        )
        self.play_button.pack(side="left")
        self.play_button_label = tk.Label(
            self.play_button, text="▶  Écouter le message",
            bg=COLORS["accent_dark"], fg=COLORS["text"],
            font=("Segoe UI", 10, "bold"), cursor="hand2",
        )
        self.play_button_label.pack()
        for widget in (self.play_button, self.play_button_label):
            widget.bind("<Button-1>", lambda _event: self.toggle_playback())
            widget.bind("<Enter>", lambda _event: self._set_play_button_color(COLORS["accent"]))
            widget.bind("<Leave>", lambda _event: self._set_play_button_color(COLORS["accent_dark"]))
        self.audio_info = tk.Label(
            controls, text="Durée : environ 1 min 33",
            bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 9),
        )
        self.audio_info.pack(side="left", padx=15)

        tk.Label(
            body, text="TRANSCRIPTION",
            bg=COLORS["background"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(2, 8))

        transcript_frame = tk.Frame(body, bg=COLORS["surface"])
        transcript_frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(transcript_frame)
        scrollbar.pack(side="right", fill="y")
        self.transcript = tk.Text(
            transcript_frame, wrap="word", yscrollcommand=scrollbar.set,
            bg=COLORS["surface"], fg=COLORS["text"],
            insertbackground=COLORS["text"], relief="flat",
            padx=18, pady=15, font=("Segoe UI", 10),
            spacing1=2, spacing3=8, state="normal",
        )
        self.transcript.pack(side="left", fill="both", expand=True)
        scrollbar.configure(command=self.transcript.yview)
        self.transcript.insert("1.0", TRANSCRIPT)
        self.transcript.configure(state="disabled")

        footer = tk.Frame(body, bg=COLORS["background"])
        footer.pack(fill="x", pady=(14, 0))
        tk.Label(
            footer, text="SIMULATION PÉDAGOGIQUE  •  DONNÉES FICTIVES",
            bg=COLORS["background"], fg=COLORS["muted"],
            font=("Segoe UI", 8),
        ).pack(side="left")
        tk.Button(
            footer, text="Fermer", command=self.close,
            bg=COLORS["card"], fg=COLORS["text"],
            activebackground=COLORS["card_hover"],
            relief="flat", padx=18, pady=7, cursor="hand2",
        ).pack(side="right")

    def _load_audio(self) -> None:
        if not self.audio_path.exists():
            self.status_label.configure(text="FICHIER AUDIO INTROUVABLE")
            self._set_play_button_enabled(False)
            self.audio_info.configure(
                text="Placez Sophie_Martin.mp3 dans assets/audio/"
            )
            return

        if pygame is None:
            self.status_label.configure(text="LECTEUR AUDIO NON INSTALLÉ")
            self.play_button.configure(state="disabled")
            self.audio_info.configure(text="Installez les dépendances : pip install -r requirements.txt")
            return

        try:
            pygame.mixer.init()
            pygame.mixer.music.load(str(self.audio_path))
        except Exception as error:
            self.status_label.configure(text="IMPOSSIBLE DE CHARGER LE MESSAGE")
            self.play_button.configure(state="disabled")
            self.audio_info.configure(text=str(error)[:90])

    def _set_play_button_color(self, color: str) -> None:
        self.play_button.configure(bg=color)
        self.play_button_label.configure(bg=color)

    def _set_play_button_enabled(self, enabled: bool) -> None:
        self.play_button.configure(cursor="hand2" if enabled else "arrow")
        self.play_button_label.configure(
            fg=COLORS["text"] if enabled else COLORS["muted"],
            cursor="hand2" if enabled else "arrow",
        )
        if not enabled:
            for widget in (self.play_button, self.play_button_label):
                widget.unbind("<Button-1>")
                widget.unbind("<Enter>")
                widget.unbind("<Leave>")

    def _set_play_button_text(self, text: str) -> None:
        self.play_button_label.configure(text=text)

    def toggle_playback(self) -> None:
        if pygame is None:
            return
        try:
            if self.is_playing:
                pygame.mixer.music.pause()
                self.is_playing = False
                self.is_paused = True
                self._set_play_button_text("▶  Reprendre")
                self.status_label.configure(text="LECTURE EN PAUSE")
            elif self.is_paused:
                pygame.mixer.music.unpause()
                self.is_playing = True
                self.is_paused = False
                self._set_play_button_text("Ⅱ  Mettre en pause")
                self.status_label.configure(text="LECTURE EN COURS")
                self._watch_playback()
            else:
                pygame.mixer.music.play()
                self.is_playing = True
                self.is_paused = False
                self._set_play_button_text("Ⅱ  Mettre en pause")
                self.status_label.configure(text="LECTURE EN COURS")
                self._watch_playback()
        except Exception as error:
            messagebox.showerror("Lecture audio", str(error), parent=self.window)

    def _watch_playback(self) -> None:
        if not self.window.winfo_exists():
            return
        if self.is_paused:
            self.window.after(400, self._watch_playback)
            return
        if pygame is not None and not pygame.mixer.music.get_busy():
            self.is_playing = False
            self.is_paused = False
            self._set_play_button_text("▶  Réécouter le message")
            self.status_label.configure(text="MESSAGE TERMINÉ")
            return
        self.window.after(400, self._watch_playback)

    def close(self) -> None:
        if pygame is not None:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception:
                pass
        self.window.grab_release()
        self.window.destroy()
