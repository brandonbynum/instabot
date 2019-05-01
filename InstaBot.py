from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import sys


class InstaBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome()

    # Checks if an element exists by searching for it's expected xpath
    def exists_by_xpath(self, xpath):
        try:
            self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            print(xpath, "does not exist\n")
            return False
        return True

    def quitDriver(self, reason):
        print(reason + '\nClosing InstaBot. GoodBye.')
        self.browser.quit()
        sys.exit()


    def login(self):
        if self.username == '':
            print('Error: No username entered')
            self.quitDriver()

        if self.password == '':
            print('Error: No password entered')
            self.quitDriver()

        # Starting a new browser session / driver.
        browser = self.browser
        browser.get('https://instagram.com')

        try:
            # Wait for page to load until login page link to become clickable
            login_elem = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.XPATH,
                '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')))

            # Navigate to login page by clicking the link
            try:
                login_elem.click()
                print('Navigating to login page')
            except Exception as e:
                self.quitDriver('Error:', e , '\nLogin Link could not be clicked and/or found!')
        except Exception as e:
            self.quitDriver('Error:', e , '\nPage could not load or login link could not be found.')

        sleep(1)
        # Enter Username
        userInputXPath = '//input[@name="username"]'
        usernameElement = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@name="username"]'))
        )
        #usernameElement = browser.find_element_by_xpath('//input[@name="username"]')
        usernameElement.clear()
        usernameElement.send_keys(self.username)

        sleep(1)

        # Enter Password
        passwordElement = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]'))
        )
        #passwordElement = browser.find_element_by_name('password')
        passwordElement.clear()
        passwordElement.send_keys(self.password)

        # Click login button
        browser.find_element_by_xpath('//button/div[text()="Log In"]').click()

        # Check for 2-factor authentication
        self.verificationCheck()

        # Check if the login has been successful, exit program otherwise.
        if self.exists_by_xpath('//*[@id="slfErrorAlert"]'):
            self.quitDriver('Password was incorrect. Please check password before running bot again.')
        else:
            print('Login Successul!')
            print('Welcome', self.username + "!")

    def verificationCheck(self):
        browser = self.browser
        attempts = 5
        print('Checking for verification...')

        # Check if verification code is needed.
        # If so, enter the code in terminal.
        if self.exists_by_xpath('//*[@id="react-root"]/section/div/div/div[3]/form/span/button[text()="Send Security Code"]'):
            # Click button to send code
            browser.find_element_by_xpath('//*[@id="react-root"]/section/div/div/div[3]/form/span/button[text()="Send Security Code"]').click()
            print('A security code is required to login. Please check your email for the code and enter the code below. (' + str(attempts) + ' attempts remaining)')

            # Loop giving 5 attempts to correctly enter code.
            for i in range(attempts):
                code = input('Code: ')

                # Input Key and Submit
                codeElement = browser.find_element_by_xpath('//*[@id="security_code"]')
                codeElement.send_keys(code)

                # Submit verification code
                browser.find_element_by_xpath('//*[@id="react-root"]/section/div/div/div[2]/form/span/button').click()
                browser.implicitly_wait(1)

                # If code is wrong, reduce allowed attempts otherwise continue.
                if self.exists_by_xpath('//*[@id="form_error"]/p'):
                    attempts -= 1
                    if attempts == 0:
                        self.quitDriver('Too many failed verification code attempts.')
                    else:
                        print('Wrong code, try again. (' + str(attempts) + ' attempts remaining)')
                        codeElement.clear()
                else:
                    break

        print('No extra verification needed.')



    def closeAppOverlays(self):
        overlays = (
            '/html/body/div[4]/div/div/div/div[3]/button[2]', # 'Turn on Notifications' Overlay
            '/html/body/div[2]/div/div/div/div[1]/button',    # 'Get App' Overlay
            '//*[@id="react-root"]/section/div/span'          # 'Get App' Overlay at bottom of screen
        )
        print('Checking for overlays...')
        for i in range(3):
            overlay = overlays[i]
            if self.exists_by_xpath(overlay):
                self.browser.find_element_by_xpath(overlay).click()
                print("Overlays closed.")
            else:
                print("No Overlays found.")



    def get_hashtag_links(self, hashtag):
        def printLinks(links):
            for i, link in enumerate(post_links):
                print('\tLink #' + str(i + 1) +': ' + str(link))

        browser = self.browser
        print("Searching hashtag '" + hashtag + "'")
        browser.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        sleep(2)
        # for i in range(1,3):
        #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        elements = browser.find_elements_by_xpath("//a[contains(@href, '/p/')]")
        post_links = [elem.get_attribute('href') for elem in elements]
        print('post_links1:\n\t')
        printLinks(post_links)
        return post_links

    def like_photos(self, links):
        likeXpath = '//button/span[@aria-label="Like"]'
        likedXpath = '//button/span[@aria-label="Unlike"]'

        for photoLink in links:
            self.browser.get(photoLink)
            sleep(2)
            print(photoLink, 'loaded \n')

            # Check if photo has already been liked, if not, like it
            if self.exists_by_xpath(likedXpath):
                print('Photo Already Liked!')
            elif self.exists_by_xpath(likeXpath):
                # Like photo
                self.browser.find_element_by_xpath(likeXpath).click()
                print('Photo Liked!')


username = ''
password = ''
print('Creating InstaBot instance')
myIGBot = InstaBot(username, password)

myIGBot.login()
sleep(1)
#links = myIGBot.get_hashtag_links('analog')
myIGBot.like_photos(['https://www.instagram.com/p/Bw2F1wtgebC/'])
