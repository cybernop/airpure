import os
import time
from datetime import datetime

from prometheus_client import Gauge, start_http_server
from pyairctrl.coap_client import CoAPAirClient

g_temp = Gauge('airpure_temp', 'Temperature')
g_pm25 = Gauge('airpure_pm25', 'PM25')
g_hum = Gauge('airpure_humidity', 'Humidity')
g_allergen = Gauge('airpure_allergen', 'Allergen')


def get_stats(ip: str):
    c = CoAPAirClient(ip)

    status = None
    while not status:
        status = c.get_status()
        time.sleep(10)

    g_temp.set_to_current_time()
    g_temp.set(status['temp'])

    g_pm25.set_to_current_time()
    g_pm25.set(status['pm25'])

    g_hum.set_to_current_time()
    g_hum.set(status['rh'])

    g_allergen.set_to_current_time()
    g_allergen.set(status['iaql'])


def repeat(delay_secs: int, func, *args):
    while True:
        try:
            func(*args)

            time.sleep(delay_secs)
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    ip = os.environ.get('AIR_PUREFIER')

    start_http_server(8000, addr="0.0.0.0")
    repeat(120, get_stats, ip)
