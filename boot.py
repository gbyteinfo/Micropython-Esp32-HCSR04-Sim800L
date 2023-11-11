from main_semaforo import execute
#from main_gsm import execute #.....................Para testar apenas o envio do sms, executar o execute do main_gsm(comente o import no main_semaforo)
from machine import Pin
import time

def main():
    resposta = execute()    
    
#def startserv():
    # Hack para ativar Esp32wrover Cam que nao boot ao ligalar ela
    # Solução foi usar a esp32 principal para dar o boot nela pelo GPIO 14
    # Colocando seu estado inicial em low(0) e em seguida ativando e desativando de novo
    # Com isso ela inicia com o servidor de stream da cam para tirar as fotos e ou disponibilizar
    # o stream de video local
    
    # Configura o pino GPIO 14 como saída
    #reset_pin = Pin(14, Pin.OUT)

    # Para ativar o pino EN
    #reset_pin.value(1)

    # Para desativar o pino EN
    #reset_pin.value(0)


if __name__ == "__main__":
    main()








