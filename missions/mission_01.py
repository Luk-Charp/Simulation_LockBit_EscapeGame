"""Questions du checkpoint 1 — Comprendre l'incident."""

CHECKPOINT = {
    "title": "Comprendre l'incident",
    "description": "Vérifiez votre compréhension du signalement initial de HexaTech Industries.",
    "pass_score": 3,
    "questions": [
        {"question": "Quel type d'attaque les premiers éléments laissent-ils suspecter ?", "choices": ["Une attaque par rançongiciel (ransomware)", "Une panne matérielle générale", "Une attaque physique contre les locaux", "Une simple erreur de configuration"], "answer": 0, "explanation": "Les fichiers deviennent inaccessibles et un message demande une rançon : ce sont des signes caractéristiques d'un rançongiciel."},
        {"question": "Que réclame le message affiché sur certains ordinateurs ?", "choices": ["L'installation d'un nouvel antivirus", "Le paiement d'une rançon", "Le changement des mots de passe", "La suppression des sauvegardes"], "answer": 1, "explanation": "Sophie Martin indique que certains ordinateurs affichent un message demandant le paiement d'une rançon."},
        {"question": "À quel moment les premiers problèmes d'accès aux fichiers sont-ils signalés ?", "choices": ["Le 3 novembre au matin", "Le 4 novembre vers 08:45", "Le 4 novembre à 09:30", "Le 5 novembre à minuit"], "answer": 1, "explanation": "Sophie Martin situe les premiers problèmes vers 08:45 le 4 novembre."},
        {"question": "La mention « LockBit » dans le message de rançon prouve-t-elle à elle seule l'identité des attaquants ?", "choices": ["Oui, le nom affiché suffit à identifier le groupe", "Oui, car le message vient des ordinateurs infectés", "Non, cette revendication doit être vérifiée et recoupée", "Non, car un rançongiciel ne peut pas afficher de nom"], "answer": 2, "explanation": "Un message peut revendiquer le nom d'un groupe sans prouver qui est réellement derrière l'attaque. Il faut croiser les indices."},
    ],
}
