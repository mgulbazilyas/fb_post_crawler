# In[1]


import pickle

import os

import random

import sys

import re

from random import randint

from selenium.common import exceptions

from selenium.webdriver.chrome.options import Options

from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import time

from webdriver_manager.utils import ChromeType

import mysqldata

import datetime

import pyrebase

import yaml

import logging

import datetime

today = datetime.datetime.now().strftime('%d-%b-%Y')

"""

%(pathname)s Full pathname of the source file where the logging call was issued(if available).



%(filename)s Filename portion of pathname.



%(module)s Module (name portion of filename).



%(funcName)s Name of function containing the logging call.



%(lineno)d Source line number where the logging call was issued (if available).

"""
os.makedirs('logs', exist_ok=True)
name = 'facebook-crawler'

level = 10

logger = logging.getLogger(name)

handler = logging.StreamHandler()

formatter = logging.Formatter('[%(name)s] - %(message)s')

handler.setFormatter(formatter)

streamHandler = logging.FileHandler(f'logs/{today}.log')

formatter = logging.Formatter('%(asctime)s [%(name)s] - %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')

streamHandler.setFormatter(formatter)

logger.addHandler(streamHandler)

logger.addHandler(handler)

logger.setLevel(level)

logger2 = logging.getLogger('post-texts')

handler = logging.FileHandler(f'post-text-{today}.log')

handler.setLevel(0)

formatter = logging.Formatter('-' * 50 + '\n%(message)s')

handler.setFormatter(formatter)

logger2.addHandler(handler)

if not os.path.exists('runner.txt'):
    with open('runner.txt', 'w') as file:
        file.write('File Created')

filename = 'logininfo.txt'

if os.path.exists(filename):

    with open(filename, 'r', encoding='utf-8') as file:

        config = yaml.load(file, Loader=yaml.FullLoader)

else:

    input(filename + ' Not Exist\n Add file. and then enter.')

email_ending = ['.co.uk', '.com.au', '.es', '.ru', '.ge', '.fr', '.ph', '.gr', '.com.cy', '.it', '.com.cy', '.wp.pl',

                '.com']

open2 = open

firebaseConfig = {

    'apiKey': "AIzaSyARUhOP1jwlYPURuevEMBYWADP2hwx2X8Q",

    'authDomain': "admin-app-467bf.firebaseapp.com",

    'databaseURL': "https://admin-app-467bf.firebaseio.com",

    'projectId': "admin-app-467bf",

    'storageBucket': "admin-app-467bf.appspot.com",

    'messagingSenderId': "905924835344",

    'appId': "1:905924835344:web:8c32cadfc547830c10f295",

    'measurementId': "G-0NKJW34D2J"

}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()


def scriptHandler(message):
    global runnerScript

    global self

    runnerScript = message['data']

    if not runnerScript:
        # self.quit()

        exit()


# runnerScript = db.child("scripts").child("runner_script").get()


# runnerScript = runnerScript.val()

with open('title.pickle', 'rb') as file:
    TITLES = pickle.load(file)

greetPattern = re.compile("^ *((hi+)|((good )?morning|evening|afternoon)|(he((llo)|y+)))\ *$", re.IGNORECASE)

chrome_options = Options()

# chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"


# chrome_options.add_argument('user-data-dir=user_data')


# chrome_options.add_extension('extension_name.zip')


chrome_options.add_argument("--disable-notifications")

chrome_options.add_argument("--disable-infobars")

chrome_options.add_argument("start-maximized")

chrome_options.add_argument("--no-sandbox")

if config.get('headless'):
    chrome_options.add_argument('--headless')

chrome_options.add_argument('--disable-dev-shm-usage')

email_endings = '|'.join(email_ending)

try:

    executable_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()

except:

    try:

        executable_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()

    except:

        executable_path = None


def getlink(link):
    temp = link.split('?')

    if temp[0].endswith('.php'):

        return temp[0] + '?' + temp[1].split('&')[0]



    else:

        return temp[0]


def extract_email(line):
    try:

        match = re.search(r'[\w.-]+@[\w-]+({})'.format(email_endings), line)

        return match.group(0)



    except Exception as e:

        logging.info('Failed to get email')

        # logging.exception(e)

        return ''


def verify_time(time_el):
    current = datetime.datetime.now()

    try:

        posted_date = datetime.datetime.fromtimestamp(

            int(time_el.find_element(By.CSS_SELECTOR, 'abbr.timestamp.livetimestamp').get_attribute('data-utime')))

        # print(' Post Date: ', posted_date)



    except:

        # print("Failed Getting Time")

        return True

    if posted_date < current - datetime.timedelta(days=5):

        return False



    else:

        return True


class Setup:

    def __init__(self, posts=[], blocked_emails=[]):

        self.post_data = []

        self.__user = config.get('username')

        self.__passwd = config.get('password')

        if executable_path:

            self.driver = Chrome(chrome_options=chrome_options, executable_path=executable_path)

        else:

            self.driver = Chrome(chrome_options=chrome_options)

        self.driver.set_window_size(1200, 1100)

        self.driver.get("https://www.facebook.com")

        try:

            self.login()



        except Exception as e:

            logging.info("ALready Logged in")

        self.posts = posts

        self.blocked_emails = blocked_emails  # blocked Emails

    def check_login_needed(self) -> bool:

        pass

    def login(self):

        user, passwd = self.__user, self.__passwd

        try:

            time.sleep(2)

            self.driver.find_element(By.CSS_SELECTOR, '[data-testid="cookie-policy-dialog-accept-button"]').click()

            time.sleep(1)

        except:

            pass

        self.driver.find_element(By.CSS_SELECTOR, '[name="pass"]').click()

        self.driver.find_element(By.CSS_SELECTOR, '[name="pass"]').send_keys(passwd)

        self.driver.find_element(By.CSS_SELECTOR, '[name="email"]').clear()

        self.driver.find_element(By.CSS_SELECTOR, '[name="email"]').send_keys(user)

        self.driver.find_element(By.XPATH, '//*[@type="submit"]').click()

        time.sleep(1)

    def add_done(self):

        pass

    def action(self):

        pass

    def quit(self):

        self.driver.quit()

    def get_feed_posts(self):

        posts = self.driver.find_elements(By.CSS_SELECTOR, '[role=feed]>div[data-pagelet*="FeedUnit"]')

        len(posts)

        return posts

    def crawl_feed(self, *args):

        post_numbers = [random.choice([True, False]) for i in range(1000)]

        post_clicked = [False for i in range(1000)]

        # self.group_name = self.driver.find_element(By.CSS_SELECTOR, 'h1#seo_h1_tag').text

        logger.info("Scrolling")

        for i in range(randint(1, 5)):

            for j in range(100):
                self.driver.execute_script('window.scrollBy(0,30);')

                time.sleep(randint(5, 20) / 100)

            # posts = self.driver.find_elements(By.CSS_SELECTOR, '[role=feed]>div')

            # for index, post in enumerate(posts):
            #
            #     if post_numbers[index] and (not post_clicked[index]):
            #
            #         try:
            #
            #             post.find_element(By.CSS_SELECTOR, '[aria-label="Like"][role=button]').click()
            #
            #             post_clicked[index] = True
            #
            #             time.sleep(1)
            #
            #         except:
            #
            #             pass
            #
            #         pass
            #
            #     pass

            logger.info("scrolled " + str(i))

            time.sleep(randint(3, 10))

        logger.info("Getting data From post")

        posts = self.driver.find_elements(By.CSS_SELECTOR, '[role=feed]>div')
        logger.info(f"posts_count:{len(posts)}")
        # self.crawl_links()

        counts = 0

        for i in posts:

            # print(i, type(i))

            if self.crawl_post(i):
                counts += 1

    def crawl_links(self):

        POST_CSS = "[data-testid=\"newsFeedStream\"] h5 span a.profileLink[title]"

        links = self.driver.find_elements(By.CSS_SELECTOR, POST_CSS)[2:]

        for i in links:
            link = getlink(i.get_attribute('href'))

            name = i.get_attribute('title')

            # connection.add_link(link, name)

    def crawl_post(self, element):

        # print(element)

        try:

            text_els = element.find_elements(By.CSS_SELECTOR,
                                             '[dir="auto"]>div[id*=jsc_c], [data-ad-preview="message"]')
            try:
                for text_el in text_els:
                    for button in text_el.find_elements(By.CSS_SELECTOR, '[role="button"]'):
                        if button.text.lower() == 'See More'.lower():
                            try:
                                button.click()
                                time.sleep(1)
                            except:
                                pass
            except:
                pass
            post_text = '\n'.join([text_el.text.lower() for text_el in text_els])

            text = post_text

            try:

                logger2.critical(text)

            except UnicodeEncodeError:

                pass

            if random.randint(0, 1):
                self.driver.execute_script('arguments[0].click();',

                                           element.find_element_by_css_selector('[aria-label="Like"]'))

            email = extract_email(text)

            if email == '':    return False

            if email in self.blocked_emails:
                # print(email, "blacklisted")

                return False

            if text in self.posts:
                return False

            self.posts.append(text)

            # group_name = self.group_name

            title, experience, size = ('', '', '')  # get_features(text)

            self.post_data.append(['', text, email, title, experience, size])

            return True

        except (exceptions.NoSuchElementException, ) as e:

            print("Post Text Not Found")

            return False

        except (exceptions.StaleElementReferenceException, ):

            print("Stale Element")

            pass

    def __del__(self):

        global open2

        try:

            self.driver.close()

        except:

            pass

        with open2('data.pickle', 'wb') as wb:

            pickle.dump(self.post_data, wb)


# In[3]


posted_data = []

self = None


def main():
    global self

    connection = mysqldata.con('')

    # emails

    x = []

    blocked_emails = connection.get_blocked()

    # emails = []

    self = Setup(x, blocked_emails=blocked_emails)

    db.child("scripts").child("runner_script").stream(scriptHandler)

    # groups = connection.get_groups(int(config.get('account_id')))

    while 1:

        self.crawl_feed('')

        for i in range(len(self.post_data)):

            data = self.post_data.pop()

            logger.info('To Add' + data[2])

            success = connection.addData(data=data)

            if success:
                logger.info('Added' + data[2])

                posted_data.append(success)

        print('ran for one time')

        self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Facebook"][href="/"]').click()

        logger.info('ran for one time')

        time.sleep(7200)

        if runnerScript:
            print("idhar aya")

            db.child("scripts").update({"runner_script": False})

            print("made it false")

            db.child("scripts").update({"runner_script": True})

            print("made it true")


# %%

import traceback as tb

if __name__ == '__main__':
    try:

        main()

    except Exception as e:

        with open('error.txt', 'a') as stream:

            stream.write(str(e))

        logging.exception(e)

        raise e
