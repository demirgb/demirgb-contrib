# ADC Microphone Show

This is a simple example of a sound-reactive light show, cycling through colors while pulsing light intensity with sound.

It listens to the D1 Mini's ADC (up to 3.3v), and expects a DC offset roughly in the middle.  The [Adafruit Electret Microphone Amplifier - MAX9814 with Auto Gain Control](https://www.adafruit.com/product/1713) is ideal for this, as it has a 1.25v DC offset and 2v peak-to-peak.

This script loops through sampling the ADC for 50ms to determine the peak-to-peak, and uses it as the intensity.  The color loops through a rotating hue cycle, roughly every 2.25 seconds (configuable; default 50ms sample time * 45 hue steps = 2250ms).
