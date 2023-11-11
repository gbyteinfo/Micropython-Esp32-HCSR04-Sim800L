from gsm_functions import GsmSim800lMsg
from main_wavsound import play
import time

def execute():
    gsm = GsmSim800lMsg()
    resposta = gsm.send()
    print("Resposta final:", resposta)
    return resposta