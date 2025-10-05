import wx
import gui
import addonHandler
import globalPluginHandler
from scriptHandler import script
from logHandler import log
from gettext import gettext as _
import wx.adv

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
            parent, title=_("Clipboard Morsecode"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        sizer = wx.BoxSizer(wx.VERTICAL)
        staticLabel1 = wx.StaticText(self, label=_("Clipboard Text:"))
        sizer.Add(staticLabel1, 0, wx.ALL | wx.EXPAND, 8)
        self.origTextCtrl = wx.TextCtrl(
            self, value=originalText, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        )
        self.origTextCtrl.SetMinSize((500, 80))
        sizer.Add(self.origTextCtrl, 0, wx.ALL | wx.EXPAND, 8)
        staticLabel = wx.StaticText(self, label=_("Morsecode:"))
        sizer.Add(staticLabel, 0, wx.ALL | wx.EXPAND, 8)
        self.textCtrl = wx.TextCtrl(
            self, value=morseText, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        )
        self.textCtrl.SetMinSize((500, 120))
        sizer.Add(self.textCtrl, 1, wx.ALL | wx.EXPAND, 8)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        copyBtn = wx.Button(self, wx.ID_ANY, _("Morsecode in Zwischenablage kopieren"))
        copyBtn.Bind(wx.EVT_BUTTON, self.onCopy)
        btnSizer.Add(copyBtn, 0, wx.ALL, 5)
        closeBtn = wx.Button(self, wx.ID_OK, _("Schließen"))
        btnSizer.AddStretchSpacer()
        btnSizer.Add(closeBtn, 0, wx.ALL, 5)
        sizer.Add(btnSizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)
        self.CentreOnScreen()

    def onCopy(self, evt):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.textCtrl.GetValue()))
            wx.TheClipboard.Close()
            wx.adv.NotificationMessage(_("Morsecode kopiert"), _("Der Morsecode wurde in die Zwischenablage kopiert.")).Show(timeout=wx.adv.NotificationMessage.Timeout_Auto)
        else:
            wx.MessageBox(_("Konnte die Zwischenablage nicht öffnen."), _("Fehler"), wx.ICON_ERROR)

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