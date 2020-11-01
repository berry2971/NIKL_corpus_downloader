### import libs
import time
import random
import os
import getpass
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from bs4 import BeautifulSoup as bs4

from pkg.init import *

### global vars
MAX_SLEEP_SEC = 3
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
NIKL_ITHUB_MAIN = 'https://ithub.korean.go.kr/user/main.do'
NIKL_ITHUB_CORPUS = 'https://ithub.korean.go.kr/user/total/database/corpusManager.do'
NIKL_ITHUB_ID = ''
NIKL_ITHUB_PW = ''
DOWNLOAD_OPTION = set()

# functions
def sleep_random():
    rand = random.random() * MAX_SLEEP_SEC
    time.sleep(rand)

def get_loginned_page():
    driver.get(NIKL_ITHUB_MAIN)
    sleep_random()
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul/li[1]/a').click()
    driver.find_element_by_xpath(
        '/html/body/form[2]/div/div[1]/fieldset/ul/li[1]/input').send_keys(NIKL_ITHUB_ID)
    driver.find_element_by_xpath(
        '/html/body/form[2]/div/div[1]/fieldset/ul/li[2]/input').send_keys(NIKL_ITHUB_PW)
    driver.find_element_by_xpath(
        '/html/body/form[2]/div/div[1]/div/a[1]').click()

    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        print('계정 정보가 잘못되었습니다.')
        set_login_info()
        get_loginned_page()
    except:
        pass

def press_next_button():
    next_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/form/div/div[8]/div/div[1]/a[3]')))
    next_btn.click()
        
### logic
# show welcome msg
print()
print('Automated downloader for corpus database in NIKL')
print('Version: 2.01, Last Updated: 2020. 7. 28')
print('업데이트 다운로드: https://www.github.com/berry2971')
print()
print('코퍼스 데이터베이스 원위치: 국립국어원 언어정보나눔터 > 데이터베이스 자료 > 말뭉치 파일')
print('주의사항: 자동으로 실행되는 크롬 인터넷 브라우저를 절대로 임의로 조작하거나 종료하지 마세요.')
print()

# get id and pw
def set_login_info():
    global NIKL_ITHUB_ID
    global NIKL_ITHUB_PW
    print('국립국어원 아이디와 비밀번호를 입력해주세요.')
    NIKL_ITHUB_ID = input('ID: ')
    NIKL_ITHUB_PW = getpass.getpass('PW: ')
    print()

set_login_info()

# get download option
DOWNLOAD_OPTION = get_download_option()

# open driver
driver = webdriver.Chrome(ABS_PATH + r'\chromedriver.exe')

# login
get_loginned_page()
sleep_random()

# enter into corpus page
driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul/li[4]/a').click()
sleep_random()
driver.find_element_by_xpath('/html/body/div[2]/div[3]/ul[4]/li[3]/ul/li[1]/a').click()
sleep_random()

# enter into post
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'tbl_list')))
board = driver.find_element_by_xpath('/html/body/div[2]/form/div/div[3]/div/table')
post = board.find_elements_by_xpath('//*[@id="corpusList"]/div/table/tbody/tr[1]/td[2]/a')
post[0].click()
sleep_random()

# download corpus # 0. 전체 1. 원시 말뭉치 2. 형태분석 말뭉치 3. 형태의미 말뭉치 4. 구문분석 말뭉치')
corpus_name = ['all', 'orgFileSeq', 'posFileSeq', 'semFileSeq', 'info_result05']
corpus_checkbox_not_exist_msg = ['메시지 ',
                                '원시 ',
                                '형태분석 ',
                                '형태의미 ',
                                '구문분석 ']

for _ in tqdm(range(1495)):
    download_option_copy = DOWNLOAD_OPTION.copy()
    first_printed = True
    once_printed = False
    no_downloadable = False
    try:
        for current in [1, 2, 3, 4]:
            if current in DOWNLOAD_OPTION:
                try:
                    # click checkbox
                    org_checkbox = driver.find_element_by_name(corpus_name[current])
                    org_checkbox.click()
                except NoSuchElementException:
                    # print title and error msg
                    if first_printed:
                        post_title = driver.find_element_by_xpath('//*[@id="command"]/div/fieldset/table/tbody/tr[2]/td')
                        print(post_title.text, end = '')
                        print(': ', end = '')
                        first_printed = False
                        once_printed = True
                    print(corpus_checkbox_not_exist_msg[current], end = '')
                    # get next page
                    download_option_copy.discard(current)
                    if len(download_option_copy) < 1:
                        sleep_random()
                        press_next_button()
                        no_downloadable = True
                        break
            else:
                continue
        if once_printed:
            print('말뭉치가 존재하지 않습니다.')

        # 다운 할 게 없어서 내려왔으면
        if no_downloadable:
            continue

        # 내려받기 버튼 클릭
        inner_download_btn = driver.find_element_by_xpath('//*[@id="command"]/div/fieldset/table/tbody/tr[14]/td/ul/li[2]/a')
        inner_download_btn.click()

        # 동의란 버튼 클릭
        accept_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'agreementYn')))
        accept_btn.click()
        outer_download_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="agreementDownloadLayer"]/div[5]/a[1]')))
        outer_download_btn.click()

        # 다음글 버튼 클릭
        sleep_random()
        press_next_button()
    except UnexpectedAlertPresentException:
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            if alert_text == '더 이상의 글이 없습니다.':
                print('마지막 게시글입니다.')
                alert.accept()
                break
            else:
                print('알 수 없는 오류가 발생했습니다:')
                print('Failed to control alert: in handling exception UnexpectedAlertPresentException')
        except NoAlertPresentException: break
        except TimeoutException: break
    except Exception as exception:
        print('알 수 없는 오류가 발생했습니다.')
        print(exception)
        break

# close
try:
    print()
    print('브라우저를 종료하고 있습니다.')
    driver.close()
    print('브라우저를 성공적으로 종료하였습니다.')
    input('Enter 키를 눌러서 프로그램을 종료하세요.')
except Exception as e:
    try:
        print('알 수 없는 오류가 발생했습니다:')
        print(e)
        print('재시도: 브라우저를 종료하고 있습니다.')
        driver.quit()
        print('재시도: 브라우저를 성공적으로 종료하였습니다.')
        input('Enter 키를 눌러서 프로그램을 종료하세요.')
    except Exception as e:
        print('알 수 없는 오류가 발생했습니다:')
        print(e)
        print('브라우저를 직접 종료해주세요.')
        input('Enter 키를 눌러서 프로그램을 종료하세요.')