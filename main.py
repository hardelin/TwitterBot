from os import system
system("pip install -r requirement.txt")
import time
from libs.selenium import webdriver
from libs.selenium.webdriver.chrome.service import Service
from libs.selenium.webdriver.common.by import By
from libs.selenium.webdriver.support import expected_conditions as EC
from libs.selenium.webdriver.support.ui import WebDriverWait
from libs.webdriver_manager.chrome import ChromeDriverManager

targets = list(map(str.strip, open('source/targets.txt', encoding='utf-8').readlines()))  # twitterID целевых точек
file = open('source/userdata.txt', encoding='utf-8')
userdata = list(map(lambda x: x.strip('\n').split(), file.readlines()))  # логин + пароль подготовленных аккаунтов
file.close()
data = []
for dat in userdata:
    d = {'username': dat[0], 'password': dat[1]}
    data.append(d)
check = open('source/last_acc.txt',
             encoding='utf-8').read()  # файл с последним пройденным аккаунтом для сохранения прогресса
ind = 0
if len(check) > 0:
    while data[ind]['username'] != check:
        ind += 1
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
for user in data[ind:]:
    driver.get("https://x.com/login")
    try:
        login_field = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
        time.sleep(2)
        login_field.send_keys(user['username'])
    except:
        lst = open('source/last_acc.txt', "w").write(user['username'])
        driver.quit()
        exit('not available internet connection or username')
    driver.find_element(By.XPATH,
                        "//button[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 r-184id4b r-13qz1uu r-2yi16 r-1qi8awa r-3pj75a r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']").click()
    try:
        password_field = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        time.sleep(2)
        password_field.send_keys(user['password'])
    except:
        lst = open('source/last_acc.txt', "w").write(user['username'])
        exit('not available internet connection or password')
    driver.find_element(By.XPATH,
                        "//button[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-19yznuf r-64el8z r-1fkl15p r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']").click()
    for account in targets:
        search_field = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
        time.sleep(2)
        search_field.send_keys(f'{account}')
        try:
            ret = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                                  f"//button[./div[./div[./div[./div[./div[./div[./div[./div[./div[./span[text()='{account}']]]]]]]]]]]")))
            time.sleep(2)
            ret.click()
        except:
            pass
        try:
            follow_button = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, f"//button[@aria-label='Follow {account}']")))
            time.sleep(2)
            follow_button.click()
        except:
            pass
        try:
            notification = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Turn on post notifications']")))
            time.sleep(2)
            notification.click()
        except:
            pass
    driver.quit()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
