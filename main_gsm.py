from gsm_functions import GsmSim800lMsg
from main_wavsound import play
import time

def execute():
    gsm = GsmSim800lMsg()
    play()
    time.sleep_ms(25000)
    resposta = gsm.send()
    print("Resposta final:", resposta)
    return resposta