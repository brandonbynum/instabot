from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass


class InstaBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome()

    def login(self):
        # starting a new browser session
        browser = self.browser
        browser.get('https://instagram.com')

        # Go to login page
        login_elem = browser.find_element_by_xpath('//a[text() = "Log in"]')
        login_elem.click()

        sleep(2)

        # Enter instagram username from console
        # username = input('Username: ')
        # browser.find_element_by_name('username').send_keys(username)

        # Enter instagram password from console
        # password = getpass.getpass('Password: ')
        # browser.find_element_by_name('password').send_keys(password)

        # Enter Username and Password
        username  = self.username
        browser.find_element_by_name('username').send_keys(username)

        password = self.password
        browser.find_element_by_name('password').send_keys(password)

        # Click login button
        browser.find_element_by_xpath('//button[text()="Log in"]').click()

    def verificationCheck(self):
        browser = self.browser
        # Check if verification code is needed.
        # If so, enter the code in terminal.
        try:
            browser.find_element_by_xpath('//*[@id="react-root"]/section/div/div/div[3]/form/span/button[text()="Send Security Code"]').click()
            print('A security code is required to login. Please check your email for the code and enter it.')
            code = input('Code: ')
            # Input Key and Submit
            browser.find_element_by_xpath('//*[@id="security_code"]').send_keys(code)
            browser.find_element_by_xpath('//*[@id="react-root"]/section/div/div/div[2]/form/span/button').click()
        except NoSuchElementException:
            pass


    def closeAppOverlays(self):
        browser = self.browser
        # Close Notification Overlay
        try:
            browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        except NoSuchElementException:
            pass

        # Close 'get app' overlay if present
        try:
            browser.find_element_by_class_name('ckWGn').click()
        except NoSuchElementException:
            pass

        # Allow page time to load
        sleep(2)

        # Close bottom app ad
        try:
            browser.find_element_by_class_name('uDNXD').click()
        except NoSuchElementException:
            pass

        sleep(2)

    def like_hashtags(self, hashtag):
        browser = self.browser
        browser.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        sleep(2)
        for i in range(1,3):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        links = browser.find_elements_by_tag_name('a')
        post_links = [elem.get_attribute('href') for elem in links]
        post_links = [href for href in post_links if hashtag in href]
        print('#' + hashtag + ' photos: ' + str(len(post_links)))
        for i, link in enumerate(post_links):
            print('\tLink #' + str(i + 1) +': ' + link)




username = ''
password = ''
myIGBot = InstaBot(username, password)
myIGBot.login()
sleep(2)
myIGBot.verificationCheck()
sleep(2)
myIGBot.closeAppOverlays()
sleep(5)
myIGBot.like_hashtags('skateboarding')
