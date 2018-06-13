#! python
# A script that currently fetches instagram user information by input and webscraping.

import requests
import time
from bs4 import BeautifulSoup
import keyboard


# Removes 'k'(thousands) or 'm'(millions) from number.
# Ex. '10.9k' -> '10,900', '1.2m' -> '1,200,000'
def clean_number(number):
    if 'k' in number:
        thousands = number[:number.find('.')] 
        hundreds = str(int(number[number.find('.') + 1: -1]) * 100)
        number = thousands + ',' + hundreds

    if 'm' in number:
        millions = number[:number.find('.')]
        thousands = str(int(number[number.find('.') + 1: number.find('m')]) * 100)
        number = millions + ',' + thousands + ',' + '000'

    return number

# Pulls followers, following, posts, and makes following to follower ratio.
# returns dictionary storing all values
def get_user_data(username):
    # Pull HTML of user's instagram page
    html = requests.get(url + username).content
    soup = BeautifulSoup(html, "lxml")

    # Grab the meta tag with the followers, following, and post count
    # Ex. <meta content="1,393 Followers, 285 Following, 8 Posts - See Instagram 
    #     photos and videos from brandon (@munybrr)" property="og:description"/>
    data = soup.find("meta", property="og:description")

    # Grab inside of content assignment
    # Ex. '1,393 Followers, 285 Following, 8 Posts - See Instagram photos and videos from brandon (@munybrr)'
    data = data['content']
    data = str(data)
    
    # Amount of followers as string
    followers = data[: data.find('Followers')].strip()

    # Fix value if value > 10,000
    if 'k' in followers or 'm' in followers:
        followers = clean_number(followers)

    following = data[data.find('s,') + 2: data.find('Following')].strip()
    posts = data[data.find('g,') + 2: data.find('Posts') - 1].strip()
    ratio = round(int(followers.replace(',', '')) / int(following.replace(',', '')), 2)

    return {'username': username,'followers': followers, 'following': following, 'posts': posts, 'ratio': ratio}

# Creates a list of usernames from user input and returns the list.
def enter_users():
    usernames = []
    print('Enter a username following the "@". Next press "Enter" to add a username or type "/done"' +
    'and press "Enter" to finish entering usernames.')
    while True:
        user = input('>> ')
        if user == '/done':
            break
        usernames.append(user)
    return usernames




# Start of program    
url = 'https://instagram.com/'

usernames = enter_users()
print('Fetching data ...')
data = {}
percent = 0
for i, user in enumerate(usernames):
    data[user] = get_user_data(user)
    percent +=  int(round(1 / len(usernames) * 100, 0))
    print(str(percent) + '%')

print('Done! Here is your data ...\n')

for user in usernames:
    username = data[user]['username']
    posts = data[user]['posts']
    followers = data[user]['followers']
    following = data[user]['following']
    ratio = str(data[user]['ratio'])

    print('@' + username, 'currently has', posts, 'posts with', followers, 'followers, '
    'while following', following, 'other users.')
    print('Follower to Follow Ratio:', ratio + '%\n')

