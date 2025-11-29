import RPi.GPIO as GPIO

LED1 = 6
LED2 = 5
LED3 = 13

TEMP_WARNING = 28.0   

def init_leds(led1_pin=LED1, led2_pin=LED2, led3_pin=LED3):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led1_pin, GPIO.OUT)
    GPIO.setup(led2_pin, GPIO.OUT)
    GPIO.setup(led3_pin, GPIO.OUT)
    GPIO.output(led1_pin,0)
    GPIO.output(led2_pin,0)
    GPIO.output(led3_pin,0)
    return led1_pin, led2_pin, led3_pin

def led_on_off(pin, value):
    GPIO.output(pin, value)

def update_leds(led1_pin, led2_pin, led3_pin, dist, temp):
    # 1) 온도 경고 우선 처리
    if temp is not None and temp >= TEMP_WARNING:
        GPIO.output(led1_pin, 0)
        GPIO.output(led2_pin, 0)
        GPIO.output(led3_pin, 1)
        return

    # 2) 온도 정상일 때는 거리 기반 패턴
    if dist is None:
        GPIO.output(led1_pin, 0)
        GPIO.output(led2_pin, 0)
        GPIO.output(led3_pin, 0)
    elif dist <= 8.0: # 위험 LED불 3개
        GPIO.output(led1_pin, 1)
        GPIO.output(led2_pin, 1)
        GPIO.output(led3_pin, 1)
    elif dist <= 15.0: # 중간 LED불 2개
        GPIO.output(led1_pin, 1)
        GPIO.output(led2_pin, 1)
        GPIO.output(led3_pin, 0)
    elif dist <= 20.0: # 안전 LED불 1개
        GPIO.output(led1_pin, 1)
        GPIO.output(led2_pin, 0)
        GPIO.output(led3_pin, 0)
    else:
        GPIO.output(led1_pin, 0)
        GPIO.output(led2_pin, 0)
        GPIO.output(led3_pin, 0)

