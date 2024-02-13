from stt import listen_write_word
from tts import speak
from with_selenium import search_word, search_play_music, rank_news, stock_price
from with_weather import weather_info, fine_dust_info, estimate_temperature
from word_connection_game import Game
from datetime import datetime
from schedule_management import ScheduleManager


class Secretary:
    def __init__(self, name):
        self.name = name

    # 이름 인식
    def recognize_name(self):
        while True:
            name = listen_write_word()
            if name:
                if self.name in name:
                    speak("무엇을 도와드릴까요?")
                    return

    # ‘~ 검색’ 라고 말할 경우, 해당 단어를 검색
    def search_word_from_command(self, command):
        word_to_find = command.split('검색')[0].strip()
        search_word(word_to_find)

    # 현재 서울의 날씨, 기온, 풍속 알림
    def inform_weather(self):
        curr_weather, curr_temperater, curr_wind_speed = weather_info()
        speak(f"현재 서울의 날씨는 {curr_weather} 입니다.")
        speak(f"기온은 {curr_temperater}도 이고, 풍속은 {curr_wind_speed} 미터 퍼 세크 입니다.")

    # 현재 서울의 미세먼지/초미세먼지 상태 알림
    def inform_fine_dust(self):
        pm10_state, pm25_state = fine_dust_info()
        speak(f"현재 미세먼지는 {pm10_state} 이며, 초미세먼지는 {pm25_state} 입니다.")

    # 끝말 잇기 게임
    def play_word_connection_game(self):
        player = Game()
        player.start_game()

    # 해당 노래 검색 및 재생
    def search_music_from_command(self, command):
        word_to_find = command.split("틀어")[0].strip()
        search_play_music(word_to_find)
        '''
        노래를 정지하는 기능을 넣으려 하였으나, 노래 소리에 시리가 인식을 못 함
        '''

    # 뉴스 알림
    def inform_news(self):
        press_name, content_list = rank_news()
        speak(f"{press_name} 뉴스 입니다.")
        for index, content in enumerate(content_list):
            speak(f"{index+1}위 뉴스")
            speak(content)

    # 주가 정보 알림
    def inform_stock(self, command):
        try:
            if "코스피" in command:
                word_to_find = "코스피"
            elif "코스닥" in command:
                word_to_find = "코스닥"
            else:
                word_to_find = command.split('주')[0].strip()
            price = stock_price(word_to_find)
            speak(f"{word_to_find} 주가는 {price}원 입니다.")
        except AttributeError:
            speak("해당 주식 정보를 찾을 수 없습니다")

    # 올해 기온 변화 예측
    def inform_temperature_estimate(self):
        speak("올해 기온 예측치는 화면을 참고하세요")
        estimate_temperature(datetime.now().year)

    # 음성인식 비서 프로그램 실행
    def play_program(self):
        while True:
            self.recognize_name()
            while True:
                command = listen_write_word()
                if command: break
            if "검색" in command:
                self.search_word_from_command(command)
            elif True in [True if condition in command else False for condition in ['날씨', '기온', '풍속']]:
                self.inform_weather()
            elif "먼지" in command:
                self.inform_fine_dust()
            elif "틀어" in command:
                self.search_music_from_command(command)
            elif "게임" in command:
                self.play_word_connection_game()
            elif ("뉴스" in command) or ("기사" in command):
                self.inform_news()
            elif ("기후" in command) and ("예측" in command):
                self.inform_temperature_estimate()
            elif True in [True if condition in command else False for condition in ['주식', '주가', '코스피', '코스닥']]:
                self.inform_stock(command)
            elif "일정" in command:
                schedule_manager = ScheduleManager()
                schedule_manager.execute_shedule_manager()
            elif True in [True if condition in command else False for condition in ["종료", "그만", "끝"]]:
                speak("음성인식 비서 물러가겠습니다")
                break

