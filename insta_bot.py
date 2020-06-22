from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from secret import username, pw
import datetime, os, re
from random import randint
DRIVER_PATH = '/home/prakhar/Downloads/chromedriver_linux64/chromedriver' # replace your path here

# return True if element is visible within 10 seconds, otherwise False 
def is_visible(locator,chrome,timeout = 10): 
	try: 
		WebDriverWait(chrome, timeout).until(EC.visibility_of_element_located((By.XPATH, locator))) 
		return True
	except TimeoutException: 
		return False



class InstaBot:
    comments = ['Good Job', 'Awesome Post']
    def __init__(self, username, pw):
        try:
            self.followers = set()
            self.following = set()
            self.unfollowers = set()
            self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
            self.driver.get('https://www.instagram.com/')  # open insta page
            self.username = username    

            if not is_visible('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(username) # enter username
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(pw) #enter password
            self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]').click()

            if not is_visible('//*[@id="react-root"]/section/main/div/div/div/div/button',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
            
            if not is_visible('/html/body/div[4]/div/div/div/div[3]/button[2]',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
            print('Logged In Successful')
        except:
            print('Something went wrong try again!!')
       

    def get_unfollowers(self):
        try:
            self.driver.get(f'https://www.instagram.com/{self.username}/')
            self.get_followers_or_following(2)  # generating all followers list
            self.get_followers_or_following(3)  # generating all following list
            self.unfollowers = (self.following).difference(self.followers)  # all unfollowers = |following| - |followers|
            print('done')
            for name in list(self.unfollowers):
                dirname = './'
                csvfilename = os.path.join(dirname, f"unfollowers_{self.username}.txt")
                f = open(csvfilename,'a')
                f.write(name + '\r\n')
                f.close()
        except:
            print('Something went wrong try again!!')
        
    def get_followers_or_following(self,i_path):
        try:
            if not is_visible(f'//*[@id="react-root"]/section/main/div/header/section/ul/li[{i_path}]/a',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            choice_path = self.driver.find_element_by_xpath(f'//*[@id="react-root"]/section/main/div/header/section/ul/li[{i_path}]/a') # ipath = 2 (followers) or =3 (unfollowers)
            self.driver.find_element_by_xpath(f'//*[@id="react-root"]/section/main/div/header/section/ul/li[{i_path}]/a').click()
        
        
            count = int(''.join(re.findall("\d+", choice_path.text)))
            print(f'{choice_path.text.split()[1]} : {count}')
            for i in range(1,count+1):
                try:
                    if not is_visible(f'/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
                    src = self.driver.find_element_by_xpath(f'/html/body/div[4]/div/div/div[2]/ul/div/li[{i}]')
                    
                    self.driver.execute_script("arguments[0].scrollIntoView();", src) # scrolling
                    lst = src.text.split()
                    dirname = './'
                    csvfilename = os.path.join(dirname, f"{choice_path.text.split()[1]}_{self.username}.txt") # creating file .txt
                    f = open(csvfilename,'a')
                    f.write(lst[0] + '\r\n')
                    f.close()
                    if i_path == 2:
                        self.followers.add(lst[0])  # adding on followers set
                    else:
                        self.following.add(lst[0])  # adding on following set
                    print(f'{i} : {lst[0]}')

                except:
                    pass
            print(f'{choice_path.text.split()[1]} Completed.................')
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
        except:
            print('Something went wrong try again!!')

    def like_comment_by_hashtag(self):
        try:
            hashtag = input("Enter Hashtag : ")

            self.driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        
            if not is_visible('//*[@id="react-root"]/section/main/article/div[1]/h2/div',self.driver): raise RuntimeError("Something Went Wrong, Try Again !")             
            href_found = self.driver.find_elements_by_tag_name('a')  # selecting all href
            photo_url = [ele.get_attribute('href') for ele in href_found if '.com/p' in ele.get_attribute('href')]
            
            for i in range(5):
                self.driver.get(photo_url[i])
                #like
                if not is_visible('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button',self.driver): raise RuntimeError("Something Went Wrong, Try Again !")            
                self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button').click()
                #comment
                if not is_visible('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[3]/div/form/textarea',self.driver): raise RuntimeError("Something Went Wrong, Try Again !")            
                self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[3]/div/form/textarea').click()
                if not is_visible("//textarea[@placeholder='Add a comment…']",self.driver): raise RuntimeError("Something Went Wrong, Try Again !")            
                self.driver.find_element_by_xpath("//textarea[@placeholder='Add a comment…']").send_keys(self.comments[randint(0,1)])
                if not is_visible("//button[@type='submit']",self.driver): raise RuntimeError("Something Went Wrong, Try Again !")            
                self.driver.find_element_by_xpath("//button[@type='submit']").click()
                print(f'Like and Comment done  .....')
              
        except:
            print('Something went wrong try again!!')
            

    def comment_on_account(self):
        try:
            account_name = input("Enter Account Name : ")
            comment = input("Enter Comment : ")
            # get to profile page
            self.driver.get(f'https://www.instagram.com/{account_name}/')
            # get most recent photo
            if not is_visible('//*[@id="react-root"]/section/main/div/div[2]',self.driver): raise RuntimeError("Something Went Wrong, Try Again !")            
            href_found = self.driver.find_elements_by_tag_name('a')  # selecting all href
            photo_url = [ele.get_attribute('href') for ele in href_found if '.com/p/' in ele.get_attribute('href')]

            self.driver.get(photo_url[0])
            # like
            if not is_visible('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button',self.driver): raise RuntimeError("Something Went Wrong, Try Again !")            
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button').click()
            # comment on the photo
            if not is_visible('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[3]/div/form/textarea',self.driver): raise RuntimeError("Something Went Wrong, Try Again !")            
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[3]/div/form/textarea').click()
            
            if not is_visible("//textarea[@placeholder='Add a comment…']",self.driver): raise RuntimeError("Something Went Wrong, Try Again !")            
            self.driver.find_element_by_xpath("//textarea[@placeholder='Add a comment…']").send_keys(comment)
            
            if not is_visible("//button[@type='submit']",self.driver): raise RuntimeError("Something Went Wrong, Try Again !")            
            self.driver.find_element_by_xpath("//button[@type='submit']").click()

            print(f'Comment done on account : {account_name}')
           
        except:
            print('Something went wrong try again!!')

    def send_post_by_hashtag(self):
        
        hashtag = input("Enter Hashtag : ")
        user = input("Enter User : ") 
        no_of_post = int(input("Enter no. of post to send : "))

        if not is_visible("//input[@placeholder='Search']",self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
        search_box = self.driver.find_element_by_xpath("//input[@placeholder='Search']") # selecting search box
        search_box.send_keys('#'+hashtag)
        
        if not is_visible('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]').send_keys(Keys.ENTER)
        time.sleep(5)
        
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        href_found = self.driver.find_elements_by_tag_name('a')  # selecting all href
        pic_href = [ele.get_attribute('href') for ele in href_found if '.com/p' in ele.get_attribute('href')]
    
        for i in range(no_of_post):
            print(f'{i+1} post sending ..... {pic_href[i]}')
            self.driver.get(pic_href[i])

            #share
            if not is_visible('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[1]/button',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[1]/button').click()
            
            if not is_visible('/html/body/div[4]/div/div/div/div[2]/div/div[1]/div/div',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div[1]/div/div').click()
            
            #search
            if not is_visible("/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input",self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input").send_keys(user)
            
            #select
            if not is_visible('/html/body/div[5]/div/div/div[2]/div[2]/div/div/div[3]/button/span',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div[2]/div/div/div[3]/button/span').click()
            
            #send
            if not is_visible('/html/body/div[5]/div/div/div[1]/div/div[2]/div/button',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/div/button').click()
        
        

    def send_msg(self):
        try:
            user = input("Enter Username : ")
            msg = input("Enter Message : ")
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(user)
            if not is_visible('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]').click()
            if not is_visible('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/button',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/button').click()                           
            if not is_visible('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea').send_keys(msg)
            if not is_visible('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button',self.driver): raise RuntimeError("Something Went Wrong, Try Again !") 
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button').click()

            print(f'Message : {msg} to account : {user} sent......')
        except:
            print('Something went wrong try again!!')


        

insta_bot = InstaBot(username,pw)

while True:
    print('Select your Choice :')
    print('1. Get Unfollowers List')
    print('2. Message Anyone')
    print('3. Like and Comment Through Hashtag')
    print("4. Comment on someone's post")
    print("5. Send Post to Someone through Hashtag ( max : 10 )")
    print("6. quit")
    c = int(input("Enter your chocie : "))

    if c == 1:
        insta_bot.get_unfollowers()
    elif c == 2:
        insta_bot.send_msg()
    elif c == 3:
        insta_bot.like_comment_by_hashtag()
    elif c == 4:
        insta_bot.comment_on_account()
    elif c == 5:
        insta_bot.send_post_by_hashtag()
    elif c == 6:
        break
    else:
        print('Wrong Choice, Try Again!')


