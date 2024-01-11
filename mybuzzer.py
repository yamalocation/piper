
import RPi.GPIO as GPIO
import requests
import subprocess
import time

# LINE Notifyのアクセストークン
# "要LINE Notifayトークン"
LINE_TOKEN = ""

# GPIOピンの設定
SENSOR_PIN = 17
BUZZER_PIN = 18

# GPIOの初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)


def send_line_notification(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + LINE_TOKEN,
    }
    payload = {"message": message}
    requests.post(url, headers=headers, data=payload)

def activate_buzzer():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    p = GPIO.PWM(BUZZER_PIN, 440) # init frequency: 50HZ
    p.start(50) # Duty cycle: 50%
    time.sleep(1)  # ブザーを鳴らす時間
    GPIO.output(BUZZER_PIN, GPIO.LOW)



def generate_warning_voice():
    subprocess.run(["open_jtalk", "-m", "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice",
                    "-x", "/var/lib/mecab/dic/open-jtalk/naist-jdic",
                    "-ow", "/tmp/warning.wav", "-ot", "/tmp/warning.txt"],
                   input="危ないです、離れてください！".encode('utf-8'))

def play_warning_voice():
    subprocess.run(["aplay", "/tmp/warning.wav"])

def main():
    try:
        print("Waiting for motion detection...")

        while True:
            if GPIO.input(SENSOR_PIN):
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                motion_data = f"接近しました {timestamp}"
                print(motion_data)

                send_line_notification(motion_data)
                activate_buzzer()
                generate_warning_voice()
                play_warning_voice()

                time.sleep(5)  # 連続して通知を防ぐために一定の時間待機
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
