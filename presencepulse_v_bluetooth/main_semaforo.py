from semaforo_functions import SemafaroIoT
from bleserver import BLEServer
import time
import network

def execute():
    semafaro = SemafaroIoT()
    time.sleep(1)
    ble_server = BLEServer("Esp Gbyteinfo")
    # Wait for Wi-Fi data to be received
    semafaro.OLED.fill(0)
    semafaro.desenha_borda()
    semafaro.OLED.text("Conecte-se ...", 5, 15)
    semafaro.OLED.show()
    while not ble_server.is_data_received():
        time.sleep(1)
    # Wi-Fi data has been received, continue with main logic
    semafaro.OLED.fill(0)
    semafaro.desenha_borda()
    semafaro.OLED.text("Dado Recebido", 2, 2)
    semafaro.OLED.text("SSid: "+ble_server.__wifi_dat, 2, 15)
    semafaro.OLED.show()
    print("Wi-Fi SSID and Password:", ble_server._wifi_data)
        
    while True:
        distancia = semafaro.ler_distancia()
        start = ""
        if distancia <= 200:  # Distância em cm
            semafaro.OLED.fill(0)
            semafaro.desenha_borda()
            semafaro.OLED.text("Dist: {:.2f} cm".format(distancia), 10, 15)
            print("Dist: {:.2f} cm".format(distancia))
            start = ""
            
            if semafaro.timer_start is None:
                semafaro.timer_start = time.ticks_ms() # Seta o time
            
            semafaro.LED_AMARELO.value(1)
            semafaro.LED_VERDE.value(0)
            
            if time.ticks_diff(time.ticks_ms(), semafaro.timer_start) >= semafaro.timer_duration: #duração = 6sec
                semafaro.LED_AMARELO.value(0)
                semafaro.envio_sms(distancia)#Envia sms
                semafaro.timer_start = None  # Reseta o timer
        else:
            if "Inicializado..." not in start:
                semafaro.OLED.fill(0)
                semafaro.desenha_borda()
                print("Dist: {:.2f} cm".format(distancia))
                
                start = "Inicializado..."
                semafaro.OLED.text(start, 10, 15)
                
            semafaro.LED_AMARELO.value(0)
            semafaro.LED_VERDE.value(1)
            semafaro.timer_start = None  # Reseta o timer
        
        semafaro.OLED.show()
        time.sleep(0.5)