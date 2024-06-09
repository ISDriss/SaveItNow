from Record import record_and_save
from STT import Audio_To_Text

AUDIO_URL = "./Backend/TempFiles/audio.wav"
TEXT_URL = "./Backend/TempFiles/transcript.txt"
SUMMARY_URL = "./Backend/TempFiles/summary.txt"

record_and_save(AUDIO_URL)
Audio_To_Text(AUDIO_URL, TEXT_URL)



