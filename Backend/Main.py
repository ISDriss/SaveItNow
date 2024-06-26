from Record import record_and_save, clean_audio
from STT import Audio_To_Text
from Summary import generate_lecture_notes


AUDIO_URL = "./Backend/TempFiles/audio.wav"
TEXT_URL = "./Backend/TempFiles/transcript.txt"
SUMMARY_URL = "./Backend/TempFiles/summary.txt"

record_and_save(AUDIO_URL)
clean_audio(AUDIO_URL)
Audio_To_Text(AUDIO_URL, TEXT_URL)
generate_lecture_notes(TEXT_URL,SUMMARY_URL)





