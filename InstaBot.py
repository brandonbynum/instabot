from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import sys


class InstaBot():
    def __init__(self):
        self.browser = webdriver.Chrome()

    # Checks if an element exists by searching for it's expected xpath
    def exists_by_xpath(self, xpath):
        try:
            self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            #print(xpath, "does not exist")
            return False
        return True

    def quitDriver(self, reason):
        print(reason + '\nClosing InstaBot. GoodBye.')
        self.browser.quit()
        sys.exit()


    def login(self):
        # Starting a new browser session / driver.
        print('Connecting to Instagram ...')
        browser = self.browser
        browser.get('https://instagram.com')

        try:
            # Wait for page to load then locate login page link
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

        sleep(2)

        # Enter Username
        usernameElement = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="username"]'))
        )
        usernameElement.clear()
        username = input('Time to log in. \nPlease enter your username: ')
        usernameElement.send_keys(username)


        # Enter Password
        passwordElement = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
        )
        passwordElement.clear()
        password = getpass.getpass('Password:')
        passwordElement.send_keys(password)

        # Click login button
        browser.find_element_by_xpath('//button/div[text()="Log In"]').click()

        sleep(1)

        # Check for 2-factor authentication
        self.verificationCheck()

        # Check if the login has been successful, exit program otherwise.

        if self.exists_by_xpath('//*[@id="slfErrorAlert"]'):
            self.quitDriver('Password was incorrect. Please check password before running bot again.')
        else:
            try:
                WebDriverWait(browser, 60).until(
                    EC.presence_of_element_located((By.XPATH, '//span[@aria-label="Profile"]'))
                )
            except Exception as e:
                print(e)
                self.quitDriver('An error occurred!')

            print('Login Successul!')
            print('Welcome', username + "!")

    def verificationCheck(self):
        browser = self.browser
        attempts = 5
        print('Checking for verification...')

        # Check if verification code is needed.
        # If so, enter the code in terminal.
        try:
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/div/div/div[3]/form/span/button[text()="Send Security Code"]'))
            )
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
                sleep(1)

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
        except:
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



    def get_hashtag_links(self, hashtagList):
        browser = self.browser
        postLinks = []
        for hashtag in hashtagList:
            print("Searching hashtag '" + hashtag + "'")
            browser.get("https://www.instagram.com/explore/tags/" + hashtag + "/")

            for i in range(1,3):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Get all the elements containing href tags
            print("Collecting", hashtag, "image links ...")
            elements = browser.find_elements_by_xpath("//a[contains(@href, '/p/')]")
            for elem in elements:
                # Append each href link to the list of image links
                postLinks.append(elem.get_attribute('href'))
            print('Finished collecting', str(len(elements)), "photos from '" + hashtag + "'." )

        print(str(len(postLinks)), 'photos collected total.')
        return postLinks

    def like_photos(self, links):
        likeXpath = '//button/span[@aria-label="Like"]'
        likedXpath = '//button/span[@aria-label="Unlike"]'

        photosLiked = 0
        photosLikedAlready = 0
        photosDidntLoad = 0
        totalPhotos = len(links)

        for i, photoLink in enumerate(links):
            self.browser.get(photoLink)
            sleep(1)
            photoNum = i + 1
            print('\nPhoto #' + str(photoNum), 'loaded:', photoLink)

            # Check if photo has already been liked, if not, like it
            if self.exists_by_xpath(likedXpath):
                print('Photo Already Liked!')
                photosLikedAlready += 1
            elif self.exists_by_xpath(likeXpath):
                self.browser.find_element_by_xpath(likeXpath).click()
                print('Photo Liked!')
                photosLiked +=1
            else:
                print('Error loading photo')
                photosDidntLoad += 1

        print('\n\nFinished liking photos.')
        print('Photos Liked:', photosLiked)
        print('Photos already liked:', photosLikedAlready)
        print('Photos unable to load:', photosDidntLoad)
        print('\n\n')



print("Welcome to Instabot!")

print("Currently the only supported feature is liking images based on hash tag searches.")
hashtags = input('Please enter hashtags you would like to search separated by commas. \nEx. "skateboarding, basketball, shoes".\n:')
hashtags = [hashtag.strip() for hashtag in hashtags.split(',')]

myIGBot = InstaBot()
myIGBot.login()
sleep(1)
links = myIGBot.get_hashtag_links(hashtags)
myIGBot.like_photos(links)

myIGBot.quitDriver('Task complete.')
