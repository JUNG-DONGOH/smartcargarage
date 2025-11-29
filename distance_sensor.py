# distance_sensor.py
import time
import RPi.GPIO as GPIO

TRIG = 20
ECHO = 16

def init_distance_sensor(trig_pin: int = TRIG, echo_pin: int = ECHO):
    """초음파 센서 GPIO 초기화 후 (trig_pin, echo_pin) 반환."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    GPIO.output(trig_pin, 0)
    return trig_pin, echo_pin

def measure_distance(trig_pin: int, echo_pin: int) -> float:
    """TRIG/ECHO 핀으로부터 거리(cm)를 측정해서 리턴."""
    time.sleep(0.2)  # 센서 안정화 시간

    # 초음파 발사
    GPIO.output(trig_pin, 1)
    time.sleep(0.00001)         # 10µs 펄스
    GPIO.output(trig_pin, 0)

    # 초음파 나가는 시간
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    # 초음파 돌아오는 시간
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 340 * 100 / 2  # cm 단위
    return distance

