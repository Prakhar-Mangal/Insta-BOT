
# Instagram Bot 🤖

![](/Demo/insta_bot-1.gif)

Insta Bot is **automation** which handles your Instagram account as a real user. While running automated tasks you're sitting and enjoying your sip of coffee ☕

## Features 
1. Get Unfollowers List ( the one's who didn't follow you back ) 😠
2. You can send a personalized message to anyone ✉️
3. Like and Comment Posts through Hashtag ❤️
4. You can comment on someone's recent post 😁
5. You can send multiple posts to someone through Hashtag 🏦

## Requirements

 - [python 3+](https://www.python.org/downloads/)
 - [selenium](https://pypi.org/project/selenium/)
 - [ChromeDriver](https://chromedriver.chromium.org/downloads)
 
 ## Installation
 ### Steps
 1. Clone this repository
 2. Create and **Activate Virtual Environment**
 3. Write command `pip3 install -r requirements.txt`
 4. Open **secret.py**, replace 
 `username = **** 
 pw = **** ` with your crendentials.
 5. Open **insta_bot.py** and replace 
`DRIVER_PATH = '/home/prakhar/Downloads/chromedriver_linux64/chromedriver'`
with your ChromeDriver path
6. Now you're ready to go `python3 insta_bot.py` and enjoy your coffee ☕.

## Wanna add more features 
Follow the instruction to add more features,
1. Open the file **insta_bot.py**
2. Under **class InstaBot define your method** with new features.
3. Now integrate that feature in while loop and **test it twice**.
4. At last, **make a pull request**, and thanks for collaborating.


Please do ⭐ the repository, if it helped you in any way.
