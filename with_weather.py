import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

# weather_code 설명
weather_variable = {
    0 : '맑은 하늘',
    1 : '대체로 맑음',
    2 : '부분적으로 흐림',
    3 : '흐림',
    45 : '안개',
    48 : '빙무 퇴적',
    51 : '약한 이슬비',
    53 : '보통의 이슬비',
    55 : '짙은 강도의 이슬비',
    56 : '가벼운 강도의 얼어붙는 이슬비',
    57 : '짙은 강도의 얼어붙는 이슬비',
    61 : '약한 비',
    63 : '보통의 비',
    65 : '심한 강도의 비',
    66 : '가벼운 강도의 얼어붙는 비',
    67 : '강한 강도의 얼어붙는 비',
    71 : '약한 강설량',
    73 : '보통의 강설량',
    75 : '강한 강설량',
    77 : '눈알',
    80 : '약한 소나기',
    81 : '보통의 소나기',
    82 : '격렬한 소나기',
    85 : '가벼운 소나기',
    86 : '가벼운 소나기'
}

# 현재 날씨, 기온, 풍속 정보
def weather_info():
    url = 'https://api.open-meteo.com/v1/forecast?latitude=37.566&longitude=126.9784&current_weather=true'
    response = requests.get(url)
    data = json.loads(response.text)

    weather_code = int(data['current_weather']['weathercode'])
    curr_weather = weather_variable[weather_code]
    curr_temperature = data['current_weather']['temperature']
    curr_wind_speed = data['current_weather']['windspeed']
    return curr_weather, curr_temperature, curr_wind_speed

# 미세먼지 기준에 따른 상태 정보
def pm10_state_info(pm10):
    try:
        pm10 = int(pm10)
    except ValueError:
        pm10_state = '정보 없음'
    else:
        if 0 <= pm10 <= 30:
            pm10_state = "좋음"
        elif 31 <= pm10 <= 50:
            pm10_state = "보통"
        elif 51 <= pm10 <= 100:
            pm10_state = "나쁨"
        elif pm10 >= 101:
            pm10_state = "매우 나쁨"
        else:
            pm10_state = "정보 없음"
    return pm10_state

# 초미세먼지 기준에 따른 상태 정보
def pm25_state_info(pm25):
    try:
        pm25 = int(pm25)
    except ValueError:
        pm25_state = "정보 없음"
    else:
        if 0 <= pm25 <= 15:
            pm25_state = "좋음"
        elif 16 <= pm25 <= 25:
            pm25_state = "보통"
        elif 26 <= pm25 <= 50:
            pm25_state = "나쁨"
        elif pm25 >= 51:
            pm25_state = "매우 나쁨"
        else:
            pm25_state = "정보 없음"
    return pm25_state

# 현재 서울 미세먼지 정보
def fine_dust_info():
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
    params = {
        'serviceKey': '인증키 삽입 필요',
        'returnType': 'json',
        'numOfRows': '100',
        'pageNo': '1',
        'sidoName': '서울',
        'ver': '1.0',
    }
    region = '도봉구'
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    info_list = data['response']['body']['items']

    for info in info_list:
        if info['stationName'] == region:
            pm10_state = pm10_state_info(info['pm10Value'])
            pm25_state = pm25_state_info(info['pm25Value'])
            return pm10_state, pm25_state

# 서울의 기온 예측
def estimate_temperature(year):
    url = f'https://climate-api.open-meteo.com/v1/climate?latitude=37.566&longitude=126.9784&start_date={year}-01-01&end_date={year}-12-31&models=CMCC_CM2_VHR4&daily=temperature_2m_max'
    response = requests.get(url)
    temperature = json.loads(response.text)['daily']['temperature_2m_max']
    date = json.loads(response.text)['daily']['time']
    df_temperature = pd.DataFrame(temperature)
    df_date = pd.DataFrame(date)
    df = pd.concat([df_date, df_temperature], axis=1)
    df.columns = ['date', 'temperature']
    print(df)
    df.plot(kind='line', x='date', y='temperature')
    plt.title(f"Maximum daily air temperature at 2 meters above ground({year} year)")
    plt.show()


if __name__ == "__main__":
    estimate_temperature('2023')
