from machine import UART
import time

class GsmSim800lMsg:
    def __init__(self):
        TX_PIN = 17
        RX_PIN = 16
        self.GSM_Instance = UART(1, tx=TX_PIN, rx=RX_PIN, baudrate=0)  # baudrate definido como 9600
        #self.numeros = ["+5519992815223"]
        self.numeros = ["+5519981728120", "+5519974086936"]

    def send_cmd(self, cmd, back=None, timeout=2000):
        print('Enviando:', cmd)
        self.GSM_Instance.write(cmd)
        time.sleep_ms(300)
        wait_time = 0
        while wait_time < timeout:
            if self.GSM_Instance.any():
                response = self.GSM_Instance.read()
                print('Resposta:', response)
                if back and back in response:
                    time.sleep_ms(300)
                    return True, response
            time.sleep_ms(300)
            wait_time += 100
        return False, ''

    def enviar_sms(self, distancia):
        # Inicialização
        for numero in self.numeros:
            def verifica_SMSC():
                self.send_cmd('AT+CSCA="+552191105300",145\r\n', 'OK')#claro
                #self.send_cmd('AT+CSCA="+551181136200",145\r\n', 'OK')#tim
                time.sleep_ms(500)
            verifica_SMSC()

            success, _ = self.send_cmd('AT\r\n', 'OK')
            if not success:
                print('Falha na inicialização.')
                continue
            
            # Configura o modo texto para SMS
            self.send_cmd('AT+CMGF=1\r\n', 'OK')

            # Envia o SMS
            distancia_formatada = "{:.2f}".format(distancia)
            message = f"ATENCAO Presenca Detectada \nDist: {} cm".format(distancia_formatada)
            success, _ = self.send_cmd(f'AT+CMGS="{numero}"\r\n', '>')
            if success:
                self.send_cmd(message + chr(26), 'OK')
            else:
                print(f"Falha ao enviar SMS para {numero}")

        return "SMS enviado com sucesso"
