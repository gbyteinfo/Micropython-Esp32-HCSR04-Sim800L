from machine import Pin, SoftI2C, UART
from gsm_functions import GsmSim800lMsg
import time
import ssd1306
import network
import ubinascii
import ubluetooth
import ujson
import ufirebase as firebase

class SemafaroIoT:
    def __init__(self):
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        self.OLED = ssd1306.SSD1306_I2C(128, 32, self.i2c, addr=0x3C)
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
        self.ssid = 'VIVOFIBRA-9271' 
        self.senha = 'CPnf2vzdJm'
        #self.ssid = 'red' 
        #self.senha = 'J23a44g21.na2021'
        # Carregar configurações do Wi-Fi
        with open('config.json') as f:
            config = ujson.load(f)
            self.ssid = config['wifi']['ssid']
            self.senha = config['wifi']['password']
     
    def on_ble_connect(self, event, data):
        if event == ubluetooth.EVT_CONN:
            print("Dispositivo conectado.")
        elif event == ubluetooth.EVT_DISCONN:
            print("Dispositivo desconectado.")
        elif event == ubluetooth.EVT_RX_DATA:
            packet = self.ble.read(data[0], data[1])
            self.wifi_data = packet.decode()
            print("Dados do Wi-Fi recebidos:", self.wifi_data)
            self.data_received = True
            
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
    
    def conect_wiffi(self):
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
        #self.OLED.text(self.enviar_sms(), 6, 15)#.........Envia o SMS por GSM
        self.OLED.show()
        time.sleep(4)
        self.salvar_firebase(distancia)#...................Salva os dados no firebase
        self.LED_VERMELHO(0)
        led_on = False
            
    def enviar_sms(self):
        resposta = self.gsm.send()
        return resposta
    
    def salvar_firebase(self, distancia):
        self.conect_wiffi()    #connect wiffi
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
        #imagem_url = ubinascii.b2a_base64("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")
        data_json = ujson.dumps({
            "presenca": "Detectada Uhuu",
            "distancia": "{:.2f}".format(distancia),
            "imagem": "Imagem da Camera"
        })
        firebase.put("Teste/Dados", data_json)
        time.sleep(5)            
