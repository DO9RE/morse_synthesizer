# morse_synthesizer

A TTS plugin for the NVDA screen reader that outputs Morse code instead of spoken text. This allows users to practice "listening reading" by using everyday utterances and notifications from the screen reader—making the Morse code learning process a part of their digital routine. Optionally, Morse output can also be displayed on a Braille device, facilitating both listening and reading training.

## Project Status

**Early alpha!** The basic functionality is present, but there are many limitations and planned improvements. Please see "Known Issues" below.

## Features

- Converts NVDA speech output into audible Morse code instead of synthesized voice.
- Configuration dialog for speed in WPM, tone frequency, and Farnsworth factor.
- Intended for Morse code listening practice using real-life screen reader messages.
- Clipboard-to-Morse conversion dialog with copy-back function.

## Why?

Learning Morse code is difficult without authentic usage scenarios. This plugin helps you practice with texts and system messages you encounter every day—turning your NVDA speech into a training field for Morse. By listening or reading Morse for messages you already know contextually, you improve your decoding and listening skills faster and with more motivation.

## How to Install

1. Clone or copy the content of this repository into the `morse_synthesizer` folder inside your NVDA Addons directory:  
   `C:\Users\[YourUsername]\AppData\Roaming\nvda\addons\morse_synthesizer`
2. Restart NVDA.
3. "Morse Synthesizer" will show up as a regular TTS (text-to-speech engine) within NVDA. Select it like any other synthesizer.

## Keyboard Shortcuts

| Function                                         | Desktop Layout              | Laptop Layout                   |
|--------------------------------------------------|-----------------------------|---------------------------------|
| Open configuration dialog                        | NVDA+Shift+M                | NVDA+Windows+M                  |
| Show clipboard text as Morse code                | NVDA+Shift+N                | NVDA+Windows+N                  |

### Details

- **Configuration Dialog:**  
  Use the keyboard shortcut to open the configuration dialog for the Morse Synthesizer. Here you can set:
  - Speed in words per minute (WPM)
  - Tone frequency in Hz
  - Farnsworth factor  
  _Important:_ Changes only take effect after confirming the dialog.

- **Clipboard-to-Morse Dialog:**  
  Use the corresponding shortcut to open a dialog that translates the current clipboard text into Morse code.  
  The dialog displays:
    - The original clipboard text (read-only)
    - The Morse code translation (read-only)
  Additionally, there's a button to copy the Morse code back to the clipboard for further use.

## Usage Notes

- Use NVDA as you normally would. All spoken output will be replaced with Morse code signals.
- Use the configuration dialog to adjust Morse parameters to your liking.
- The clipboard-to-Morse function is great for quickly converting and sharing text in Morse code.

## Known Issues

- **Special characters, punctuation, and spaces are not yet converted to their proper Morse code—except when in read all mode and punctuation is set to (none).** Instead, they are spelled out as words in Morse.
- **Very experimental**—may break in future NVDA versions.

## Planned Features

- Proper mapping of all characters, including punctuation and spaces.
- Improved error handling and integration.
- Internationalization.
- Integration of synthesizer settings into the NVDA Voice Settings Ring (Rotor).

## Contributing

All contributions, feature requests, bug reports, and pull requests are welcome!

## Credits

Created and maintained by Richard, DO9RE. Special thanks to the friendly folks from my NVDA users WhatsApp group.

---

*Happy Morse coding and NVDA listening practice!*