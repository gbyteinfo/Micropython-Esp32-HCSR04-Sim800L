from machine import Pin, SoftI2C, UART
from gsm_functions import GsmSim800lMsg
import time
import ssd1306

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
        self.timer_duration = 5000
#       self.timer_duration = 10000
        self.timer_start_margin = None
        self.timer_duration_margin = 2000
        self.gsm = GsmSim800lMsg()
        
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
    
    def desenha_borda(self):
        for x in range(128):
            self.OLED.pixel(x, 0, 1)
            self.OLED.pixel(x, 31, 1)
        for y in range(32):
            self.OLED.pixel(0, y, 1)
            self.OLED.pixel(127, y, 1)    
    
    def teste_envio_sms(self):
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
        self.OLED.text(self.enviar_sms(), 6, 15)
        self.OLED.show()
        time.sleep(5)
        self.LED_VERMELHO(0)
        led_on = False
        
    def enviar_sms(self):
        resposta = self.gsm.send()
        return resposta

