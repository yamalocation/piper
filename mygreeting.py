import RPi.GPIO as GPIO
import subprocess
import time

# GPIOピンの設定
BUTTON_PIN = 24  # ボタンピン（GPIO24）

def speak_message_japanese(message):
    subprocess.run(["open_jtalk", "-m", "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice",
                    "-x", "/var/lib/mecab/dic/open-jtalk/naist-jdic",
                    "-ow", "/tmp/out.wav", "-ot", "/tmp/out.txt"],
                   input=message.encode('utf-8'))

    subprocess.run(["aplay", "/tmp/out.wav"])

def speak_japanese_message():
    current_hour = time.localtime().tm_hour

    if 7 <= current_hour < 9:
        # 7時から9時までの間は「おはよう」
        speak_message_japanese("おはよう、ひびちゃん、のんちゃん、朝起きたらまずトイレだよ")
    elif 9 <= current_hour < 10:
        # 9時から10時までの間は「出発前」
        speak_message_japanese("トイレにいったかな？忘れ物はない？ハンカチ、マスク、帽子は忘れてないかな")
    elif 15 <= current_hour < 18:
        # 15時から18時までの間は「おかえりなさい」
        speak_message_japanese("おかえりなさい、帰ったらまず手を洗うんだよ")
    elif 20 <= current_hour < 22:
        # 20時から22時までの間は「おやすみなさい」
        speak_message_japanese("寝る前に歯磨きだよ。トイレに行ったかな？パジャマに着替えるんだよ、おやすみなさい")
    else:
        # それ以外の時間は「こんにちは」
        speak_message_japanese("ひびちゃん、のんちゃん、元気にしてるかな")

def button_callback(channel):
    print("ボタンが押されました。Button Pressed!")

    # ボタンが押されたときの処理をここに追加
    speak_japanese_message()

# GPIOの初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ボタンが押されたときのコールバックを設定
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    print("ボタンを押してください。Press the button to trigger Japanese message. Press Ctrl+C to exit.")
    # メインループ
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
