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

        try:
            # Go to login page
            login_elem = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')))
            # login_elem = browser.find_element_by_xpath('//a[text() = "Log in"]')
            login_elem.click()

            sleep(2)
        except Exception as e:
            print(error)
            exit

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

    def exists_by_xpath(self, xpath):
        try:
            self.browser.find_element_by_xpath(xpath).click()
        except NoSuchElementException:
            pass
        return True

    def closeAppOverlays(self):
        overlays = (
            '/html/body/div[4]/div/div/div/div[3]/button[2]', # 'Turn on Notifications' Overlay
            '/html/body/div[2]/div/div/div/div[1]/button',    # 'Get App' Overlay
            '//*[@id="react-root"]/section/div/span'          # 'Get App' Overlay at bottom of screen
        )
        for i in range(3):
            self.exists_by_xpath(overlays[i])



    def like_hashtags(self, hashtag):
        browser = self.browser
        browser.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        sleep(2)
        for i in range(1,3):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        links = browser.find_elements_by_tag_name('a')

        post_links = [elem.get_attribute('href') for elem in links]
        print('post_links1:\n\t')
        for i, link in enumerate(post_links):
            print('\tLink #' + str(i + 1) +': ' + str(link))
        print('-----------------------------')

        post_links = [href for href in post_links if hashtag in href]
        print('#' + hashtag + ' photos: ' + str(len(post_links)))
        for i, link in enumerate(post_links):
            print('\tLink #' + str(i + 1) +': ' + link)




username = ''
password = ''
myIGBot = InstaBot(username, password)
print('Logging in...')
myIGBot.login()
sleep(2)
print('Checking for verification...')
myIGBot.verificationCheck()
sleep(1)
print('Checking for overlays...')
myIGBot.closeAppOverlays()
print("Overlays closed.")
sleep(1)
#myIGBot.like_hashtags('skateboarding')
