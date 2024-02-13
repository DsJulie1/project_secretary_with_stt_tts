from tts import speak
from stt import listen_write_word
from datetime import datetime
import pickle
import os

class ScheduleManager:
    def __init__(self):
        self.schedule_dic = {}
        self.file_path = 'schedule_dic.pkl'

    # 데이터 가져오기
    def load_data(self):
        with open(self.file_path, 'rb') as f:
            self.schedule_dic = pickle.load(f)

    # 날짜 입력하기
    def input_date(self):
        speak("날짜를 말씀해주세요")
        while True:
            try:
                date = listen_write_word()
                if ("월" in date) and ("일" in date):
                    if "년" not in date:
                        year = int(datetime.now().year)
                        month = int(date.split("월")[0].strip())
                        day = int(date.split("월")[1].split("일")[0].strip())
                    else:
                        year = int(date.split("년")[0].strip())
                        month = int(date.split("년")[1].split("월")[0].strip())
                        day = int(date.split("년")[1].split("월")[1].split("일")[0].strip())
                    return f"{year}년 {month}월 {day}일"
                elif "오늘" in date:
                    return f"{datetime.now().year}년 {datetime.now().month}월 {datetime.now().day}일"
                elif "잘못" in date:
                    speak("이전 메뉴로 넘어갑니다")
                    return
                else:
                    speak("날짜를 정확히 말씀해주세요")
            except TypeError:
                pass
            except ValueError:
                speak("날짜를 정확히 말씀해주세요")

    # 스케줄 추가하기
    def add_schedule(self, command):
        schedule = command.split('일정')[0].strip()
        date = self.input_date()
        if not date: return
        try:
            self.schedule_dic[date]
        except KeyError:
            self.schedule_dic[date] = []
        finally:
            self.schedule_dic[date].append(schedule)
        speak("일정 등록을 완료했습니다")

    # 일정 알려주기
    def inform_schedule(self):
        date = self.input_date()
        if not date: return
        if date in self.schedule_dic.keys():
            schedule = self.schedule_dic[date]
            speak(f"{date} 일정은 {schedule} 입니다")
        else:
            speak(f"{date}의 일정은 없습니다")

    # 전체 일정 알려주기
    def inform_total_schedule(self):
        if not self.schedule_dic:
            speak("일정이 없습니다")
        else:
            for key in self.schedule_dic.keys():
                speak(f"{key} 일정은")
                for schedule in self.schedule_dic[key]:
                    speak(schedule)
                speak("입니다.")

    # 일정 삭제하기
    def delete_schedule(self):
        date = self.input_date()
        if not date: return
        if date not in self.schedule_dic.keys():
            speak("해당 날짜에는 일정이 없습니다")
            return
        # 해당 날짜의 일정 중 인덱스 확인 및 삭제
        speak("몇 번째 일정을 삭제 하실 건가요?")
        while True:
            # 말하지 않아도 기다려주기
            while True:
                try:
                    index_command = listen_write_word()
                except TypeError:
                    pass
                else:
                    break
            # 이전 메뉴로 넘어가기
            if "잘못" in index_command:
                speak("이전 메뉴로 넘어갑니다")
                return

            # 인덱스 확인
            num_dic = {"첫":0, "두":1, "세":2, "네":3, "다섯":4, "여섯":5}
            for key in num_dic.keys():
                if key in index_command:
                    index = num_dic[key]
            # 일정 삭제
            try:
                speak(f"{self.schedule_dic[date][index]} 일정을 삭제했습니다")
                del self.schedule_dic[date][index]
                if not self.schedule_dic[date]:
                    self.schedule_dic.pop(date)
            # 올바르지 않게 인덱스 말한 경우
            except IndexError:
                speak("정확한 인덱스를 말씀해주세요")
            else:break

    # 일정 데이터 저장
    def save_schedule(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.schedule_dic, f)
        speak("일정 저장을 완료했습니다")

    # 일정 관리 프로그램 실행
    def execute_shedule_manager(self):
        speak("일정 관리 프로그램 입니다.")

        # 일정 정보 담긴 파일 있는 경우 데이터 가져오기
        if os.path.exists(self.file_path):
            self.load_data()
        # 프로그램 실행
        while True:
            try:
                command = listen_write_word()
                if ("추가" in command) or ("등록" in command):
                    self.add_schedule(command)
                elif ("전체" in command) and ("일정" in command):
                    self.inform_total_schedule()
                elif ("일정" in command) and (("알려" in command) or ("말해") in command):
                    self.inform_schedule()
                elif "삭제" in command:
                    self.delete_schedule()
                elif ("종료" in command) or ("그만" in command):
                    self.save_schedule()
                    speak("프로그램을 종료합니다")
                    break
            except TypeError:
                pass


if __name__ == "__main__":
    instance = ScheduleManager()
    instance.execute_shedule_manager()
    print(instance.schedule_dic)