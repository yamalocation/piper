import requests

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # セ氏温度で取得する場合
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            # 天気情報の取得
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']

            print(f'天気: {weather_description}')
            print(f'気温: {temperature} ℃')
            print(f'湿度: {humidity} %')
        else:
            print(f'エラー: {data["message"]}')
    except Exception as e:
        print(f'エラー: {e}')

if __name__ == "__main__":
    # OpenWeatherMap APIキーと対象の都市を指定してください
    # '要OpenWeatheのトークン'
    api_key = ''
    city = 'Chiba'

    get_weather(api_key, city)
