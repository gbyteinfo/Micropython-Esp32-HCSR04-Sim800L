from machine import Pin
import camera
import time
import os
import gc # Garbage Collector
import ujson
import ubinascii
import network
from ufirebase import FIREBASE_GLOBAL_VAR, INTERNAL, setURL, get, put, patch

# Inicializa o pino GPIO 4 como uma saída e ssid e senha para wifi
led = Pin(2, Pin.OUT)
ssid = ""
senha = ""

# Setando o endereço do firease para a instancia atual
setURL("https://presencepulse-oficial-default-rtdb.firebaseio.com")

# Carregar configurações do Wi-Fi
with open('config.json') as f:
    config = ujson.load(f)
    ssid = config['wifi']['ssid']
    senha = config['wifi']['password']

# Função para acender e apagar o LED
def flash_led():
    led.on()  # Acende o LED
    time.sleep(1)  # Mantém aceso por 1 sec
    led.off()  # Desliga o LED
    
def conecta_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Conectando ao Wifi...")
        sta_if.active(True)
        sta_if.connect(ssid, senha)
        while not sta_if.isconnected():
            pass
    print(f"Conectado a {ssid}, {sta_if.ifconfig()}")
    
# Inicializa a câmera com as configurações específicas para o hardware
def init_camera():
    camera.init(0, d0=4, d1=5, d2=18, d3=19, d4=36, d5=39, d6=34, d7=35,
                format=camera.JPEG, framesize=camera.FRAME_VGA, 
                xclk_freq=camera.XCLK_20MHz,
                href=23, vsync=25, reset=-1, pwdn=-1,
                sioc=27, siod=26, xclk=21, pclk=22)

            
# Captura uma foto e a salva no sistema de arquivos, sobrescrevendo a anterior
def salvar_photo():
    init_camera() #Liga a Camera
    time.sleep(2) # Dá um tempo para a câmera se estabilizar
    flash_led()
    photo = camera.capture()
    camera.deinit() # Desliga a câmera para liberar recursos
    
    # Salva a foto. Usando 'w+b' como modo para sobrescrever se já existir
    with open('photo.jpg', 'w+b') as file:
        file.write(photo)
    print("Foto tirada e salva como photo.jpg.")
    
    # Dados binários (a imagem armazenada photo) em uma string codificada em Base64
    foto_base64 = ubinascii.b2a_base64(photo).decode('utf-8')
    del photo # Deleta a variavel photo para liberar recursos
    gc.collect() # Coleta de lixo para liberar memória
    # Limpeza 1
    
    data_json = ujson.dumps({
        "imagem": foto_base64
    })
    put("Dados/Imagem", data_json, bg=False, id='0')
   
    del data_json # Deleta a variavel data_json para liberar recursos
    del foto_base64 # Deleta a variavel foto_base64 para liberar recursos
    gc.collect() # Coleta de lixo para liberar memória
    # Limpeza 2
 
conecta_wifi()
salvar_photo()
