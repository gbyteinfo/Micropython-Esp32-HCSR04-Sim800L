from semaforo_functions import SemafaroIoT
import time
import network

def execute():
    semafaro = SemafaroIoT()
    while True:
        distancia = semafaro.ler_distancia()
        start = ""
        if distancia <= 200:#.......................................................................... Distância em centimetros ( 1 metro = 100 cm )
            semafaro.OLED.fill(0)
            semafaro.desenha_borda()
            semafaro.OLED.text("Dist: {:.2f} cm".format(distancia), 10, 15)
            print("Dist: {:.2f} cm".format(distancia))
            start = ""
            
            if semafaro.timer_start is None:
                semafaro.timer_start = time.ticks_ms()#................................................. Seta o time start que é inicio do caluculo do intervalo para enviar as informações SMS e Firebase
            
            semafaro.LED_AMARELO.value(1)
            semafaro.LED_VERDE.value(0)
            
            if time.ticks_diff(time.ticks_ms(), semafaro.timer_start) >= semafaro.timer_duration:#...... Função ticks_diff recebe dois times o atual e o inicial, e devolve o intervalo enre eles. Intervalo érmitido para continuar scaneando é programado em segundos, e definidos na semaforo_functions
                semafaro.LED_AMARELO.value(0)
                semafaro.envio_sms(distancia)#.......................................................... Envia 
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