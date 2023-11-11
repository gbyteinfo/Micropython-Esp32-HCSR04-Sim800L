from machine import Pin, I2S
import os
from WavPlayer import WavPlayer 

class WavSound:
    def __init__(self):
        SCK_PIN = Pin(27, Pin.OUT) # I2S_BCLK
        WS_PIN = Pin(26, Pin.OUT) # I2S_LRC
        SD_PIN = Pin(25, Pin.OUT) # I2S_DOUT
        BUFFER_LENGTH_IN_BYTES = 50000
        I2S_ID = 1
        self.wp = WavPlayer(id=I2S_ID, sck_pin=SCK_PIN, ws_pin=WS_PIN, sd_pin=SD_PIN, ibuf=BUFFER_LENGTH_IN_BYTES)

    def execute(self):
        try:
            self.wp.play('20231012_141444.wav', loop=False)
            print("tocando...")
        except OSError as e:
            if e.args[0] == 2:
                print("O arquivo WAV não foi encontrado.")
            else:
                print("OSError:", e)
        except Exception as e:
            print("Erro desconhecido:", e)