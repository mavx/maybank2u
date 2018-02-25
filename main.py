import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


SESSION_URL = 'https://www.maybank2u.com.my/mbb/m2u/common/mbbPortalAccess.do?action=Login#1'
BROWSER = webdriver.Chrome('driver/chromedriver')
PASSWORD = os.getenv('MAYBANK2U_PASSWORD')
USERNAME = os.getenv('MAYBANK2U_USERNAME')


def main():
    task_list = [
        access_maybank2u,
        login,
        access_main_nav,
        access_account_details,
        access_account_nav,
    ]
    
    for task in task_list:
        task()
        time.sleep(2) # "Human"-delay


def access_maybank2u():
    BROWSER.get(SESSION_URL)


def login():
    print("Logging in...")
    # Username page
    username = BROWSER.find_element_by_id('input-rounded')
    username_next = BROWSER.find_element_by_id('replacement-4') # Input Field
    username.send_keys(USERNAME)
    username_next.click()

    # Image & security phase
    for elem in BROWSER.find_elements_by_id('replacement-4'):
        if elem.get_attribute('value').lower() == 'yes':
            elem.click()

    # Password
    password = BROWSER.find_element_by_id('input-rounded')
    login = BROWSER.find_element_by_id('replacement-1')
    password.send_keys(PASSWORD)
    login.click()


def access_main_nav(main_nav_name='accounts'):
    print("Accessing Account & Banking...")
    # Access account & banking
    for elem in BROWSER.find_elements_by_id('mainNav'):
        for li in elem.find_elements_by_css_selector('li'):
            for a in elem.find_elements_by_tag_name('a'):
                if 'account' in a.text.lower():
                    a.click()
                    return


def access_account_details():
    print("Accessing account details...")
    # Show account
    for elem in BROWSER.find_elements_by_class_name('account'):
        for a in elem.find_elements_by_tag_name('a'):
            if 'savings' in a.text.lower():
                url = a.get_attribute('href')
                a.click()
                return


def access_account_nav(nav_name='transaction_history'):
    print("Accessing transaction history...")
    elem = BROWSER.find_element_by_class_name('tableLink')
    for a in elem.find_elements_by_tag_name('a'):
        words = ['transaction', 'history']
        if all(w in a.text.lower() for w in words):
            a.click()
            return


# print('Quitting browser')
# BROWSER.quit()


if __name__ == '__main__':
    main()
