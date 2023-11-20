from main_semaforo import execute
#from main_gsm import execute #.....................Para testar apenas o envio do sms, executar o execute do main_gsm(comente o import no main_semaforo)
from machine import Pin
import time

def main():
    resposta = execute()    

if __name__ == "__main__":
    main()









