# temp_sensor.py
import time
import busio
from adafruit_htu21d import HTU21D
import board

def init_temp_sensor():
    # board.SCL, board.SDA가 더 표준적이라 이걸 권장
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = HTU21D(i2c)
    return sensor

def get_temperature(sensor):
    return float(sensor.temperature)

def get_humidity(sensor):
    return float(sensor.relative_humidity)

