import assemblyai as aai

aai.settings.api_key = "0ddb3b06c064442a8ed1f48767cd2b74"
config = aai.TranscriptionConfig(language_code="fr")

def Audio_To_Text(audio, text):
    print("transcribing audio...")

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio, config = config)

    # si la transcription n'échoue pas, le texte est sauvegardé
    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
        with open(text,'w') as f:
            f.write("an error occured")
    else:
        with open(text, 'w') as f:
            f.write(transcript.text)
    
    print("transcription completed")