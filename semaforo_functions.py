from machine import Pin, SoftI2C, UART
from gsm_functions import GsmSim800lMsg
import time
import ssd1306
import network
import ubinascii
import ujson
import ufirebase as firebase
import os

class SemafaroIoT:
    def __init__(self):
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        self.OLED = ssd1306.SSD1306_I2C(128, 32, self.i2c, addr=0x3C)
        self.reset_pin = Pin(14, Pin.IN)
        self.LED_VERDE = Pin(5, Pin.OUT, value=0)
        self.LED_AMARELO = Pin(19, Pin.OUT, value=0)
        self.LED_VERMELHO = Pin(23, Pin.OUT, value=0)
        self.TRIG = Pin(15, Pin.OUT)
        self.ECHO = Pin(4, Pin.IN)
        self.GSM_Instance = UART(2, baudrate=0, tx=17, rx=16)
        self.timer_start = None
        self.timer_duration = 6000
#       self.timer_duration = 10000
        self.timer_start_margin = None
        self.timer_duration_margin = 2000
        self.gsm = GsmSim800lMsg()
        self.sta_if = network.WLAN(network.STA_IF)
        
        # Carregar configurações do Wi-Fi
        with open('config.json') as f:
            config = ujson.load(f)
            self.ssid = config['wifi1']['ssid']
            self.senha = config['wifi1']['password']
            
    def ler_distancia(self):
        self.TRIG.init(mode=Pin.OUT)
        
        self.TRIG.value(0)
        time.sleep_us(2)
        self.TRIG.value(1)
        time.sleep_us(10)
        self.TRIG.value(0)
        
        while self.ECHO.value() == 0:
            pass
        
        inicio = time.ticks_us()
        
        while self.ECHO.value() == 1:
            pass
        
        fim = time.ticks_us()
        
        duracao = fim - inicio
        distancia = (duracao / 2) / 29.1  # em cm
        self.TRIG.init(mode=Pin.IN)
        return distancia
    
    def verifica_wiffi(self):
        if not self.sta_if.isconnected():
            self.OLED.fill(0)
            self.desenha_borda()
            self.OLED.text("Conectando", 15, 3)
            self.OLED.text("Wifi...", 22, 15)
            self.OLED.show()
            self.sta_if.active(True)
            self.sta_if.connect(self.ssid, self.senha)
            print("Conectando Wifi")
            while not self.sta_if.isconnected():
                print(".", end="")
                time.sleep(0.1)
            print("Wi-Fi Conectado.")
            time.sleep(1)
            #self.OLED.fill(0)
            #self.desenha_borda()
            #self.OLED.text("Wif des...", 7, 15)
            #self.OLED.show()
            #self.sta_if.active(False)
            #print("WiFi Desativado.")
    
    def desenha_borda(self):
        for x in range(128):
            self.OLED.pixel(x, 0, 1)
            self.OLED.pixel(x, 31, 1)
        for y in range(32):
            self.OLED.pixel(0, y, 1)
            self.OLED.pixel(127, y, 1)    
    
    def envio_sms(self, distancia):
        
        self.OLED.fill(0)
        self.desenha_borda()
        self.OLED.text("Enviando SMS...", 8, 15)
        self.OLED.show()
        sec = 1
        while sec <= 1:
            self.LED_VERMELHO.value(1)
            time.sleep(1.0)
            self.LED_VERMELHO.value(0)
            time.sleep(1.0)
            self.LED_VERMELHO.value(1)
            time.sleep(0.7)
            self.LED_VERMELHO.value(0)
            time.sleep(0.7)
            self.LED_VERMELHO.value(1)
            time.sleep(0.5)
            self.LED_VERMELHO.value(0)
            time.sleep(0.5)
            self.LED_VERMELHO.value(1)
            time.sleep(0.3)
            self.LED_VERMELHO.value(0)
            time.sleep(0.3)
            self.LED_VERMELHO.value(1)
            for i in range(5):
                time.sleep(0.1)
                self.LED_VERMELHO.value(0)
                time.sleep(0.1)
                self.LED_VERMELHO.value(1)
            sec = sec + 1
        led_on = True
        self.OLED.fill(0)
        self.desenha_borda()
        self.OLED.text(self.enviar_sms(distancia), 6, 15)#.......... 1° Envia o SMS por GSM
        self.OLED.show()
        time.sleep(4)
        led_on = True
        self.startPhoto()#.......................................... 2° Tira Foto com a espwrover
        time.sleep(2)
        self.salvar_firebase(distancia)#............................ 3° Salva os dados no firebase e é carregado no APP REACT para vizualização na web(futuramente miostrando foto tirada no local tambem)
        self.LED_VERMELHO(0)
        led_on = False
        
    def startPhoto(self):
        # Hack para ativar Esp32wrover Cam que nao boot ao ligalar ela
        # Solução foi usar a esp32 principal para dar o boot nela pelo GPIO 14
        # Colocando seu estado inicial em hight(1) e em seguida ativando e desativando de novo
        # Com isso ela inicia com o servidor de stream da cam para tirar as fotos e ou disponibilizar
        # o stream de video local
        self.OLED.fill(0)
        self.desenha_borda()
        self.OLED.text("Ligando Cam...", 3, 15)#.......... 1° Envia o SMS por GSM
        self.OLED.show()
        self.reset_pin = Pin(14, Pin.OUT)
        time.sleep(1)
        self.reset_pin = Pin(14, Pin.IN)
        
    def enviar_sms(self, distancia):
        resposta = self.gsm.enviar_sms(distancia)
        return resposta
    # Variável global para armazenar os dados obtidos do Firebase
        dados_firebase = {}                
        
    def salvar_firebase(self, distancia):
        self.verifica_wiffi()#................................ Connecta Wiffi
        self.OLED.fill(0)
        self.desenha_borda()
        self.OLED.text("Wifi Conectado!", 2, 15)
        self.OLED.show()
        time.sleep(3)
        
        self.OLED.fill(0)
        self.desenha_borda()
        self.OLED.text("Firebase save...", 2, 3)
        self.OLED.text("HortoPlaza Hotel", 2, 18)
        self.OLED.show()
        firebase.setURL("https://presencepulse-oficial-default-rtdb.firebaseio.com")
        data_json = ujson.dumps({
            "presenca": "Detectada Uhuu",
            "distancia": "{:.2f}".format(distancia),
        })
        firebase.put("Dados2/Presenca", data_json)
        time.sleep(4)
        # Tentar obter dados do Firebase
        #try:
        #    def busca_dados(name, id, varname):
        #        print("value: "+str(eval("firebase."+varname))+"\n")
        #    firebase.get("Teste", "VAR1", bg=True, id=0, cb=(busca_dados, ("Teste", "0", "VAR1")))
        #    time.sleep(4)
            # Salvar dados no Firebase
           
        #except Exception as e:
        #    print("Erro ao acessar o Firebase:", e)    