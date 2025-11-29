# main.py

import os
import time
import RPi.GPIO as GPIO

from sound_system import init_sound_system, play_beep_pattern, play_voice
from distance_sensor import init_distance_sensor, measure_distance
from led_system import init_leds, update_leds, led_on_off
from camera_system import init_camera_system, capture_and_save, cleanup_camera_system
from temp_sensor import init_temp_sensor, get_temperature, get_humidity
from light_sensor import read_light_raw  # ⭐ 조도센서 모듈에서 값 읽기

import mqtt_control

# 사진 촬영 최소 간격(초)
SHOT_INTERVAL = 3.0


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # ===== 1. 초기화 =====
    # 초음파 센서
    trig_pin, echo_pin = init_distance_sensor()

    # LED 핀 (led1, led2, led3)
    led1_pin, led2_pin, led3_pin = init_leds()

    # 온습도 센서
    temp_sensor = init_temp_sensor()

    # 카메라 + static 디렉토리
    camera, buffer_size, static_dir = init_camera_system(base_dir)

    # MQTT 초기화
    mqtt_control.init_mqtt()

    # 사운드 시스템
    beep, voices = init_sound_system()
    car_detected_before = False

    # 타이밍 관리 변수들
    last_shot = 0.0          # 마지막 사진 촬영 시각
    last_temp_pub = 0.0      # 마지막 온습도/조도 MQTT 전송 시각

    print("스마트 차고 시스템 시작")

    try:
        while True:
            now = time.time()

            # ===== 2. 센서 읽기 =====
            dist = measure_distance(trig_pin, echo_pin)
            temp = get_temperature(temp_sensor)
            hum  = get_humidity(temp_sensor)
            light = read_light_raw()  # ⭐ 조도(raw, 0~1023)

            # 한 줄로 상태 출력 (필요하면 light도 같이 표시)
            print(
                "온도: %4.1f °C | 습도: %4.1f %% | 거리: %5.1f cm | 조도(raw): %4d"
                % (temp, hum, dist, light)
            )

            # ===== 3. MQTT 제어 신호 (start/stop) 반영 =====
            if not mqtt_control.running:
                # P(주차) 모드: LED/사운드/촬영 모두 정지
                update_leds(led1_pin, led2_pin, led3_pin, None, temp)
                time.sleep(0.3)
                continue

            # ===== 4. LED 제어 (거리 + 온도 기반) =====
            # 여기서 temp까지 넘겨서 led_system 내부에서 TEMP_WARNING 기준으로 LED3 경고까지 처리
            update_leds(led1_pin, led2_pin, led3_pin, dist, temp)

            # ===== 5. 사운드 제어 (거리 기반) =====
            if dist <= 8.0:
                # 아주 근접: 빠른 비프 + 위험 안내
                play_beep_pattern(beep, "near")
                play_voice(voices, "too_close")
            elif dist <= 15.0:
                # 중간: 두 번 비프
                play_beep_pattern(beep, "mid")
            elif dist <= 20.0 and not car_detected_before:
                # 처음 가까워졌을 때만 안내
                play_voice(voices, "car_detected")
                car_detected_before = True
                play_beep_pattern(beep, "far")
            else:
                # 그 외는 소리 없음
                pass

            # ===== 6. 온습도/조도 MQTT 전송 (1초에 한 번 정도만) =====
            if now - last_temp_pub >= 1.0:
                mqtt_control.publish_temp_hum(temp, hum)
                mqtt_control.publish_light(light)   # ⭐ 조도값도 같이 전송
                last_temp_pub = now

            # ===== 7. 카메라 촬영 + 사진 업데이트 이벤트 =====
            if dist <= 8.0:
                # 근접 구간: SHOT_INTERVAL 간격으로 계속 촬영
                if (now - last_shot) >= SHOT_INTERVAL:
                    ok = capture_and_save(camera, buffer_size, static_dir)
                    if ok:
                        last_shot = now
                        mqtt_control.publish_photo_event()
            else:
                # 거리 멀어지면 그냥 last_shot만 유지 (초기화 필요 없음)
                pass

    except KeyboardInterrupt:
        print("\n[종료] 사용자에 의해 종료됨")

    finally:
        # LED 끄기
        led_on_off(led1_pin, 0)
        led_on_off(led2_pin, 0)
        led_on_off(led3_pin, 0)

        # GPIO, 카메라, MQTT 정리
        GPIO.cleanup()
        cleanup_camera_system(camera)
        mqtt_control.cleanup_mqtt()
        print("[정리 완료] GPIO / 카메라 / MQTT 종료")


if __name__ == "__main__":
    main()

