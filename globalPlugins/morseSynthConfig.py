import wx
import addonHandler
import config
import gui
import globalPluginHandler
from scriptHandler import script
from logHandler import log
from gettext import gettext as _

addonHandler.initTranslation()

class MorseSynthConfigDialog(wx.Dialog):
    def __init__(self, parent=None):
        super().__init__(parent, title=_("Morsecode-Synthesizer"), style=wx.DEFAULT_DIALOG_STYLE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Abschnitt anlegen, falls nicht vorhanden
        if "morseSynth" not in config.conf:
            config.conf["morseSynth"] = {}
        self._settings = config.conf["morseSynth"]
        wpm = int(self._settings.get('wpm', 15))
        freq = int(self._settings.get('freq', 440))
        farnsworth = self._settings.get('farnsworth', 1.0)
        
        # Geschwindigkeit (WPM)
        wpmSizer = wx.BoxSizer(wx.HORIZONTAL)
        wpmLabel = wx.StaticText(self, label=_("WPM:"))
        self.wpmEdit = wx.SpinCtrl(self, min=5, max=60)
        self.wpmEdit.SetValue(wpm)
        wpmSizer.Add(wpmLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        wpmSizer.Add(self.wpmEdit, 0, wx.ALL, 5)
        sizer.Add(wpmSizer, 0, wx.EXPAND)
        
        # Tonhöhe (Hz)
        freqSizer = wx.BoxSizer(wx.HORIZONTAL)
        freqLabel = wx.StaticText(self, label=_("Freq (Hz):"))
        self.freqEdit = wx.SpinCtrl(self, min=200, max=2000)
        self.freqEdit.SetValue(freq)
        freqSizer.Add(freqLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        freqSizer.Add(self.freqEdit, 0, wx.ALL, 5)
        sizer.Add(freqSizer, 0, wx.EXPAND)
        
        # Farnsworth-Faktor
        farnSizer = wx.BoxSizer(wx.HORIZONTAL)
        farnLabel = wx.StaticText(self, label=_("Farnsworth:"))
        self.farnsworthEdit = wx.TextCtrl(self, value=str(farnsworth))
        farnSizer.Add(farnLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        farnSizer.Add(self.farnsworthEdit, 0, wx.ALL, 5)
        sizer.Add(farnSizer, 0, wx.EXPAND)

        btns = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(btns, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        self.SetSizerAndFit(sizer)
        self.CentreOnScreen()

    def Save(self):
        try:
            self._settings['wpm'] = self.wpmEdit.GetValue()
            self._settings['freq'] = self.freqEdit.GetValue()
            farn = float(self.farnsworthEdit.GetValue())
            if farn < 0.5 or farn > 3.0:
                farn = 1.0
            self._settings['farnsworth'] = farn
            config.conf.save()  # Einstellungen dauerhaft speichern
        except Exception as e:
            log.error(f"Fehler beim Speichern der MorseSynth-Einstellungen: {e}")

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    @script(
        description=_("Öffnet die Einstellungen für den Morsecode-Synthesizer."),
        gestures=["kb(desktop):NVDA+shift+m","kb(laptop):NVDA+windows+m"],
        category="Morse Synthesizer" 
    )

    def script_openMorseSynthConfig(self, gesture):
        def show():
            dlg = MorseSynthConfigDialog(gui.mainFrame)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Save()
            dlg.Destroy()
        wx.CallAfter(show)