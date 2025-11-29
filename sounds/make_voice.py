# make_voice.py
from gtts import gTTS
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def make_voice(filename, text, lang="ko"):
    path = os.path.join(BASE_DIR, filename)
    tts = gTTS(text=text, lang=lang)
    tts.save(path)
    print(f"[완료] {path} 생성됨")

if __name__ == "__main__":
    # 차량 감지 안내
    make_voice(
        "car_detected.mp3",
        "차량이 감지되었습니다. 주의해서 주차하세요."
    )

    # 너무 근접 경고
    make_voice(
        "too_close.mp3",
        "정지하세요"
    )

