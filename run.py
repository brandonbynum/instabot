import InstaBot
import config

import getpass
from time import sleep
import random


print("Welcome to Instabot!")
print("Currently the only supported feature is liking images based on hash tag searches.\n")

def getHashTags():
    hashtagOptions = config.HASHTAGS
    numToSelect = config.NUMBER_OF_HASHTAGS
    randomlySelect = config.RANDOM_HASHTAGS

    if not len(hashtagOptions) > 0:
        print("Please enter a hashtag or list of hashtags you would like to search separated by commas, then press 'Enter'. \nEx. 'skateboarding, basketball, shoes'.\n")
        hashtags = input()
    else:
        if numToSelect > len(hashtagOptions):
            print(f"There are not enough hashtag choices to search {numToSelect} hashtags, so we will search the existing {len(hashtagOptions)} hashtag options.")
            hashtags = hashtagOptions

        if not randomlySelect:
            hashtags = hashtagOptions[:numToSelect]
        else:
            hashtags = random.sample(hashtagOptions, numToSelect)

    print('Hashtags that will be searched:', hashtags, '\n')
    return hashtags

def getCredentials():
    def getPassword():
        if not config.PASSWORD == '':
            return config.PASSWORD
        else:
            print(f"Please enter the password for user '{username}'")
            return getpass.getpass('Password:')

    if not config.USERNAME == '':
        username = config.USERNAME
        password = getPassword()
        
    else:
        username = input('\nTime to log in. \nPlease enter your username: ')
        password = getPassword()

    return {'username':username, 'password':password}




hashtags = getHashTags()

credentials = getCredentials()
username = credentials['username']
password = credentials['password']
myIGBot = InstaBot.InstaBot()
myIGBot.login(username, password)
print('login complete')
links = myIGBot.get_hashtag_links(hashtags)
myIGBot.like_photos(links)

myIGBot.quitDriver('Task complete.')
