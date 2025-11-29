# sound_system.py
import os
import time
import pygame

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")

# ===== 1. 초기화 함수 =====
def init_sound_system():
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    # 비프음 로드
    beep_path = os.path.join(BASE_DIR, "beep.wav")
    if not os.path.exists(beep_path):
        raise FileNotFoundError(f"beep.wav를 찾을 수 없습니다: {beep_path}")
    beep_sound = pygame.mixer.Sound(beep_path)

    # 음성 파일 로드 (경로만 저장)
    voice_files = {
        "car_detected": os.path.join(BASE_DIR, "car_detected.mp3"),
        "too_close": os.path.join(BASE_DIR, "too_close.mp3"),
    }

    # 파일 존재 여부 체크(없어도 프로그램은 계속 돌아가게만 경고)
    for name, path in voice_files.items():
        if not os.path.exists(path):
            print(f"[경고] {name} 음성 파일이 없습니다: {path}")

    return beep_sound, voice_files


# ===== 2. 비프 패턴 =====
def play_beep_pattern(beep_sound, level: str):
    """
    level:
      - "far"  : 한 번 천천히 삐—
      - "mid"  : 두 번 중간 속도 삐삐—
      - "near" : 세 번 빠르게 삐삐삐—
    """
    if level == "far":
        count = 1
        interval = 0.4
    elif level == "mid":
        count = 2
        interval = 0.25
    elif level == "near":
        count = 3
        interval = 0.15
    else:
        count = 1
        interval = 0.4

    for _ in range(count):
        beep_sound.play()
        time.sleep(beep_sound.get_length() + interval)


# ===== 3. 음성 안내 재생 =====
def play_voice(voice_files, name: str):
    """
    name: "car_detected", "too_close" 등
    """
    path = voice_files.get(name)
    if not path or not os.path.exists(path):
        print(f"[경고] '{name}' 음성 파일이 없어 재생할 수 없습니다.")
        return

    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    # 재생이 끝날 때까지 대기
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)


# ===== 4. 단독 실행 테스트 =====
if __name__ == "__main__":
    print("[시작] 사운드 시스템 초기화")
    beep, voices = init_sound_system()
    print("[완료] 초기화 성공")

    try:
        # 1) 차량 감지: 안내 + far 비프
        print("\n[테스트] 차량 감지: 음성 + far 비프")
        play_voice(voices, "car_detected")
        play_beep_pattern(beep, "far")
        time.sleep(1)

        # 2) 중간 거리: mid 비프
        print("\n[테스트] 중간 거리: mid 비프")
        play_beep_pattern(beep, "mid")
        time.sleep(1)

        # 3) 근접: near 비프 + 위험 안내
        print("\n[테스트] 근접: near 비프 + 위험 안내")
        play_beep_pattern(beep, "near")
        play_voice(voices, "too_close")

        print("\n[테스트 종료]")

    except KeyboardInterrupt:
        print("\n[중단] 사용자에 의해 종료됨")
    finally:
        pygame.mixer.quit()

