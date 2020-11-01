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

from pkg.greetings import *
from pkg.getOptions import *
from pkg.inDriver import *

### global vars
MAX_SLEEP_SEC = 3
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER = ABS_PATH + r'\chromedriver.exe'
NIKL_ITHUB_MAIN = 'https://ithub.korean.go.kr/user/main.do'
NIKL_ITHUB_CORPUS = 'https://ithub.korean.go.kr/user/total/database/corpusManager.do'
NIKL_ITHUB_ID = ''
NIKL_ITHUB_PW = ''
DOWNLOAD_OPTION = set()

# 0. 전체 1. 원시 말뭉치 2. 형태분석 말뭉치 3. 형태의미 말뭉치 4. 구문분석 말뭉치')
corpus_name = ['all', 'orgFileSeq', 'posFileSeq', 'semFileSeq', 'info_result05']
corpus_checkbox_not_exist_msg = ['메시지 ',
                                '원시 ',
                                '형태분석 ',
                                '형태의미 ',
                                '구문분석 ']

### JS Selector
js_nextBtn = '/html/body/div[2]/form/div/div[8]/div/div[1]/a[3]'
js_board = '/html/body/div[2]/form/div/div[3]/div/table'
js_post = '//*[@id="corpusList"]/div/table/tbody/tr[1]/td[2]/a'
js_postTitle = '//*[@id="command"]/div/fieldset/table/tbody/tr[2]/td'
js_downloadBtn = '//*[@id="command"]/div/fieldset/table/tbody/tr[14]/td/ul/li[2]/a'
js_outerDownloadBtn = '//*[@id="agreementDownloadLayer"]/div[5]/a[1]'
js_indexToSitemap = '/html/body/div[1]/div[1]/ul/li[4]/a'
js_sitemapToCorpus = '/html/body/div[2]/div[3]/ul[4]/li[3]/ul/li[1]/a'

### HTML Class Name
class_postsTable = 'tbl_list'

# functions
def sleep_random():
    rand = random.random() * MAX_SLEEP_SEC
    time.sleep(rand)

def press_next_button():
    next_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, js_nextBtn)))
    next_btn.click()
        
### logic
greetings()

NIKL_ITHUB_ID, NIKL_ITHUB_PW = get_login_info()
DOWNLOAD_OPTION = get_download_option()
driver = webdriver.Chrome(CHROME_DRIVER) # open driver

# login
site_login(driver, NIKL_ITHUB_MAIN, NIKL_ITHUB_ID, NIKL_ITHUB_PW)
sleep_random()

# enter into corpus page
driver.find_element_by_xpath(js_indexToSitemap).click()
sleep_random()
driver.find_element_by_xpath(js_sitemapToCorpus).click()
sleep_random()

# enter into post
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, class_postsTable)))
board = driver.find_element_by_xpath(js_board)
post = board.find_elements_by_xpath(js_post)
post[0].click()
sleep_random()

# download corpus
for _ in tqdm(range(1495)): # single post에 성공적으로 진입
    download_option_copy = DOWNLOAD_OPTION.copy()
    first_print = True
    once_printed = False
    no_downloadable = False
    try:
        for current in [1, 2, 3, 4]:
            if current not in DOWNLOAD_OPTION:
                continue

            try: # single corpus 다운로드 과정
                # click checkbox
                org_checkbox = driver.find_element_by_name(
                    corpus_name[current])
                org_checkbox.click()
            except NoSuchElementException:
                # print title and error msg
                if first_print:
                    post_title = driver.find_element_by_xpath(
                        js_postTitle)
                    print(post_title.text, end = '')
                    print(': ', end = '')
                    first_print = False
                    once_printed = True
                print(corpus_checkbox_not_exist_msg[current], end = '')
                # get next page
                download_option_copy.discard(current)
                if len(download_option_copy) < 1:
                    sleep_random()
                    press_next_button()
                    no_downloadable = True
                    break
        
        if once_printed:
            print('말뭉치가 존재하지 않습니다.')

        # 다운 할 게 없어서 내려왔으면
        if no_downloadable:
            continue

        # 내려받기 버튼 클릭
        inner_download_btn = driver.find_element_by_xpath(js_downloadBtn)
        inner_download_btn.click()

        # 동의란 버튼 클릭
        accept_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'agreementYn')))
        accept_btn.click()

        # 최종 다운로드 버튼 클릭
        outer_download_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, js_outerDownloadBtn)))
        outer_download_btn.click()

        # 다음글 버튼 클릭
        sleep_random()
        press_next_button()

    except UnexpectedAlertPresentException:
        try:
            except_res = handle_UnexpectedAlertPresentException(driver)
            if except_res == 0: break
            else: pass
        except NoAlertPresentException: break
        except TimeoutException: break
    except Exception as exception:
        print('알 수 없는 오류가 발생했습니다.')
        print(exception)
        break

# close
close_driver(driver)