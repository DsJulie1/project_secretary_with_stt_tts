from tts import speak
from stt import listen_write_word
import requests
import json
import random
import os
import pickle

from pprint import pprint
# pprint : json 형식의 데이터를 깔끔하게 출력해주는 함수


class Game:
    def __init__(self):
        self.min_length = 2
        self.max_length = 3
        self.turn = 1
        self.curr_word = None
        self.word_list = []

    # 글자 수 2개 이상인지 여부 확인
    def check_length(self, word):
        return len(word) >= 2

    # 표준국어대사전 데이터에 접근
    def access_dictionary(self, word, method, num=None, advanced='n'):
        url = 'https://opendict.korean.go.kr/api/search'
        params = {
            'key': '인증키 삽입 필요',
            'q': word,
            'num' : num,
            'start' : 1,
            'req_type': 'json',
            'part': 'word',
            'sort' : 'popular',
            'target': 1,
            'method': method,
            'type3': 'general',
            'pos': 1,
            'letter_s' : self.min_length,
            'letter_e': self.max_length,
            "advanced": advanced
        }

        os.environ['CURL_CA_BUNDLE'] = ''  # 인증 문제 해결을 위한 코드(+requests 다운그레이드)
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        return data

    # 표준국어대사전에 있는지 여부 확인
    def check_is_in_dictionary(self, word):
        data = self.access_dictionary(word, method='exact')
        check = int(data['channel']['total'])
        return check

    # 두음법칙 적용
    def apply_word_principle(self, word):
        with open("word_principle_dict.pkl", "rb") as f:
            word_principle_dict = pickle.load(f)

        if word in word_principle_dict.keys():
            word = word_principle_dict[word]
        return word

    # 사용자 단어 입력
    def input_with_validation(self):
        speak("단어를 말씀해주세요")
        while True:
            while True:
                word = listen_write_word()
                if word: break
            if ("그만" in word) or ("종료" in word) or ("끝" in word):
                return word

            # 사전에 있는 단어 인지, 2음절 이상의 단어인지, 이전에 말한 단어는 아닌지, 끝말을 이은 단어인지 확인
            connetion_condition = True if (not self.curr_word) else (word[0] == self.apply_word_principle(self.curr_word[-1]))
            if (self.check_is_in_dictionary(word)) and (self.check_length(word)) and (word not in self.word_list) and connetion_condition:
                self.curr_word = word
                self.word_list.append(word)
                return word
            else:
                speak("다시 말씀해주세요")

    # 음성 비서 단어 입력
    def connect_word(self, starging_word):
        data = self.access_dictionary(starging_word, method='start', num=100, advanced="y")
        while True:
            while True:
                try:
                    word = data['channel']['item'][random.randint(0, 99)]['word']
                except IndexError:
                    pass
                except TypeError:
                    pass
                else: break

            if word not in self.word_list:
                self.word_list.append(word)
                speak(word)
                return word

    # 끝말 잇기 게임 실행
    def start_game(self):
        speak("끝말 잇기 게임을 시작합니다")
        while True:
            word = self.input_with_validation() if self.turn else self.connect_word(self.apply_word_principle(self.curr_word[-1]))
            if ("그만" in word) or ("종료" in word) or ("끝" in word):
                speak("게임을 종료합니다")
                break
            print(f"사용자 입력 단어 : {word}") if self.turn else print(f"음성인식 비서 입력 단어 : {word}")
            self.curr_word = word
            print(f"언급된 단어들 : {self.word_list}")
            self.turn = not self.turn

if __name__ == "__main__":
    instance = Game()
    instance.start_game()