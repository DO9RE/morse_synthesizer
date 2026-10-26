import synthDriverHandler
from synthDriverHandler import synthDoneSpeaking
import addonHandler
import tones
import threading
import time
import config
from speech.commands import IndexCommand

addonHandler.initTranslation()

# Register config spec so defaults are guaranteed even when loaded before the global plugin
confspec = {
    "wpm": "integer(default=15, min=5, max=60)",
    "freq": "integer(default=440, min=200, max=2000)",
    "farnsworth": "float(default=1.0, min=0.5, max=3.0)",
    "volume": "integer(default=100, min=0, max=100)",
}
config.conf.spec["morseSynth"] = confspec

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
    description = _("Morse code synthesizer")
    supportedSettings = (
        synthDriverHandler.SynthDriver.RateSetting(),
        synthDriverHandler.SynthDriver.PitchSetting(),
        synthDriverHandler.SynthDriver.VolumeSetting(),
    )
    supportedCommands = frozenset({IndexCommand})
    supportedNotifications = {synthDriverHandler.synthIndexReached, synthDoneSpeaking}
    _cancel = threading.Event()
    _playThread = None

    @classmethod
    def check(cls):
        return True

    # Ring values (0-100) are mapped onto the add-on configuration
    def _get_rate(self):
        return round((config.conf["morseSynth"]["wpm"] - 5) * 100 / 55)

    def _set_rate(self, value):
        config.conf["morseSynth"]["wpm"] = 5 + round(value * 55 / 100)

    def _get_pitch(self):
        return round((config.conf["morseSynth"]["freq"] - 200) * 100 / 1800)

    def _set_pitch(self, value):
        config.conf["morseSynth"]["freq"] = 200 + round(value * 1800 / 100)

    def _get_volume(self):
        return config.conf["morseSynth"]["volume"]

    def _set_volume(self, value):
        config.conf["morseSynth"]["volume"] = value

    def speak(self, speechSequence):
        self.cancel()
        self._cancel.clear()

        wpm = config.conf["morseSynth"]["wpm"]
        freq = config.conf["morseSynth"]["freq"]
        farnsworth = config.conf["morseSynth"]["farnsworth"]
        self._volume = config.conf["morseSynth"]["volume"]

        def run():
            for item in speechSequence:
                if self._cancel.is_set():
                    break
                if isinstance(item, str):
                    self._playMorse(item, wpm, freq, farnsworth)
                elif isinstance(item, IndexCommand):
                    synthDriverHandler.synthIndexReached.notify(synth=self, index=item.index)
            if not self._cancel.is_set():
                synthDoneSpeaking.notify(synth=self)
        self._playThread = threading.Thread(target=run, daemon=True)
        self._playThread.start()

    def cancel(self):
        self._cancel.set()
        if self._playThread and self._playThread.is_alive():
            self._playThread.join(timeout=0.1)
        self._playThread = None

    def _playMorse(self, text, wpm, freq, farnsworth):
        unit = morse_unit(wpm)
        fws = farnsworth
        dit = unit
        dah = 3 * unit
        intra_element_gap = unit
        inter_char_gap = 3 * unit * fws
        inter_word_gap = 7 * unit * fws

        text = text.replace('\r\n', '\n').replace('\r', '\n')

        now = time.monotonic()
        timeline = now

        i = 0
        length = len(text)
        while i < length:
            if self._cancel.is_set():
                break
            char = text[i]
            if char == ' ' or char in ('\n', '\u2029'):
                timeline = self._wait_until(timeline, inter_word_gap)
                while i + 1 < length and (text[i+1] == ' ' or text[i+1] in ('\n', '\u2029')):
                    i += 1
                i += 1
                continue

            code = MORSE_CODE.get(char.upper(), '')
            if not code:
                i += 1
                continue  # Unbekanntes Zeichen überspringen

            for j, symbol in enumerate(code):
                if self._cancel.is_set():
                    break
                if symbol == '.':
                    tones.beep(freq, int(dit * 1000), left=self._volume, right=self._volume)
                    timeline = self._wait_until(timeline, dit)
                elif symbol == '-':
                    tones.beep(freq, int(dah * 1000), left=self._volume, right=self._volume)
                    timeline = self._wait_until(timeline, dah)
                if j < len(code) - 1:
                    timeline = self._wait_until(timeline, intra_element_gap)
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
            time.sleep(min(remaining, 0.003))
        return target