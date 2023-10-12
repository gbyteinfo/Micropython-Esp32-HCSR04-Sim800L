from wav_functions import WavSound
import time

def play():
    sound = WavSound()
    sound.execute()
    print("Executando")
    time.sleep_ms(25000)