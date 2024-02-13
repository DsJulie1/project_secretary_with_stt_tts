from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tts import speak

# 사이트 켜지는 것을 보이지 않게 하기 위한 옵션
headless_options = Options()
headless_options.add_argument("--headless")
# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


# Selenium 활용하여 사이트에 접근
def access_site(url, options=None):
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get(url)
    time.sleep(1)
    return driver

# 네이버에서 단어 검색
def search_word(word):
    url = 'https://www.naver.com/'
    driver = access_site(url, chrome_options)
    driver.find_element(By.CSS_SELECTOR, '#query').send_keys(word)
    driver.find_element(By.CSS_SELECTOR, '#search-btn').click()

# 지니뮤직에서 해당 노래 검색 및 재생
def search_play_music(word):
    url = 'https://www.genie.co.kr/'
    driver = access_site(url, headless_options)
    # 해당 곡 검색
    driver.find_element(By.CSS_SELECTOR, '#sc-fd').send_keys(word)
    driver.find_element(By.CSS_SELECTOR, '.btn-submit').click()
    time.sleep(1)
    # 해당 곡 있는 경우 재생
    try:
        driver.find_element(By.CSS_SELECTOR, '#body-content > div.search_song > div.search_result_detail > div > div:nth-child(1) > input').click()
        driver.find_element(By.CSS_SELECTOR, '#body-content > div.search_song > div.search_result_detail > div > div:nth-child(1) > a.btn.btn-listen').click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.fp-playbtn').click()
        continue_music(driver)
    except:
        speak("해당 곡이 없네요")

# 해당 노래 시간까지 기다리기
def continue_music(driver):
    music_time_str = driver.find_element(By.CSS_SELECTOR, '.fp-duration').text
    # 노래 시간을 selenium으로 가져와 그만큼 sleep
    time.sleep(int(music_time_str[1]) * 60 + int(music_time_str[-2:]) + 2)

# 랭킹 뉴스
def rank_news():
    url ='https://news.naver.com/main/ranking/popularDay.naver'
    driver = access_site(url, headless_options)
    press_name = driver.find_element(By.CSS_SELECTOR, '#wrap > div.rankingnews._popularWelBase._persist > div.rankingnews_box_wrap._popularRanking > div > div:nth-child(1) > a > strong').text
    content_tags = driver.find_elements(By.CSS_SELECTOR, '.list_content > a')
    content_list = [content_tags[i].text for i in range(5)]
    return press_name, content_list

# 주가 확인
def stock_price(company):
    url = 'http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd'
    driver= access_site(url, headless_options)
    driver.find_element(By.CSS_SELECTOR, '#jsTotSch').send_keys(company)
    driver.find_element(By.CSS_SELECTOR, '#jsTotSchBtn').click()
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    if (company == "코스피") or (company == "코스닥"):
        price_full = soup.select_one("#jsIdxInfo > span").text
    else:
        # 해당 회사의 주가 확인
        price_full = soup.select_one("#isuInfoTitle > span").text

    price = price_full.split('▲')[0].strip()
    price = price.split('▼')[0].strip()
    return price

