import getpass
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import random, time
MAX_SLEEP_SEC = 3

def sleep_random():
    rand = random.random() * MAX_SLEEP_SEC
    time.sleep(rand)

# get id and pw
def get_login_info():
    print('국립국어원 아이디와 비밀번호를 입력해주세요.')
    NIKL_ITHUB_ID = input('ID: ')
    NIKL_ITHUB_PW = getpass.getpass('PW: ')
    print()

    return (NIKL_ITHUB_ID, NIKL_ITHUB_PW)

def site_login(driver, NIKL_ITHUB_MAIN, NIKL_ITHUB_ID, NIKL_ITHUB_PW):
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
        get_login_info()
        site_login()
    except:
        pass



def handle_UnexpectedAlertPresentException(driver):
    WebDriverWait(driver, 3).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text
    
    if alert_text == '더 이상의 글이 없습니다.':
        print('마지막 게시글입니다.')
        alert.accept()
        return 0
    else:
        print('알 수 없는 오류가 발생했습니다:')
        print('Failed to control alert: in handling exception UnexpectedAlertPresentException')
        return 1

def close_driver(driver):
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