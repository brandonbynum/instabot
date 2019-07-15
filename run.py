import InstaBot
import config

import getpass
from time import sleep


print("Welcome to Instabot!")

print("Currently the only supported feature is liking images based on hash tag searches.\n")
#print("Please enter a hashtag or list of hashtags you would like to search separated by commas, then press 'Enter'. \nEx. 'skateboarding, basketball, shoes'.\n")
#hashtags = input()

hashtags = config.HASHTAGS

username = input('\nTime to log in. \nPlease enter your username: ')
password = getpass.getpass('Password:')

#username = config.username
#password = config.password

myIGBot = InstaBot.InstaBot()
myIGBot.login(username, password)
sleep(1)
links = myIGBot.get_hashtag_links(hashtags)
myIGBot.like_photos(links)

myIGBot.quitDriver('Task complete.')
