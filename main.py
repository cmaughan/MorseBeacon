from machine import Pin
import time

# ---------------- USER SETTINGS ----------------
GPIO_PIN = 7          # Pico GPIO pin driving key transistor or MOSFET (active-low)
WPM = 12               # Words per minute (12–15 recommended)

# Beacon text (G7LQX @ IO93KX, 800 mW, EFHW 40m)
MSG1 = "VVV VVV VVV"
MSG2 = "DE G7LQX/B G7LQX/B G7LQX/B"
MSG3 = "QTH IO93KX PWR 800MW ANT EFHW 40M"
MSG4 = "DE G7LQX/B"

PAUSE1 = 2   # seconds
PAUSE2 = 2
PAUSE3 = 5
PAUSE4 = 30
# -----------------------------------------------

# Setup GPIO (active low: 0 = key up, 1 = key down)
key = Pin(GPIO_PIN, Pin.OUT)
key.value(0)

# Morse timings (PARIS standard)
DIT = 1.2 / WPM
DAH = 3 * DIT
INTRA = DIT
INTER_CHAR = 3 * DIT
INTER_WORD = 7 * DIT

MORSE = {
    'A': ".-",   'B': "-...", 'C': "-.-.", 'D': "-..",  'E': ".",
    'F': "..-.", 'G': "--.",  'H': "....", 'I': "..",   'J': ".---",
    'K': "-.-",  'L': ".-..", 'M': "--",   'N': "-.",   'O': "---",
    'P': ".--.", 'Q': "--.-", 'R': ".-.",  'S': "...",  'T': "-",
    'U': "..-",  'V': "...-", 'W': ".--",  'X': "-..-", 'Y': "-.--",
    'Z': "--..",
    '0': "-----", '1': ".----", '2': "..---", '3': "...--",
    '4': "....-", '5': ".....", '6': "-....", '7': "--...",
    '8': "---..", '9': "----.",
    '/': "-..-.", '=': "-...-", '?': "..--..", '.': ".-.-.-",
    ',': "--..--", '+': ".-.-.", '-': "-....-", '@': ".--.-."
}

def key_down(): key.value(1)
def key_up():   key.value(0)

def send_element(symbol):
    key_down()
    time.sleep(DIT if symbol == '.' else DAH)
    key_up()
    time.sleep(INTRA)

def send_char(ch):
    if ch == ' ':
        time.sleep(INTER_WORD); return
    pat = MORSE.get(ch.upper())
    if not pat: return
    for s in pat:
        send_element(s)
    time.sleep(INTER_CHAR - INTRA)

def send_string(msg):
    for ch in msg:
        send_char(ch)

time.sleep(2)

# Beacon loop
while True:
    send_string(MSG1); time.sleep(PAUSE1)
    send_string(MSG2); time.sleep(PAUSE2)
    send_string(MSG3); time.sleep(PAUSE3)
    send_string(MSG4); time.sleep(PAUSE4)
