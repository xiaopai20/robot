import pyttsx
import sys

text = sys.argv[1]
engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 80)
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')
engine.say(text)
engine.runAndWait()