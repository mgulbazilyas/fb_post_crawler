import pandas as pdimport requestsrequests.adapters.DEFAULT_RETRIES = 3url = "http://pyadmin.season-life.co.uk/api/"import repattern = r'[ ,\.!?-\^]'class con:    def __init__(self, path=''):        self.df = []        self.get_jobs()        pass        # self.path = path        # self.createcon();self.total=0        # self.query = '''insert into seasonli_jobsapi.`job_detail` (message,post_time,email_id,post_id,location_id) VALUES (%s,%s,%s,%s,%s)'''        # self.add_link_query = "insert into seasonli_fbgroup.profile_links (profile_link,Profile_Name) values (%s,%s)"    # def createcon(self):    #     self.con = mysql.connector.connect(host="138.68.134.43",    #                                         user="seasonli_fbuser",    #                                         password="facebook1",    #    #     )    #     # print("succesfull")    def get_jobs(self):        endpoint = 'jobsall/?page_size=2000'        j = requests.get(url+endpoint).json()        df = pd.DataFrame(j['results'])        try:            df.message = df.message.str.strip().str.lower().str.replace(pattern, '', True)            df.message = df.message.str[:25]        except:            df['message'] = ''            df['email_id'] = ''        self.df = df    def get_blocked(self):        endpoint = 'blocked-emails'        r = requests.api.get(url+endpoint).json()        emails = []        for email in r:            emails.append(email.get('email').strip())        return emails    def add_link(self,link,name):        endpoint = 'add-profile/'        data = {            'profile_link': link,            'profile_name': name,        }        r = requests.api.post(url+endpoint,json=data,timeout=2)        if r.status_code == 201:            return True        else:            return False    def get_groups(self, account_id: int=23):        endpoint = 'groups'        r = requests.api.get(url+endpoint).json()        groups = []        for group in r:            if int(group.get('account'))==account_id:                groups.append(group.get('link').strip())        return groups    def addData(self,data):        group = data[0]        post_text = data[1]        title = data[3]        experience = data[4]        size = data[5]        email = data[2]        endpoint = 'jobs/'        x = ((self.df.email_id == email) & (self.df.message.str[:25] == re.sub(pattern,'',post_text[:25]).lower())).any()        if x:            f=open("runner.txt",'a')                        print("Duplicate Detected")            print("Duplicate Detected",file = f)            f.close()            return False        data = {            'message': post_text,            'email_id': email,            'location_id': 1        }            try:            r = requests.api.post(url+endpoint,json=data,timeout=3)            self.df = self.df.append([{            'message': post_text[:50],            'email_id': email,            'location_id': 1            }])            if r.status_code == 201:                return r.json().get('post_id')            else:                f=open("runner.txt",'a')                print('Failed to Post')                print('Failed to Post', file=f)                f.close()                return False        except Exception as e:             print(e)            f= open("runner.txt","a")            print(e,file=f)            f.close()            f=open("runner.txt",'a')            print('Failed to Post')            print('Failed to Post',file = f)            f.close()            return False                                    