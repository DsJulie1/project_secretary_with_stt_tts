from gtts import gTTS
import playsound
import os

def speak(text):
	tts = gTTS(text=text, lang='ko') # 함수 인자로 들어온 text 를 음성으로 변환
	tts.save('voice.mp3') # 변환된 음성을 voice.mp3 라는 이름으로 저장
	playsound.playsound('voice.mp3') # 저장한 음성 파일을 재생
	os.remove('voice.mp3') # 재생 후에는 해당 파일 삭제

if __name__ == "__main__":
    speak('안녕하세요') # 코드가 실행되면, 컴퓨터가 안녕하세요 라고 말하는 것을 들을 수 있습니다!