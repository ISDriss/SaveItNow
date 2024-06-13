import threading
import keyboard
import pyaudio
import wave
from audio_denoiser.AudioDenoiser import AudioDenoiser

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second

def record_and_save(file):
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = p.open(format=sample_format, channels=channels, rate=fs, input=True, frames_per_buffer=chunk)
    frames = []

    # Function to read from the stream
    def read_stream():
        while not stop_flag.is_set():
            data = stream.read(chunk)
            frames.append(data)

    # Flag to stop the thread
    stop_flag = threading.Event()

    # Start the stream reading in a separate thread
    thread = threading.Thread(target=read_stream)
    thread.start()

    # Wait for the Enter key press to stop the stream
    print("Recording, press Enter to stop recording...")
    keyboard.wait('enter')

    # Signal the thread to stop and wait for it to finish
    stop_flag.set()
    thread.join()

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print('Finished recording')

def clean_audio(file):
    denoiser = AudioDenoiser()
    denoiser.process_audio_file(file, file)