import random

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

# Select language
print("Select Language:")
for code, name in languages.items():
    print(f"{code} - {name}")
lang = input("Language code: ").lower()
if lang not in translations:
    print("Language not supported. Defaulting to English.")
    lang = "en"

def t(key):
    return translations[lang].get(key, key)

print(t("welcome"))

wins = 0
losses = 0
ties = 0

while True:
    try:
        total_rounds = int(input(t("ask_rounds")))
        if total_rounds > 0:
            break
        else:
            print(t("invalid_num"))
    except ValueError:
        print(t("invalid_input"))

round_num = 1

while round_num <= total_rounds:
    print(f"\n{t('round')} {round_num} {t('of')} {total_rounds}")
    print(f"{t('current_score')}: {wins} {t('wins')}, {losses} {t('losses')}, {ties} {t('ties')}")

    while True:
        print(t("choose_move"))
        playermove = input(t("your_move")).upper()
        if playermove in ["R", "P", "S"]:
            break
        else:
            print(t("invalid_move"))

    moves = {"R": "ROCK", "P": "PAPER", "S": "SCISSORS"}
    print(f"{moves[playermove]} {t('versus')}")
    compMove = random.choice(["R", "P", "S"])
    print(moves[compMove])

    if playermove == compMove:
        print(t("tie"))
        ties += 1
    elif (playermove == "R" and compMove == "S") or \
         (playermove == "P" and compMove == "R") or \
         (playermove == "S" and compMove == "P"):
        print(t("you_win"))
        wins += 1
    else:
        print(t("you_lose"))
        losses += 1

    round_num += 1

print(f"\n{t('game_over')}")
print(f"{t('final_score')}: {wins} {t('wins')}, {losses} {t('losses')}, {ties} {t('ties')}")

if wins > losses:
    print(t("overall_win"))
elif losses > wins:
    print(t("overall_lose"))
else:
    print(t("overall_tie"))
