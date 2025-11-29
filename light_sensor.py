# light_sensor.py

import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI

# 라즈베리파이 기본 SPI 포트/디바이스
SPI_PORT = 0
SPI_DEVICE = 0

# MCP3008 객체 생성 (하드웨어 SPI 사용)
mcp = Adafruit_MCP3008.MCP3008(
    spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE)
)

def read_light_raw():
    """MCP3008의 채널 0에서 조도 raw 값(0~1023)을 읽어서 반환."""
    return mcp.read_adc(0)

