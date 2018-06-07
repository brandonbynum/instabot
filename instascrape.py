import requests
import time
from bs4 import BeautifulSoup


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
def get_user_data(user):
    # Pull HTML of user's instagram page
    html = requests.get(url + user).content
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
    ratio = int(followers.replace(',', '')) / int(following.replace(',', ''))

    return {'followers': followers, 'following': following, 'posts': posts, 'ratio': ratio}


# Start of program    
url = 'https://instagram.com/'

# Input desired instagram user name
user = input('\nEnter Instagram name @')

data = get_user_data(user)

print('\n@' + user, 'currently has', data['posts'], 'posts with', data['followers'], 'followers, '
'while following', data['following'], 'other users.')
print('Follower to Following Ratio:', str(round(data['ratio'], 2)) + '%\n\n')

