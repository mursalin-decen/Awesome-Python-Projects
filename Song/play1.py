import sys
import time

# ANSI Code for Bold + Yellow
YELLOW_BOLD = "\033[1;33m"
RESET = "\033[0m"


def type_lyrics(text, delay=0.14):
    sys.stdout.write(YELLOW_BOLD)

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

    sys.stdout.write(RESET + "\n")


def play_song():
    # Format: (Text, typing speed, pause after line)
    lyrics = [
        ("Aisa lagta hai kyun", 0.16, 1.2),
        ("Teri aankhen jaise", 0.15, 1.0),
        ("Aankhon mein meri reh gayi", 0.15, 1.8),

        ("Kabhi pehle maine na suni jo", 0.14, 1.3),
        ("Aisi baatein keh gayi", 0.15, 2.0),

        ("Tu hi tu hai jo har taraf mere", 0.14, 1.5),
        ("Toh tujhse pare main jaaun kahan", 0.14, 2.2),

        ("Mere dil mubarak ho", 0.16, 1.3),
        ("Yahi toh pyar hai", 0.16, 1.8),

        ("Ae mere dil mubarak ho", 0.16, 1.3),
        ("Yahi toh pyar hai", 0.18, 3.0),
    ]

    print(f"\n{YELLOW_BOLD}--- Playing: Dil Mubarak for you SHi<<3 ---{RESET}\n")
    time.sleep(2)

    for line, speed, pause in lyrics:
        type_lyrics(line, delay=speed)
        time.sleep(pause)


if __name__ == "__main__":
    play_song()