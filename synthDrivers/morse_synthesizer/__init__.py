import synthDriverHandler
import tones
import threading
import time

# ===== EINSTELLUNGEN =====
DEFAULT_WPM = 15
DEFAULT_FREQ = 440
DEFAULT_FARNSWORTH = 1.0

def morse_unit(wpm):
    return 1.2 / wpm

MORSE_CODE = {
    # Buchstaben
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    # Zahlen
    '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----',
    # Umlaute
    'Ä': '.-.-',  'Ö': '---.',  'Ü': '..--',
    # Satz-/Sonderzeichen
    '.': '.-.-.-',      ',': '--..--',      ':': '---...',
    '?': '..--..',      "'": '.----.',      '-': '-....-',
    '/': '-..-.',       '(': '-.--.',       ')': '-.--.-',
    '"': '.-..-.',      '=': '-...-',       '+': '.-.-.',
    '@': '.--.-.',      '!': '-.-.--',      ';': '-.-.-.',
    '_': '..--.-',      '$': '...-..-',     '&': '.-...',
    # Prosigns (optional)
    '<SK>': '...-.-',   '<BK>': '-...-.-',  '<SN>': '...-.',
    # Absatz (optional: AR)
    '\n': '.-.-', '\r': '.-.-', '\u2029': '.-.-'
}

class SynthDriver(synthDriverHandler.SynthDriver):
    name = "morse_synthesizer"
    description = "Morsecode-Synthesizer"
    supportedSettings = ()
    _cancel = threading.Event()
    _playThread = None

    wpm = DEFAULT_WPM
    freq = DEFAULT_FREQ
    farnsworth = DEFAULT_FARNSWORTH

    @classmethod
    def check(cls):
        return True

    def speak(self, speechSequence):
        self.cancel()
        self._cancel.clear()
        def run():
            for item in speechSequence:
                if self._cancel.is_set():
                    break
                if isinstance(item, str):
                    self._playMorse(item)
        self._playThread = threading.Thread(target=run, daemon=True)
        self._playThread.start()

    def cancel(self):
        self._cancel.set()
        if self._playThread and self._playThread.is_alive():
            self._playThread.join(timeout=0.1)
        self._playThread = None

    def _playMorse(self, text):
        unit = morse_unit(self.wpm)
        fws = self.farnsworth
        dit = unit
        dah = 3 * unit
        intra_element_gap = unit
        inter_char_gap = 3 * unit * fws
        inter_word_gap = 7 * unit * fws
        freq = self.freq

        text = text.replace('\r\n', '\n').replace('\r', '\n')

        # Zeitstrahl initialisieren
        now = time.monotonic()
        timeline = now

        i = 0
        length = len(text)
        while i < length:
            if self._cancel.is_set():
                break
            char = text[i]
            # Leerzeichen und Absätze: immer EINE Wortpause erzwingen, egal wie viele hintereinander
            if char == ' ' or char in ('\n', '\u2029'):
                # Nur, wenn vorher kein Worttrenner war (sonst mehrfaches Leer ignorieren)
                timeline = self._wait_until(timeline, inter_word_gap)
                # Überspringe alle folgenden Leerzeichen/Absätze!
                while i + 1 < length and (text[i+1] == ' ' or text[i+1] in ('\n', '\u2029')):
                    i += 1
                i += 1
                continue

            code = MORSE_CODE.get(char.upper(), '')
            if not code:
                i += 1
                continue  # Unbekanntes Zeichen überspringen

            # Buchstabe morse
            for j, symbol in enumerate(code):
                if self._cancel.is_set():
                    break
                if symbol == '.':
                    tones.beep(freq, int(dit * 1000))
                    timeline = self._wait_until(timeline, dit)
                elif symbol == '-':
                    tones.beep(freq, int(dah * 1000))
                    timeline = self._wait_until(timeline, dah)
                # Lücke zwischen Morse-Elementen (außer nach letztem)
                if j < len(code) - 1:
                    timeline = self._wait_until(timeline, intra_element_gap)
            # Buchstabenpause, aber nicht nach letztem Zeichen oder vor Worttrenner
            if i + 1 < length and text[i+1] not in (' ', '\n', '\u2029'):
                timeline = self._wait_until(timeline, inter_char_gap)
            i += 1

    def _wait_until(self, timeline, duration):
        target = timeline + duration
        while not self._cancel.is_set():
            now = time.monotonic()
            remaining = target - now
            if remaining <= 0:
                break
            # Schlaf-Intervall sehr klein für maximale Präzision
            time.sleep(min(remaining, 0.003))
        return target