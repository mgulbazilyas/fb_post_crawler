# In[1]import pickleimport osimport randomimport sysimport refrom random import randintfrom selenium.common import exceptionsfrom selenium.webdriver.chrome.options import Optionsfrom selenium.webdriver import Chromefrom selenium.webdriver.common.by import Byfrom webdriver_manager.chrome import ChromeDriverManagerimport timefrom webdriver_manager.utils import ChromeTypeimport mysqldataimport datetimeimport pyrebaseimport yamlimport loggingimport datetimetoday = datetime.datetime.now().strftime('%d-%b-%Y')os.makedirs('logs', exist_ok=True)"""%(pathname)s Full pathname of the source file where the logging call was issued(if available).%(filename)s Filename portion of pathname.%(module)s Module (name portion of filename).%(funcName)s Name of function containing the logging call.%(lineno)d Source line number where the logging call was issued (if available)."""name = 'facebook-crawler'level = 10logger = logging.getLogger(name)handler = logging.StreamHandler()formatter = logging.Formatter('[%(name)s] - %(message)s')handler.setFormatter(formatter)streamHandler = logging.FileHandler(f'logs/facebook-crawler-{today}.log')formatter = logging.Formatter('%(asctime)s [%(name)s] - %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')streamHandler.setFormatter(formatter)logger.addHandler(streamHandler)logger.addHandler(handler)logger.setLevel(level)logger2 = logging.getLogger('post-texts')handler = logging.FileHandler(f'logs/post-text-{today}.log')handler.setLevel(10)formatter = logging.Formatter('-' * 50 + '\n%(message)s')handler.setFormatter(formatter)logger2.addHandler(handler)if not os.path.exists('runner.txt'):    with open('runner.txt', 'w') as file:        file.write('File Created')filename = 'logininfo.txt'if os.path.exists(filename):    with open(filename, 'r', encoding='utf-8') as file:        config = yaml.load(file, Loader=yaml.FullLoader)else:    input(filename+' Not Exist\n Add file. and then enter.')email_ending = ['.co.uk', '.com.au', '.es', '.ru', '.ge', '.fr', '.ph', '.gr', '.com.cy', '.it', '.com.cy', '.wp.pl',                '.com']open2 = openfirebaseConfig = {    'apiKey': "AIzaSyARUhOP1jwlYPURuevEMBYWADP2hwx2X8Q",    'authDomain': "admin-app-467bf.firebaseapp.com",    'databaseURL': "https://admin-app-467bf.firebaseio.com",    'projectId': "admin-app-467bf",    'storageBucket': "admin-app-467bf.appspot.com",    'messagingSenderId': "905924835344",    'appId': "1:905924835344:web:8c32cadfc547830c10f295",    'measurementId': "G-0NKJW34D2J"}firebase = pyrebase.initialize_app(firebaseConfig)db = firebase.database()def scriptHandler(message):    global runnerScript    global self    runnerScript = message['data']    if not runnerScript:        # self.quit()        exit()# runnerScript = db.child("scripts").child("runner_script").get()# runnerScript = runnerScript.val()with open('title.pickle', 'rb') as file:    TITLES = pickle.load(file)greetPattern = re.compile("^ *((hi+)|((good )?morning|evening|afternoon)|(he((llo)|y+)))\ *$", re.IGNORECASE)chrome_options = Options()# chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"# chrome_options.add_argument('user-data-dir=user_data')# chrome_options.add_extension('extension_name.zip')chrome_options.add_argument("--disable-notifications")chrome_options.add_argument("--disable-infobars")chrome_options.add_argument("start-maximized")chrome_options.add_argument("--no-sandbox")if config.get('headless'):    chrome_options.add_argument('--headless')chrome_options.add_argument('--disable-dev-shm-usage')email_endings = '|'.join(email_ending)try:    executable_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()except:    try:        executable_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()    except:        executable_path = Nonedef getlink(link):    temp = link.split('?')    if temp[0].endswith('.php'):        return temp[0] + '?' + temp[1].split('&')[0]    else:        return temp[0]def extract_email(line):    try:        match = re.search(r'[\w.-]+@[\w-]+({})'.format(email_endings), line)        return match.group(0)    except Exception as e:        logging.info('Failed to get email')        # logging.exception(e)        return ''def verify_time(time_el):    current = datetime.datetime.now()    try:        posted_date = datetime.datetime.fromtimestamp(            int(time_el.find_element_by_css_selector('abbr.timestamp.livetimestamp').get_attribute('data-utime')))        # print(' Post Date: ', posted_date)    except:        # print("Failed Getting Time")        return True    if posted_date < current - datetime.timedelta(days=5):        return False    else:        return Truedef writeToFile(txt):    f = open("runner.txt", "a")    f.write(txt + "\n")    f.close()class Setup:    def __init__(self, posts=[], blocked_emails=[]):        self.post_data = []        self.__user = config.get('username')        self.__passwd = config.get('password')        if executable_path:            self.driver = Chrome(chrome_options=chrome_options, executable_path=executable_path)        else:            self.driver = Chrome(chrome_options=chrome_options)        self.driver.set_window_size(1200, 1000)        self.driver.get("https://www.facebook.com")        try:            self.login()        except Exception as e:            logging.info("ALready Logged in")        self.posts = posts        self.blocked_emails = blocked_emails  # blocked Emails    def check_login_needed(self) -> bool:        pass    def login(self):        user, passwd = self.__user, self.__passwd        try:            time.sleep(2)            self.driver.find_element_by_css_selector('[data-testid="cookie-policy-dialog-accept-button"]').click()            time.sleep(1)        except:            try:                el = self.driver.find_element(By.CSS_SELECTOR,'button[title="Allow Essential and Optional Cookies"]')                el.click()                # self.driver.execute_script('arguments[0].click();', el)                time.sleep(2)            except Exception as e:                pass                # print(e)                # input("Press Enter")        self.driver.find_element_by_css_selector('[name="pass"]').click()        self.driver.find_element_by_css_selector('[name="pass"]').send_keys(passwd)        self.driver.find_element_by_css_selector('[name="email"]').clear()        self.driver.find_element_by_css_selector('[name="email"]').send_keys(user)        self.driver.find_element_by_xpath('//*[@type="submit"]').click()        time.sleep(1)    def add_done(self):        pass    def action(self):        pass    def quit(self):        self.driver.quit()    def crawl_group(self, link):        # test link 	https://www.facebook.com/groups/palmayachtcrew/         self.driver.get(link + '?sorting_setting=CHRONOLOGICAL')        # self.group_name = self.driver.find_element_by_css_selector('h1#seo_h1_tag').text        # Get All Posts.        print("Scrolling")        writeToFile("Scrolling")        for i in range(randint(2, 5)):            self.driver.execute_script('window.scrollBy(0,3500);')            print("scrolled", i, end='\r', flush=True)            writeToFile("scrolled " + str(i))            time.sleep(randint(5, 15))        print("Getting data From post")        writeToFile("Getting data From post")        allposts = [i for i in                    self.driver.find_elements_by_css_selector('[data-pagelet="GroupFeed"] [role=feed] > div')                    # if verify_time(i)                    ][1:]        # self.crawl_links()        for i in allposts:            self.crawl_post(i)            time.sleep(0.5)    def crawl_links(self):        POST_CSS = "[data-testid=\"newsFeedStream\"] h5 span a.profileLink[title]"        links = self.driver.find_elements_by_css_selector(POST_CSS)[2:]        for i in links:            link = getlink(i.get_attribute('href'))            name = i.get_attribute('title')            # connection.add_link(link, name)    def crawl_post(self, element):        try:            text_el = element.find_element_by_css_selector('[data-ad-preview="message"]')            for button in text_el.find_elements_by_css_selector('[role="button"]'):                if button.text.lower() =='See More'.lower():                    try:                        button.click()                        time.sleep(1)                    except: pass            text = text_el.text            try:                logger2.critical(text)            except UnicodeEncodeError:                pass            if random.randint(0, 1):                self.driver.execute_script('arguments[0].click();',                                           element.find_element_by_css_selector('[aria-label="Like"]'))            email = extract_email(text)            if email == '':    return False            if email in self.blocked_emails:                # print(email, "blacklisted")                return False            if text in self.posts:                return False            self.posts.append(text)            # group_name = self.group_name            title, experience, size = ('', '', '')  # get_features(text)            self.post_data.append(['', text, email, title, experience, size])            return True        except (exceptions.NoSuchElementException):            print("Post Text Not Found")            return False        except (exceptions.StaleElementReferenceException):            print("Stale Element")            pass    def __del__(self):        global open2        try:            self.driver.close()        except:            pass        with open2('data.pickle', 'wb') as wb:            pickle.dump(self.post_data, wb)# In[3]posted_data = []self = Nonedef main():    global self    connection = mysqldata.con('')    # emails    x = []    blocked_emails = connection.get_blocked()    # emails = []    self = Setup(x, blocked_emails=blocked_emails)    db.child("scripts").child("runner_script").stream(scriptHandler)    groups = connection.get_groups(int(config.get('account_id')))    while 1:        random.shuffle(groups)        for link in groups:            self.crawl_group(link)            logging.info("Get data Successful from\t"+ link)            logging.info(f'total = {len(self.post_data)}')            for i in range(len(self.post_data)):                data = self.post_data.pop()                success = connection.addData(data=data)                if success:                    posted_data.append(success)        print('ran for one time')        self.driver.find_element_by_css_selector('[aria-label="Facebook"][href="/"]').click()        writeToFile('ran for one time')        time.sleep(150)        if runnerScript:            print("idhar aya")            db.child("scripts").update({"runner_script": False})            print("made it false")            db.child("scripts").update({"runner_script": True})            print("made it true")# %%import traceback as tbif __name__ == '__main__':    try:        main()    except Exception as e:        with open('error.txt','a') as stream:            stream.write(str(e))        logging.exception(e)        raise e