import wx
import gui
import gui.guiHelper
import addonHandler
import globalPluginHandler
import ui
from scriptHandler import script
from logHandler import log

addonHandler.initTranslation()

MORSE_CODE_DICT = {
    'A': '.-',     'Ä': '.-.-',  'B': '-...',  'C': '-.-.',  'D': '-..',
    'E': '.',      'É': '..-..', 'F': '..-.',  'G': '--.',   'H': '....',
    'I': '..',     'J': '.---',  'K': '-.-',   'L': '.-..',  'M': '--',
    'N': '-.',     'O': '---',   'Ö': '---.',  'P': '.--.',  'Q': '--.-',
    'R': '.-.',    'S': '...',   'ß': '...--..','T': '-',    'U': '..-',
    'Ü': '..--',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    '0': '-----',  '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....',  '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', ':': '---...', '?': '..--..', "'": '.----.',
    '-': '-....-', '/': '-..-.',  '(': '-.--.',  ')': '-.--.-', '"': '.-..-.',
    '=': '-...-',  '+': '.-.-.',  '@': '.--.-.', '!': '-.-.--', '&': '.-...',
    ';': '-.-.-.', '_': '..--.-', '$': '...-..-', '¿': '..-.-', '¡': '--...-',
    ' ': '',
    'á': '.--.-',  'à': '.--.-', 'ä': '.-.-',  'å': '.--.-', 'ç': '-.-..',
    'é': '..-..',  'è': '.-..-', 'ð': '..--.', 'ñ': '--.--', 'ö': '---.',
    'ø': '---.',   'ś': '...-...', 'š': '----', 'ü': '..--', 'þ': '.--..',
    'ß': '...--..', '¿': '..-.-', '¡': '--...-'
}
for c in list(MORSE_CODE_DICT):
    if len(c) == 1 and c.isalpha() and c.isupper():
        lower = c.lower()
        if lower not in MORSE_CODE_DICT:
            MORSE_CODE_DICT[lower] = MORSE_CODE_DICT[c]

def text_to_morse(text):
    morse_words = []
    for word in text.split(' '):
        morse_chars = []
        for char in word:
            code = MORSE_CODE_DICT.get(char, '?')
            morse_chars.append(code)
        if morse_chars:
            morse_words.append(' '.join(morse_chars))
    return '   '.join(morse_words)

class MorseSpeechDisplayDialog(wx.Dialog):
    def __init__(self, morseText, originalText, parent=None):
        super().__init__(
            parent,
            title=_("Clipboard Morsecode"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=mainSizer)
        self.origTextCtrl = sHelper.addLabeledControl(
            _("Clipboard Text:"),
            wx.TextCtrl,
            value=originalText,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL,
        )
        self.origTextCtrl.SetMinSize((-1, 80))
        self.textCtrl = sHelper.addLabeledControl(
            _("Morsecode:"),
            wx.TextCtrl,
            value=morseText,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL,
        )
        self.textCtrl.SetMinSize((-1, 120))
        bHelper = gui.guiHelper.ButtonHelper(wx.HORIZONTAL)
        copyBtn = bHelper.addButton(self, label=_("Morsecode in Zwischenablage kopieren"))
        copyBtn.Bind(wx.EVT_BUTTON, self.onCopy)
        bHelper.addButton(self, id=wx.ID_OK, label=_("Schließen"))
        sHelper.addItem(bHelper.sizer, flag=wx.ALIGN_RIGHT)
        self.SetMinSize((500, -1))
        self.SetSizerAndFit(mainSizer)
        self.CentreOnScreen()

    def onCopy(self, evt):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.textCtrl.GetValue()))
            wx.TheClipboard.Close()
            ui.message(_("Der Morsecode wurde in die Zwischenablage kopiert."))
        else:
            gui.messageBox(
                _("Konnte die Zwischenablage nicht öffnen."),
                _("Fehler"),
                wx.OK | wx.ICON_ERROR,
                self,
            )

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    @script(
        description=_("Zeigt den aktuellen Text der Zwischenablage als Morsecode an."),
        gestures=["kb(desktop):NVDA+shift+n", "kb(laptop):NVDA+windows+n"],
        category="Morse Synthesizer"
    )
    def script_showClipboardAsMorse(self, gesture):
        def show():
            clipboard_text = ""
            if wx.TheClipboard.Open():
                if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
                    data = wx.TextDataObject()
                    wx.TheClipboard.GetData(data)
                    clipboard_text = data.GetText()
                wx.TheClipboard.Close()
            clipboard_text = clipboard_text.strip()
            if not clipboard_text:
                clipboard_text = _("Kein Text in der Zwischenablage gefunden. Bitte kopiere erst Text in die Zwischenablage.")
                morse_text = ""
            else:
                morse_text = text_to_morse(clipboard_text)
            dlg = MorseSpeechDisplayDialog(morse_text, clipboard_text, gui.mainFrame)
            dlg.ShowModal()
            dlg.Destroy()
        wx.CallAfter(show)