# camera_system.py
import os
import cv2

def init_camera_system(base_dir: str):
    """
    카메라와 static 디렉토리 초기화.
    (camera, buffer_size, static_dir) 반환.
    """
    static_dir = os.path.join(base_dir, "static")
    os.makedirs(static_dir, exist_ok=True)

    camera = cv2.VideoCapture(0, cv2.CAP_V4L)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    buffer_size = 1
    camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

    return camera, buffer_size, static_dir

def capture_and_save(camera, buffer_size: int, static_dir: str):
    """
    최신 프레임을 캡처해서
    - static/last_shot.jpg 로 저장하고
    - MQTT 전송용 JPEG 바이트를 리턴.
    실패 시 None 리턴.
    """
    # 버퍼 비우고 최신 프레임 확보
    for _ in range(buffer_size + 1):
        ret, frame = camera.read()

    if not ret:
        print("[카메라] 프레임 캡처 실패")
        return None

    ok, encoded = cv2.imencode(".jpg", frame)
    if not ok:
        print("[카메라] JPEG 인코딩 실패")
        return None

    im_bytes = encoded.tobytes()

    img_path = os.path.join(static_dir, "last_shot.jpg")
    cv2.imwrite(img_path, frame)
    print("[카메라] 이미지 저장:", img_path)

    return im_bytes

def cleanup_camera_system(camera):
    """카메라만 정리."""
    try:
        camera.release()
    except Exception:
        pass

