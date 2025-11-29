# make_beep.py
import math
import wave
import struct
import os

def make_beep(filename="beep.wav",
              duration=0.2,   # 초
              freq=1000,      # Hz
              volume=0.5,     # 0.0 ~ 1.0
              sample_rate=44100):  # Hz

    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, filename)

    num_samples = int(sample_rate * duration)

    with wave.open(path, "w") as wav_file:
        wav_file.setnchannels(1)      # 모노
        wav_file.setsampwidth(2)      # 16비트
        wav_file.setframerate(sample_rate)

        for i in range(num_samples):
            t = i / sample_rate
            sample = volume * math.sin(2 * math.pi * freq * t)
            value = int(sample * 32767)  # 16비트 정수로 변환
            data = struct.pack("<h", value)
            wav_file.writeframesraw(data)

    print(f"[완료] {path} 생성됨")

if __name__ == "__main__":
    make_beep()

