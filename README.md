# morse_synthesizer

A TTS plugin for the NVDA screen reader that outputs Morse code instead of spoken text. This allows users to practice "listening reading" by using everyday utterances and notifications from the screen reader—making the Morse code learning process a part of their digital routine. Optionally, Morse output can also be displayed on a Braille device, facilitating both listening and reading training.

## Project Status

**Early alpha!** The basic functionality is present, but there are many limitations and planned improvements. Please see "Known Issues" below.

## Features

- Converts NVDA speech output into audible Morse code instead of synthesized voice.
- Configuration Dialog for speed in wpm, tone frequency and Farnsworth-factor.
- Intended for Morse code listening practice using real-life screen reader messages.

## Why?

Learning Morse code is difficult without authentic usage scenarios. This plugin helps you practice with texts and system messages you encounter every day—turning your NVDA speech into a training field for Morse. By listening or reading Morse for messages you already know contextually, you improve your decoding and listening skills faster and with more motivation.

## How to Install

1. Clone or copy the content of this repository into the `morse_synthesizer` folder inside your NVDA Addons directory:
`C:\Users\[YourUsername]\AppData\Roaming\nvda\addons\morse_synthesizer`
2. Restart NVDA.
3. "Morse Synthesizer" will show up as a regular TTS (text-to-speech engine) within NVDA. Select it like any other synthesizer.

## Usage Notes

- Use NVDA as you normally would. All spoken output will be replaced with Morse code signals.
- Press NVDA+Shift+M on a desktop layout, or NVDA+Windows+M on a laptop, for a basic configuration Dialog. Adjust Speed, Frequency and the Farnsworth-factor according to your liking.

## Known Issues

- **Special characters, punctuation, and spaces are not yet converted to their proper Morse code - except when in read all mode and punctuation is set to (none) - equivalents.** Instead, they are spelled out as words in Morse.
- **Very experimental**—may break in future NVDA versions.

## Planned Features

- Proper mapping of all characters, including punctuation and spaces.
- Improved error handling and integration.
- Internationalization.

## Contributing

All contributions, feature requests, bug reports and pull requests are welcome!

## Credits

Created and maintained by Richard, DO9RE. Special thanks to the friendly guys from my NVDA users WhatsApp group.

---

*Happy Morse coding and NVDA listening practice!*
