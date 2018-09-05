from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
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

        # main input
        username  = self.username
        browser.find_element_by_name('username').send_keys(username)

        password = self.password
        browser.find_element_by_name('password').send_keys(password)

        # Click login button
        browser.find_element_by_xpath('//button[text()="Log in"]').click()

        # Allow page time to load
        sleep(3)

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
        except NoSuchELementException:
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




username = 'username'
password = 'password'
myIGBot = InstaBot(username, password)
myIGBot.login()
myIGBot.like_hashtags('skateboarding')
