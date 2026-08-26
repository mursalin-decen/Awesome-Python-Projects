import sys
import time

# ANSI Code for Bold + Bright Yellow
YELLOW_BOLD = "\033[1;\033[93m"
RESET = "\033[0m"


def type_lyrics(text, delay=0.06):
    sys.stdout.write(YELLOW_BOLD)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET + "\n")


def play_song():
    # Format: (Line text, typing speed per char, pause after line)
    lyrics = [
        ("Aisa lagta hai kyun", 0.06, 0.4),
        ("Teri aankhen jaise", 0.05, 0.3),
        ("Aankhon mein meri reh gayi", 0.05, 0.6),
        ("Kabhi pehle maine na suni jo", 0.05, 0.4),
        ("Aisi baatein keh gayi", 0.05, 0.8),
        ("Tu hi tu hai jo har taraf mere", 0.05, 0.5),
        ("Toh tujhse pare main jaaun kahan", 0.05, 0.9),
        ("Mere dil mubarak ho", 0.06, 0.4),
        ("Yahi toh pyar hai", 0.06, 0.7),
        ("Ae mere dil mubarak ho", 0.06, 0.4),
        ("Yahi toh pyar hai", 0.07, 1.2),
    ]

    print(f"\n{YELLOW_BOLD}--- Playing: Ishq Mubarak (for you Shi <3) ---{RESET}\n")
    time.sleep(1)

    for line, speed, pause in lyrics:
        type_lyrics(line, delay=speed)
        time.sleep(pause)


if __name__ == "__main__":
    play_song()