import random
import tkinter as tk
from tkinter import ttk

# Language selection
languages = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "ta": "Tamil",
    "bn": "Bengali"
}

translations = {
    "en": {
        "welcome": "Let's Play ROCK PAPER SCISSORS GAME!",
        "ask_rounds": "How many rounds would you like to play? (e.g., 3, 5): ",
        "invalid_num": "Please enter a positive number.",
        "invalid_input": "Invalid input. Please enter a number.",
        "round": "Round",
        "of": "of",
        "current_score": "Current score",
        "wins": "Wins",
        "losses": "Losses",
        "ties": "Ties",
        "choose_move": "Type 'R' for ROCK, 'P' for PAPER, 'S' for SCISSORS",
        "your_move": "Your move: ",
        "invalid_move": "Invalid input. Try again.",
        "versus": "versus...",
        "tie": "It's a tie!",
        "you_win": "You win this round!",
        "you_lose": "You lose this round!",
        "game_over": "--- GAME OVER ---",
        "final_score": "Final score",
        "overall_win": "🎉 You are the overall winner!",
        "overall_lose": "😢 You lost the game. Better luck next time!",
        "overall_tie": "😐 It's a tie overall!"
    },
    "hi": {
        "welcome": "चलिए ROCK PAPER SCISSORS खेलते हैं!",
        "ask_rounds": "आप कितने राउंड खेलना चाहते हैं? (जैसे 3, 5): ",
        "invalid_num": "कृपया एक सकारात्मक संख्या दर्ज करें।",
        "invalid_input": "अमान्य इनपुट। कृपया एक संख्या दर्ज करें।",
        "round": "राउंड",
        "of": "में से",
        "current_score": "वर्तमान स्कोर",
        "wins": "जीत",
        "losses": "हार",
        "ties": "बराबरी",
        "choose_move": "'R' ROCK के लिए, 'P' PAPER के लिए, 'S' SCISSORS के लिए टाइप करें",
        "your_move": "आपका मूव: ",
        "invalid_move": "अमान्य इनपुट। फिर से प्रयास करें।",
        "versus": "के मुकाबले...",
        "tie": "यह बराबरी है!",
        "you_win": "आपने यह राउंड जीत लिया!",
        "you_lose": "आप यह राउंड हार गए!",
        "game_over": "--- खेल समाप्त ---",
        "final_score": "अंतिम स्कोर",
        "overall_win": "🎉 आप कुल विजेता हैं!",
        "overall_lose": "😢 आप हार गए। अगली बार कोशिश करें!",
        "overall_tie": "😐 यह कुल मिलाकर बराबरी है!"
    },
    "es": {
        "welcome": "¡Juguemos a PIEDRA, PAPEL o TIJERA!",
        "ask_rounds": "¿Cuántas rondas quieres jugar? (por ejemplo, 3, 5): ",
        "invalid_num": "Por favor, introduce un número positivo.",
        "invalid_input": "Entrada no válida. Por favor, introduce un número.",
        "round": "Ronda",
        "of": "de",
        "current_score": "Puntuación actual",
        "wins": "Victorias",
        "losses": "Derrotas",
        "ties": "Empates",
        "choose_move": "Escribe 'R' para PIEDRA, 'P' para PAPEL, 'S' para TIJERA",
        "your_move": "Tu jugada: ",
        "invalid_move": "Entrada no válida. Intenta de nuevo.",
        "versus": "contra...",
        "tie": "¡Es un empate!",
        "you_win": "¡Ganaste esta ronda!",
        "you_lose": "¡Perdiste esta ronda!",
        "game_over": "--- JUEGO TERMINADO ---",
        "final_score": "Puntuación final",
        "overall_win": "🎉 ¡Eres el ganador!",
        "overall_lose": "😢 Perdiste el juego. ¡Buena suerte la próxima vez!",
        "overall_tie": "😐 ¡Es un empate general!"
    },
    "fr": {
        "welcome": "Jouons à PIERRE PAPIER CISEAUX !",
        "ask_rounds": "Combien de manches voulez-vous jouer ? (par exemple, 3, 5) : ",
        "invalid_num": "Veuillez entrer un nombre positif.",
        "invalid_input": "Entrée invalide. Veuillez entrer un nombre.",
        "round": "Manche",
        "of": "sur",
        "current_score": "Score actuel",
        "wins": "Victoires",
        "losses": "Défaites",
        "ties": "Égalités",
        "choose_move": "Tapez 'R' pour PIERRE, 'P' pour PAPIER, 'S' pour CISEAUX",
        "your_move": "Votre choix : ",
        "invalid_move": "Entrée invalide. Réessayez.",
        "versus": "contre...",
        "tie": "Égalité !",
        "you_win": "Vous avez gagné cette manche !",
        "you_lose": "Vous avez perdu cette manche !",
        "game_over": "--- FIN DU JEU ---",
        "final_score": "Score final",
        "overall_win": "🎉 Vous êtes le grand gagnant !",
        "overall_lose": "😢 Vous avez perdu. Bonne chance la prochaine fois !",
        "overall_tie": "😐 Match nul au total !"
    },
    "ta": {
        "welcome": "வாங்க பாறை காகிதம் கத்தரி விளையாடலாம்!",
        "ask_rounds": "நீங்கள் எத்தனை ரவுண்ட்கள் விளையாட விரும்புகிறீர்கள்? (எ.கா. 3, 5): ",
        "invalid_num": "தயவுசெய்து ஒரு நேர்மறை எண்ணை உள்ளிடவும்.",
        "invalid_input": "தவறான உள்ளீடு. தயவுசெய்து எண்ணை உள்ளிடவும்.",
        "round": "ரௌண்டு",
        "of": "இல்",
        "current_score": "தற்போதைய மதிப்பெண்கள்",
        "wins": "வெற்றி",
        "losses": "தோல்வி",
        "ties": "சமம்",
        "choose_move": "'R' கற்க பாறை, 'P' காகிதம், 'S' கத்தரி என்று டைப் செய்யவும்",
        "your_move": "உங்கள் தேர்வு: ",
        "invalid_move": "தவறான தேர்வு. மீண்டும் முயற்சிக்கவும்.",
        "versus": "எதிராக...",
        "tie": "இது சமம்!",
        "you_win": "இந்த ரௌண்ட் நீங்கள் வென்றீர்கள்!",
        "you_lose": "இந்த ரௌண்ட் நீங்கள் தோற்றீர்கள்!",
        "game_over": "--- விளையாட்டு முடிந்தது ---",
        "final_score": "இறுதி மதிப்பெண்கள்",
        "overall_win": "🎉 நீங்கள் முழு வெற்றியாளராக உள்ளீர்கள்!",
        "overall_lose": "😢 நீங்கள் தோற்றுவிட்டீர்கள். அடுத்த முறை சிறப்பாக செய்யலாம்!",
        "overall_tie": "😐 இது ஒரு சம விளையாட்டு!"
    },
    "bn": {
        "welcome": "চলো ROCK PAPER SCISSORS খেলি!",
        "ask_rounds": "আপনি কত রাউন্ড খেলতে চান? (যেমন, ৩, ৫): ",
        "invalid_num": "দয়া করে একটি ধনাত্মক সংখ্যা লিখুন।",
        "invalid_input": "ভুল ইনপুট। একটি সংখ্যা লিখুন।",
        "round": "রাউন্ড",
        "of": "এর মধ্যে",
        "current_score": "বর্তমান স্কোর",
        "wins": "জয়",
        "losses": "পরাজয়",
        "ties": "সমতা",
        "choose_move": "'R' ROCK এর জন্য, 'P' PAPER, 'S' SCISSORS এর জন্য টাইপ করুন",
        "your_move": "আপনার চাল: ",
        "invalid_move": "ভুল ইনপুট। আবার চেষ্টা করুন।",
        "versus": "বনাম...",
        "tie": "এটি একটি সমতা!",
        "you_win": "আপনি এই রাউন্ড জিতেছেন!",
        "you_lose": "আপনি এই রাউন্ড হেরেছেন!",
        "game_over": "--- খেলা শেষ ---",
        "final_score": "চূড়ান্ত স্কোর",
        "overall_win": "🎉 আপনি জয়ী!",
        "overall_lose": "😢 আপনি হেরেছেন। আবার চেষ্টা করুন!",
        "overall_tie": "😐 এটি একটি সমতা!"
    }
}
class RPSGUI:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.total_rounds = 0
        self.current_round = 0
        self.game_active = False

        self.build_gui()

    def t(self, key):
        return translations[self.lang].get(key, key)

    def build_gui(self):
        self.root.title("Rock Paper Scissors")

        # Language Selection
        lang_frame = tk.Frame(self.root)
        lang_frame.pack(pady=5)

        tk.Label(lang_frame, text="Language:").pack(side="left")
        self.lang_menu = ttk.Combobox(lang_frame, values=list(languages.values()))
        self.lang_menu.current(0)
        self.lang_menu.pack(side="left")
        self.lang_menu.bind("<<ComboboxSelected>>", self.set_language)

        # Round Input
        round_frame = tk.Frame(self.root)
        round_frame.pack(pady=5)

        tk.Label(round_frame, text="Number of Rounds:").pack(side="left")
        self.round_entry = tk.Entry(round_frame, width=5)
        self.round_entry.pack(side="left")

        # Start Button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.pack(pady=5)

        # Title
        self.title_label = tk.Label(self.root, text=self.t("welcome"), font=("Helvetica", 14))
        self.title_label.pack(pady=10)

        # Move buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        self.move_label = tk.Label(self.root, text=self.t("choose_move"))
        self.move_label.pack()

        tk.Button(btn_frame, text="🪨 Rock", command=lambda: self.play("R")).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="📄 Paper", command=lambda: self.play("P")).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="✂️ Scissors", command=lambda: self.play("S")).grid(row=0, column=2, padx=10)

        # Result
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        # Score
        self.score_label = tk.Label(self.root, text="")
        self.score_label.pack()

        self.update_score()

        # Reset Button
        tk.Button(self.root, text="Reset", command=self.reset_game).pack(pady=5)

    def set_language(self, event):
        selected_name = self.lang_menu.get()
        self.lang = next(code for code, name in languages.items() if name == selected_name)
        self.refresh_labels()

    def refresh_labels(self):
        self.root.title("Rock Paper Scissors")
        self.title_label.config(text=self.t("welcome"))
        self.move_label.config(text=self.t("choose_move"))
        self.update_score()
        self.start_button.config(text=self.t("start") if "start" in translations[self.lang] else "Start")

    def play(self, player_move):
        if not self.game_active:
            self.result_label.config(text="Click 'Start Game' first.")
            return

        comp_move = random.choice(["R", "P", "S"])

        if player_move == comp_move:
            self.ties += 1
            outcome = self.t("tie")
        elif (player_move == "R" and comp_move == "S") or \
             (player_move == "P" and comp_move == "R") or \
             (player_move == "S" and comp_move == "P"):
            self.wins += 1
            outcome = self.t("you_win")
        else:
            self.losses += 1
            outcome = self.t("you_lose")

        self.update_score()

        if self.current_round >= self.total_rounds:
            final_message = f"{self.t('game_over')}\n{self.t('final_score')}: {self.wins}W {self.losses}L {self.ties}T\n"

            if self.wins > self.losses:
                final_message += self.t("overall_win")
            elif self.losses > self.wins:
                final_message += self.t("overall_lose")
            else:
                final_message += self.t("overall_tie")

            self.result_label.config(text=final_message)
            self.game_active = False


        else:
            self.current_round += 1
            self.result_label.config(
                text=f"{outcome} (Round {self.current_round}/{self.total_rounds})"
            )

    def update_score(self):
        self.score_label.config(
            text=f"{self.t('wins')}: {self.wins} | {self.t('losses')}: {self.losses} | {self.t('ties')}: {self.ties}"
        )

    def reset_game(self):
        self.wins = self.losses = self.ties = 0
        self.current_round = 0
        self.total_rounds = 0
        self.round_entry.delete(0, tk.END)
        self.game_active = False
        self.result_label.config(text="")
        self.update_score()

    def start_game(self):
        try:
            self.total_rounds = int(self.round_entry.get())
            if self.total_rounds <= 0:
                raise ValueError
        except ValueError:
            self.result_label.config(text=self.t("invalid_num"))
            return

        self.wins = self.losses = self.ties = 0
        self.current_round = 1
        self.game_active = True
        self.result_label.config(
            text=f"{self.t('choose_move')} (Round {self.current_round}/{self.total_rounds})"
        )
        self.update_score()






if __name__ == "__main__":
    root = tk.Tk()
    app = RPSGUI(root)
    root.mainloop()
