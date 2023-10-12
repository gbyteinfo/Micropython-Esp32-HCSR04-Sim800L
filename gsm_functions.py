from machine import UART
import time

class GsmSim800lMsg:
    def __init__(self):
        TX_PIN = 17
        RX_PIN = 16
        self.GSM_Instance = UART(1, tx=TX_PIN, rx=RX_PIN, baudrate=0) # baudrate definido como auto
        self.send_count = 1
        self.flag = ""
        self.numeros = ["+5519992815223"]
        self.resposta = ""

    def send_cmd(self, cmd, back=None, timeout=2000):
        print('Enviando:', cmd)
        self.GSM_Instance.write(cmd)
        time.sleep_ms(300)
        wait_time = 0
        while wait_time < timeout:
            if self.GSM_Instance.any():
                response = self.GSM_Instance.read()
                time.sleep_ms(300)
                print('Resposta:', response)
                if back:
                    if back in response:
                        time.sleep_ms(300)
                        return True, response
                else:
                    return True, response
            time.sleep_ms(300)
            wait_time += 100
        return False, ''
    
    def send(self):
        while self.send_count == 1:
            for index, numero in enumerate(self.numeros):
                success, _ = self.send_cmd('AT\r\n', 'OK')
                if success:
                    print('SIM800L OK.')
                else:
                    print('Falha na inicialização.')

                # Configura o modo texto para SMS
                self.send_cmd('AT+CMGF=1\r\n', 'OK')

                # Envia o SMS
                phone_number = numero
                horario_atual = self.get_time()
                message = f"ATENCAO ->Presenca Detectada<-\n\nTime:{horario_atual}\nEnviado para: {index+1} {phone_number}"
                success, _ = self.send_cmd(f'AT+CMGS="{phone_number}"\r\n', '>')
                if success:
                    self.send_cmd(message + chr(26), 'OK')
            
            self.send_count += 1
            
            if self.send_count == 1:
                break
        self.send_count = 1
        return self.resposta
    
    def get_time(self):
        # Busca o horario definido pela rede(esta falhando ainda em analise)
        success, response = self.send_cmd('AT+CCLK?\r\n', 'OK')
        time.sleep(1)
        if success:
            time_rede = response.decode().split('"')[1]
            print(f"\nGorario enviado: {time_rede}\n")
            return time_rede
        else:
            return "Tempo não disponível"
