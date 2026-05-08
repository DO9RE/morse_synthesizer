import wx
import addonHandler
import config
import gui
import gui.guiHelper
import gui.nvdaControls
import gui.settingsDialogs
import globalPluginHandler
from scriptHandler import script
from logHandler import log

addonHandler.initTranslation()

confspec = {
    "wpm": "integer(default=15, min=5, max=60)",
    "freq": "integer(default=440, min=200, max=2000)",
    "farnsworth": "float(default=1.0, min=0.5, max=3.0)",
}
config.conf.spec["morseSynth"] = confspec


class MorseSynthSettingsPanel(gui.settingsDialogs.SettingsPanel):
    title = _("Morsecode Synthesizer")

    def makeSettings(self, settingsSizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        self.wpmEdit = sHelper.addLabeledControl(
            _("WPM:"),
            gui.nvdaControls.SelectOnFocusSpinCtrl,
            min=5, max=60, initial=config.conf["morseSynth"]["wpm"],
        )
        self.freqEdit = sHelper.addLabeledControl(
            _("Freq (Hz):"),
            gui.nvdaControls.SelectOnFocusSpinCtrl,
            min=200, max=2000, initial=config.conf["morseSynth"]["freq"],
        )
        self.farnsworthEdit = sHelper.addLabeledControl(
            _("Farnsworth:"),
            wx.TextCtrl,
            value=str(config.conf["morseSynth"]["farnsworth"]),
        )

    def onSave(self):
        config.conf["morseSynth"]["wpm"] = self.wpmEdit.GetValue()
        config.conf["morseSynth"]["freq"] = self.freqEdit.GetValue()
        try:
            farn = float(self.farnsworthEdit.GetValue())
            if not (0.5 <= farn <= 3.0):
                farn = 1.0
        except ValueError:
            farn = 1.0
        config.conf["morseSynth"]["farnsworth"] = farn


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self):
        super().__init__()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(MorseSynthSettingsPanel)

    def terminate(self):
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(MorseSynthSettingsPanel)

    @script(
        description=_("Öffnet die Einstellungen für den Morsecode-Synthesizer."),
        gestures=["kb(desktop):NVDA+shift+m", "kb(laptop):NVDA+windows+m"],
        category="Morse Synthesizer",
    )
    def script_openMorseSynthConfig(self, gesture):
        wx.CallAfter(
            gui.mainFrame._popupSettingsDialog,
            gui.settingsDialogs.NVDASettingsDialog,
            MorseSynthSettingsPanel,
        )