# Child's Automatic Printer Configuration

# Daily print limits
DAILY_PRINT_LIMIT = 10

# Voice recognition settings
VOICE_TIMEOUT = 5
VOICE_PHRASE_TIME_LIMIT = 10
VOICE_LANGUAGE = "fi-FI"

# Finnish wake words (commands that trigger printing)
WAKE_WORDS = ["tulosta", "kirjoita", "piirtää", "kuva", "tee"]

# Audio settings
TTS_RATE = 150  # Words per minute (slower for children)
TTS_VOLUME = 0.8

# Content filtering
MAX_CONTENT_LENGTH = 200
ENABLE_EDUCATIONAL_BOOST = True

# Printer settings
DEFAULT_PRINTER = None  # Use system default
PRINT_TIMEOUT = 30

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "kidprinter.log"
