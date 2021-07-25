import time
import sys
import toml
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    try:
        with open("user.txt", 'r') as f:
            conf = toml.load(f)
    except Exception as e:
        print(e)
        sys.exit(0)
    USER = conf['USER']
    USER_ID = USER['ID']
    XS = USER['XS']
    CONTENT = conf['CONTENT']
    MESSAGE = CONTENT['MESSAGE']
    CONVERSATION = CONTENT['CONVERSATION']
    AT = conf['AT']
    print(f"send message: {MESSAGE} to {CONVERSATION}")
    print(f"schedule at: {AT['HOUR']:02d}:{AT['MINUTE']:02d}:{AT['SECOND']:02d}")

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.messenger.com")
    driver.add_cookie({'name': 'c_user', 'value': USER_ID, 'domain': '.messenger.com'})
    driver.add_cookie({'name': 'xs', 'value': XS, 'domain': '.messenger.com'})
    driver.get(f"https://www.messenger.com/t/{CONVERSATION}")
    driver.implicitly_wait(5)
    while True:
        now = datetime.now().replace(microsecond=0)
        nex = datetime(now.year, now.month, now.day, AT['HOUR'], AT['MINUTE'], AT['SECOND'])
        if now == nex:
            elem = driver.find_element_by_xpath('//div[@data-contents="true"]')
            elem.send_keys(f"{MESSAGE}")
            elem.send_keys(Keys.RETURN)
        time.sleep(1)
