# mqtt_control.py
import paho.mqtt.client as mqtt

# ---------------------------
# MQTT 브로커 설정
# ---------------------------
BROKER_IP = "localhost"
BROKER_PORT = 1883

# ---------------------------
# MQTT 토픽 정의
# ---------------------------
CONTROL_TOPIC      = "car_garage/control"        # start/stop 제어용
TEMP_HUM_TOPIC     = "car_garage/temp_hum"       # 온도, 습도
PHOTO_EVENT_TOPIC  = "car_garage/photo_updated"  # 사진 갱신 이벤트
LIGHT_TOPIC        = "car_garage/light"          # 조도 센서 값

# ---------------------------
# 전역 상태
# ---------------------------
running = True   # start/stop 제어 플래그
client = None    # MQTT 클라이언트 핸들


# ---------------------------
# 콜백 함수들
# ---------------------------
def on_connect(client_, userdata, flags, rc, properties=None):
    """MQTT 브로커에 연결되었을 때 호출."""
    print(f"[MQTT] Connected (rc={rc})")
    # 제어 토픽 구독
    client_.subscribe(CONTROL_TOPIC)
    print(f"[MQTT] Subscribed: {CONTROL_TOPIC}")


def on_message(client_, userdata, msg):
    """CONTROL_TOPIC에서 start/stop 신호를 받을 때 호출."""
    global running
    payload = msg.payload.decode().strip().lower()
    print(f"[MQTT] 수신: topic={msg.topic}, payload={payload}")

    if msg.topic == CONTROL_TOPIC:
        if payload == "stop":
            running = False
            print("[MQTT] → 시스템 정지 (running = False)")
        elif payload == "start":
            running = True
            print("[MQTT] → 시스템 동작 (running = True)")


# ---------------------------
# 초기화 / 종료
# ---------------------------
def init_mqtt():
    """MQTT 클라이언트를 초기화하고 loop_start까지 수행."""
    global client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_IP, BROKER_PORT)
    client.loop_start()
    print("[MQTT] init_mqtt() 완료")
    return client


def cleanup_mqtt():
    """MQTT 클라이언트 정리."""
    global client
    if client is None:
        return
    try:
        client.loop_stop()
        client.disconnect()
        print("[MQTT] MQTT 연결 종료")
    except Exception as e:
        print("[MQTT] 종료 중 예외:", e)
    client = None


# ---------------------------
# Publish 함수들
# ---------------------------
def publish_temp_hum(temp: float, hum: float):
    """
    온도/습도 값을 TEMP_HUM_TOPIC으로 전송.
    temp: 섭씨 온도 (float)
    hum : 상대습도 % (float)
    """
    if client is None:
        return
    payload = f"{temp:.1f},{hum:.1f}"  # 예: "24.3,40.5"
    client.publish(TEMP_HUM_TOPIC, payload, qos=0)
    # print(f"[MQTT] 온습도 전송: {payload}")


def publish_photo_event():
    """
    사진이 새로 저장되었다는 '이벤트'만 전송.
    실제 이미지 데이터는 전송하지 않고, 웹이 이 신호를 받으면
    /static/last_shot.jpg 를 새로 로딩하도록 구현.
    """
    if client is None:
        return
    client.publish(PHOTO_EVENT_TOPIC, "updated", qos=0)
    print("[MQTT] 사진 업데이트 이벤트 전송")


def publish_light(light_value):
    """
    조도 센서 raw 값(예: 0~1023)을 LIGHT_TOPIC으로 전송.
    light_value: ADC에서 읽은 정수값
    """
    if client is None:
        return
    client.publish(LIGHT_TOPIC, str(light_value), qos=0)
    # print(f"[MQTT] 조도 전송: {light_value}")

