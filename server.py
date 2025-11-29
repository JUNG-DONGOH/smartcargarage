# server.py
from flask import Flask, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

BROKER_IP = "localhost"
CONTROL_TOPIC = "car_garage/control"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect(BROKER_IP, 1883)
mqtt_client.loop_start()

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/start", methods=["POST"])
def start():
    mqtt_client.publish(CONTROL_TOPIC, "start")
    print("[웹] START 버튼 → MQTT start 전송")
    return ("", 204)

@app.route("/stop", methods=["POST"])
def stop():
    mqtt_client.publish(CONTROL_TOPIC, "stop")
    print("[웹] STOP 버튼 → MQTT stop 전송")
    return ("", 204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

