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
            return False
        return True

    def closeProgram(self, reason):
        print(reason + '\nClosing InstaBot. GoodBye.')
        self.browser.quit()
        sys.exit()


    def login(self):
        # Starting a new browser session / driver.
        browser = self.browser
        browser.get('https://instagram.com')

        try:
            # Go to login page.
            login_elem = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.XPATH,
                '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')))

            # login_elem = browser.find_element_by_xpath('//a[text() = "Log in"]')
            login_elem.click()
            print('Logging in...')
            sleep(2)

        except Exception as e:
            self.closeProgram('Wrong password entered.')

        # Enter instagram username from console.
        # username = input('Username: ')
        # browser.find_element_by_name('username').send_keys(username)

        # Enter instagram password from console
        # password = getpass.getpass('Password: ')
        # browser.find_element_by_name('password').send_keys(password)

        # Enter Username
        usernameElement = browser.find_element_by_xpath('//input[@name="username"]')
        usernameElement.clear()
        usernameElement.send_keys(self.username)

        # Enter Password
        passwordElement = browser.find_element_by_name('password')
        passwordElement.clear()
        passwordElement.send_keys(self.password)
        sleep(2)

        # Click login button
        browser.find_element_by_xpath('//button/div[text()="Log In"]').click()
        sleep(3)

        if self.exists_by_xpath('//*[@id="react-root"]/section/div/div/div[3]/form/span/button[text()="Send Security Code"]'):
            print('Checking for verification...')
            self.verificationCheck()
            sleep(2)
        # Check if the login has been successful, exit program otherwise.
        elif self.exists_by_xpath('//*[@id="slfErrorAlert"]'):
            self.closeProgram('Password was incorrect. Please check password before running again.')
        else:
            print('Welcome', self.username + "!")

    def verificationCheck(self):
        browser = self.browser
        attempts = 5
        # Check if verification code is needed.
        # If so, enter the code in terminal.
        try:
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
                sleep(1)

                # If code is wrong, reduce allowed attempts otherwise continue.
                if self.exists_by_xpath('//*[@id="form_error"]/p'):
                    attempts -= 1
                    if attempts == 0:
                        self.closeProgram('Too many failed verification code attempts.')
                    else:
                        print('Wrong code, try again. (' + str(attempts) + ' attempts remaining)')
                        codeElement.clear()
                else:
                    break
        except NoSuchElementException:
            pass



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
        for photoLink in links:
            self.browser.get(photoLink)
            sleep(1)
            print(photoLink, 'loaded \n')

            # Like photo
            self.browser.find_element_by_xpath('//button/span[@aria-label="Like"]').click()




username = 'munybrr'
password = 'Whoisthis2124!'
myIGBot = InstaBot(username, password)

myIGBot.login()
myIGBot.verificationCheck()
sleep(1)
#myIGBot.closeAppOverlays()
# sleep(1)
links = myIGBot.get_hashtag_links('analog')
myIGBot.like_photos(links)
