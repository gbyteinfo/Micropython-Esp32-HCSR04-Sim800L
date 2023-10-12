from gsm_functions import GsmSim800lMsg

def execute():
    gsm = GsmSim800lMsg()
    resposta = gsm.send()
    print("Resposta final:", resposta)
    return resposta