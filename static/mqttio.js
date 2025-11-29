// static/mqtt_chart.js

const MQTT_HOST = location.hostname;
const MQTT_PORT = 9001;  // mosquitto 웹소켓 포트

const TOPIC_TEMP_HUM    = "car_garage/temp_hum";
const TOPIC_PHOTO_EVENT = "car_garage/photo_updated";
const TOPIC_LIGHT       = "car_garage/light";    // 조도센서 토픽

// 온도 경고 임계값
const TEMP_WARNING = 28.0;

// 상태 변수들
let tempAlerted = false;
let mqttClient = null;

let latestTemp = null;
let latestHum  = null;
let latestLight = null;

// ==========================
// 사진 새로고침
// ==========================
function refreshPhoto() {
    const img = document.getElementById("snapshot");
    if (!img) return;
    img.src = "/static/last_shot.jpg?t=" + new Date().getTime();
}

// ==========================
// 온도 경고 팝업
// ==========================
function checkTempWarning(temp) {
    if (temp >= TEMP_WARNING && !tempAlerted) {
        alert("🔥 화재 위험! 온도가 너무 높습니다.\n현재 온도: " + temp + "°C");
        tempAlerted = true;
    }
    else if (temp < TEMP_WARNING -0.3) {
        tempAlerted = false;
    }
}

// ==========================
// 조도 기반 라이트/다크 모드
// ==========================
let currentTheme = "light";
const DARK_TH  = 300;   // 이 값보다 낮으면 어둡다고 판단
const LIGHT_TH = 400;   // 이 값보다 높으면 밝다고 판단

// 테마 변경 최소 간격 (ms)
const THEME_MIN_INTERVAL = 2000;
let lastThemeChange = 0;

function handleLight(raw) {
    const light = Number(raw);
    if (isNaN(light)) return;

    latestLight = light;
   // console.log("[Light] 조도값:", light);

    if (light < DARK_TH && currentTheme !== "dark") {
        setTheme("dark");
    }
    else if (light > LIGHT_TH && currentTheme !== "light") {
        setTheme("light");
    }
}

function setTheme(theme) {
    const now = Date.now();
    if (now - lastThemeChange < THEME_MIN_INTERVAL) {
        // 2초 안에 여러 번 바뀌는 것 방지
        return;
    }

    lastThemeChange = now;
    currentTheme = theme;

    const body = document.body;

    if (theme === "dark") {
        body.classList.remove("light-mode");
        body.classList.add("dark-mode");
    } else {
        body.classList.remove("dark-mode");
        body.classList.add("light-mode");
    }
}

// ==========================
// MQTT 초기화
// ==========================
function initMQTT() {
    mqttClient = new Paho.MQTT.Client(
        MQTT_HOST,
        Number(MQTT_PORT),
        "webclient_" + Math.floor(Math.random() * 10000)
    );

    mqttClient.onConnectionLost = function (responseObject) {
        console.log("[MQTT] 연결 끊김:", responseObject.errorMessage);
    };

    mqttClient.onMessageArrived = function (message) {
        const topic = message.destinationName;
        const payload = message.payloadString;

        if (topic === TOPIC_TEMP_HUM) {
            const parts = payload.split(",");
            if (parts.length >= 2) {
                latestTemp = parseFloat(parts[0]);
                latestHum  = parseFloat(parts[1]);

                if (!isNaN(latestTemp)) {
                    checkTempWarning(latestTemp);
                }
            }
        }
        else if (topic === TOPIC_PHOTO_EVENT) {
            refreshPhoto();
        }
        else if (topic === TOPIC_LIGHT) {
            handleLight(payload);
        }
    };

    mqttClient.connect({
        onSuccess: function () {
            console.log("[MQTT] 웹 클라이언트 연결 성공");
            mqttClient.subscribe(TOPIC_TEMP_HUM);
            mqttClient.subscribe(TOPIC_PHOTO_EVENT);
            mqttClient.subscribe(TOPIC_LIGHT);
        },
        onFailure: function (err) {
            console.log("[MQTT] 연결 실패:", err.errorMessage);
        }
    });
}

// ==========================
// 초기 실행
// ==========================
window.addEventListener("load", function () {
    drawCharts();
    initMQTT();

    setInterval(function () {
        if (latestTemp !== null && latestHum !== null) {
            addTempHumData(latestTemp, latestHum);
        }
    }, 1000);
});


