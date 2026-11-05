"""Fenêtre de validation pédagogique des objectifs de l'enquête."""

import tkinter as tk
from interface.theme import COLORS, center_window


class CheckpointWindow:
    """Questionnaire à choix multiples avec correction et validation par score."""

    def __init__(self, parent: tk.Misc, checkpoint: dict, on_pass) -> None:
        self.window = tk.Toplevel(parent)
        self.window.title("FBI Cyber Division — Validation de l'objectif")
        self.window.transient(parent)
        self.window.configure(bg=COLORS["background"])
        center_window(self.window, 820, 700)
        self.checkpoint = checkpoint
        self.on_pass = on_pass
        self.variables = []
        self._build_interface()

    def _build_interface(self) -> None:
        header = tk.Frame(self.window, bg=COLORS["taskbar"], padx=24, pady=18)
        header.pack(fill="x")
        tk.Label(header, text="FBI CYBER DIVISION  /  CHECKPOINT",
                 bg=COLORS["taskbar"], fg=COLORS["gold"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(header, text=self.checkpoint["title"],
                 bg=COLORS["taskbar"], fg=COLORS["on_dark"],
                 font=("Segoe UI", 19, "bold")).pack(anchor="w", pady=(5, 2))
        tk.Label(header, text=self.checkpoint["description"],
                 bg=COLORS["taskbar"], fg=COLORS["on_dark_muted"],
                 font=("Segoe UI", 9), wraplength=740,
                 justify="left").pack(anchor="w")

        info = tk.Frame(self.window, bg=COLORS["card"], padx=18, pady=10)
        info.pack(fill="x", padx=20, pady=(16, 10))
        total = len(self.checkpoint["questions"])
        self.progress_value = tk.Label(
            info, text=f"PROGRESSION  •  0/{total} RÉPONSES",
            bg=COLORS["card"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"),
        )
        self.progress_value.pack(anchor="w")
        self.progress_canvas = tk.Canvas(
            info, height=5, bg=COLORS["border"], highlightthickness=0, bd=0,
        )
        self.progress_canvas.pack(fill="x", pady=(8, 7))
        self.progress_canvas.bind("<Configure>", lambda _event: self._update_progress())
        tk.Label(
            info,
            text=f"{total} QUESTIONS  •  SCORE MINIMUM : {self.checkpoint['pass_score']}/{total}",
            bg=COLORS["card"], fg=COLORS["muted"],
            font=("Segoe UI", 8),
        ).pack(anchor="w")

        outer = tk.Frame(self.window, bg=COLORS["background"])
        outer.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.canvas = tk.Canvas(outer, bg=COLORS["background"], highlightthickness=0)
        scrollbar = tk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        self.questions_frame = tk.Frame(self.canvas, bg=COLORS["background"])
        self.questions_window = self.canvas.create_window((0, 0), window=self.questions_frame, anchor="nw")
        self.questions_frame.bind("<Configure>", lambda _e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.questions_window, width=e.width))
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for number, question in enumerate(self.checkpoint["questions"], start=1):
            self._add_question(number, question)

        footer = tk.Frame(self.window, bg=COLORS["background"], padx=20, pady=12)
        footer.pack(fill="x")
        self.result_label = tk.Label(footer, text="Répondez à toutes les questions pour soumettre votre validation.",
                                     bg=COLORS["background"], fg=COLORS["muted"],
                                     font=("Segoe UI", 9), anchor="w")
        self.result_label.pack(fill="x", pady=(0, 8))
        self.submit_button = tk.Button(footer, text="SOUMETTRE MES RÉPONSES", command=self._submit,
                                       bg=COLORS["accent_dark"], fg=COLORS["button_text"],
                                       activebackground=COLORS["accent"], activeforeground=COLORS["button_text"],
                                       relief="flat", font=("Segoe UI", 9, "bold"),
                                       padx=18, pady=11, cursor="hand2")
        self.submit_button.pack(anchor="e")

    def _add_question(self, number: int, question: dict) -> None:
        card = tk.Frame(self.questions_frame, bg=COLORS["surface"], padx=16, pady=12,
                        highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="x", pady=5)
        tk.Label(card, text=f"QUESTION {number}", bg=COLORS["surface"], fg=COLORS["accent"],
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(card, text=question["question"], bg=COLORS["surface"], fg=COLORS["text"],
                 font=("Segoe UI", 10, "bold"), wraplength=700,
                 justify="left").pack(anchor="w", pady=(4, 7))
        variable = tk.IntVar(value=-1)
        self.variables.append(variable)
        for index, choice in enumerate(question["choices"]):
            tk.Radiobutton(card, text=choice, variable=variable, value=index,
                           bg=COLORS["surface"], fg=COLORS["text"],
                           activebackground=COLORS["surface"], selectcolor=COLORS["card"],
                           font=("Segoe UI", 9), anchor="w", justify="left",
                           wraplength=690, padx=3, pady=3,
                           command=self._update_progress).pack(fill="x", anchor="w")
        question["_feedback_widget"] = tk.Label(card, text="", bg=COLORS["surface"],
                                                fg=COLORS["muted"], font=("Segoe UI", 8),
                                                wraplength=700, justify="left")
        question["_feedback_widget"].pack(anchor="w", pady=(5, 0))

    def _update_progress(self) -> None:
        """Met à jour le repère de progression sans modifier le score requis."""
        answered = sum(variable.get() >= 0 for variable in self.variables)
        total = len(self.variables)
        self.progress_value.configure(text=f"PROGRESSION  •  {answered}/{total} RÉPONSES")
        self.progress_canvas.delete("all")
        width = self.progress_canvas.winfo_width()
        if width > 1 and total:
            self.progress_canvas.create_rectangle(
                0, 0, width * answered / total, 5,
                fill=COLORS["accent"], outline="",
            )

    def _submit(self) -> None:
        if any(variable.get() < 0 for variable in self.variables):
            self.result_label.configure(text="Il manque une réponse : répondez à toutes les questions.", fg="#a13d3d")
            return
        score = sum(v.get() == q["answer"] for v, q in zip(self.variables, self.checkpoint["questions"]))
        total = len(self.variables)
        passed = score >= self.checkpoint["pass_score"]
        for variable, question in zip(self.variables, self.checkpoint["questions"]):
            correct = variable.get() == question["answer"]
            answer = question["choices"][question["answer"]]
            message = ("✓ Bonne réponse. " if correct else f"✗ Réponse attendue : {answer}. ") + question["explanation"]
            question["_feedback_widget"].configure(text=message, fg=COLORS["green"] if correct else "#a13d3d")
        if passed:
            self.result_label.configure(text=f"VALIDATION RÉUSSIE — {score}/{total}. L'objectif est débloqué.", fg=COLORS["green"])
            self.submit_button.configure(text="CONTINUER", command=self._finish, bg=COLORS["green"])
        else:
            self.result_label.configure(text=f"{score}/{total} — Il faut obtenir {self.checkpoint['pass_score']}/{total}. Relisez les explications et réessayez.", fg="#a13d3d")
            self.submit_button.configure(text="RÉESSAYER", command=self._retry)

    def _retry(self) -> None:
        for variable, question in zip(self.variables, self.checkpoint["questions"]):
            variable.set(-1)
            question["_feedback_widget"].configure(text="")
        self.result_label.configure(text="Nouvelle tentative : prenez le temps de relire les documents.", fg=COLORS["muted"])
        self.submit_button.configure(text="SOUMETTRE MES RÉPONSES", command=self._submit)

    def _finish(self) -> None:
        self.on_pass()
        self.window.destroy()
