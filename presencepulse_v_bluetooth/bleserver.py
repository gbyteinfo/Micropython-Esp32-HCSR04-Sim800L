import ubluetooth
import time
from ubluetooth import BLE, UUID, FLAG_READ, FLAG_NOTIFY, FLAG_WRITE
from micropython import const

_DEVICE_NAME = 'ESP32-Semafaro'
_SERVICE_UUID = UUID('12345678-1234-5678-1234-56789ABCDEF0')
_CHAR_UUID = UUID('12345678-1234-5678-1234-56789ABCDEF1')

_BLE_IRQ_CENTRAL_CONNECT = const(1)
_BLE_IRQ_CENTRAL_DISCONNECT = const(2)
_BLE_IRQ_GATTS_WRITE = const(3)

class BLEServer:
    def __init__(self, name):
        self._ble = BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._connections = set()
        self._data_received = False
        self._wifi_data = ""

        self._services = (
            (_SERVICE_UUID, (
                (_CHAR_UUID, FLAG_READ | FLAG_NOTIFY | FLAG_WRITE),
            )),
        )
        self._handles = self._ble.gatts_register_services(self._services)

        name_bytes = bytes(name, "utf-8")
        self._adv_payload = bytearray(  # Aqui, armazenamos a adv_payload como um atributo
            b'\x02\x01\x06'
            b'\x03\x03\x9E\xFE'
            + bytes([1 + len(name_bytes)]) + b'\x09' + name_bytes
        )
        self._ble.gap_advertise(100, adv_data=self._adv_payload)

    def _irq(self, event, data):
        if event == _BLE_IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("Connected")
        elif event == _BLE_IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self._ble.gap_advertise(100, adv_data=self._adv_payload)  # Aqui usamos o atributo armazenado
            self._data_received = False
        elif event == _BLE_IRQ_GATTS_WRITE:
            conn_handle, attr_handle, buf, offset = data
            if attr_handle == self._handles[0][0]:
                self._wifi_data = buf.decode()
                print("Wi-Fi Data Received:", self._wifi_data)
                self._data_received = True

    def is_data_received(self):
        return self._data_received