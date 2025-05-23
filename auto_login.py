# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00ED897CF64488F4A6D893D880B40186B5743722700DD9C1FEEBC510392610045F0CE8EB14E244B45762929A0225820DD602CFEA122AFBBEB420DB7F47E878F8FA3E8DFFCFD85F69DB94D2A1D4684DD1FB0516652EA37245B2006B6D39D2F20F253E6C937990AA820DAC126AF831117A6E02CC790BC47B2191632E916593148F06D96B120BC6CEDC5F1C958BAB3AE8F435E1BCE678C2CB6A40498AB8E5C6D70BF7F0DEFE21D677191971D7739C1B3845356E27F0B3E96F7FE51B5F4CD85AC02092E672602BCB0D1466DB526CE501F0D2B8F4A28DF24DE0EC91A0840D9EF6691622E414A6D3E7093B4CA58C15FD777313FFCCB9ED7B77FB8315748B560B1DE590E6D8989AB7F183D55171A67561A63568786B1185342E1127C6DB5F57E6BB9680C023897E16FB2279CFE8EB6F5042961F4318658F7A68EF7E1D41EFFE3D622D8D42055128D14BF8D0749D84DF117107E0F159328C4D49501DD0484D6A95C6B7525F"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
