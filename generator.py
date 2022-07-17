
import random
import requests
import datetime
from bs4 import BeautifulSoup as bs4
from fake_useragent import UserAgent

USER_AGENTS = [
    "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Firefox/59",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
]

def gen_user_agent() -> str:
    user_agent = random.choice(USER_AGENTS)
    try:
        user_agent = UserAgent().random
    except Exception:
       pass
    return user_agent


def get_header():
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "User-Agent": gen_user_agent(),
        }
        return headers


# import phonenumbers 
# from phonenumbers import carrier
# from phonenumbers.phonenumberutil import number_type

# number = "+49 176 1234 5678"
# carrier._is_mobile(number_type(phonenumbers.parse(number))) 


def get_random(list):
    return random.choice(list)

class Blocker:
    
    def __init__(self) -> None:
        self.messages = dict()
        self.numbers = list()
        self.number_index = 0
        self.urls=list()
        self.set_all_engines()
        self.current_number = self.numbers[self.number_index]

        
    def get_soup(self,webpage):
        soup = bs4(webpage,features="lxml")
        return soup


    def get_async_results(self,func):
        [func(self.call_async_request(i)) for i in self.urls]
                       
    def call_async_request(self,url):
        header= get_header()
        response = requests.get(url,headers=header)
        return self.get_soup(response.text)
 
    def get_message(self,number):
        if number['site']=='oksms':
            self.oksms_child(number)
        elif number['site']=='freesms':
            self.free_sms_child(number) 

    def display(self,refresh=True,time_offset=120,filter_sender=None,filter_message=None,index=-1,number_str=None,paginate=None,random=False):
        if refresh:
            while True:
                self.__display_message(time_offset=time_offset,filter_sender=filter_sender,filter_message=filter_message,index=index,number_str=number_str,paginate=paginate)
                put = input("'enter':continue,'q':stop,'n':next,p:previous,time={int value}:change time\n")
                if put is 'q':
                    break
                elif put is 'n':
                    self.next(random)
                    index=-1
                    number_str=None
                elif put is 'p':
                    self.previous() 
                    index=-1
                    number_str=None
                else:
                    arg = put.split('=')
                    if len(arg) ==2:
                        if 'time' == arg[0].strip():
                            try:
                                time_offset = int(arg[1].strip())
                            except:
                                print('Enter interger as Time value')
        else:
            self.__display_message()

    def next(self,random_=True):
        if random_:
            print(self.current_number,self.number_index)
            self.current_number = get_random(self.numbers)
            
            index,_=self.check_numbers(self.current_number['number'])
            self.number_index = index
            print(self.current_number,self.number_index)
        else:
            self.number_index+=1 if self.number_index < len(self.numbers) else self.number_index
            self.current_number = self.numbers[self.number_index]
        #self.display()


    def previous(self):
        self.number_index-=1 if self.number_index > 0 else self.number_index   
        self.current_number = self.numbers[self.number_index]
        #self.display()

    def set_all_engines(self):
        self.oksms()
        self.free_sms()

    def oksms(self):
        soup = self.call_async_request("https://oksms.org/us-phone-numbers")
        self.numbers.extend(list({'number':i.span.text.replace(' ',''),'receive_link':f"https://oksms.org{i.a['href']}",'site':'oksms','country':'US'} for i in soup.select('div[class="card-body"] li[class="list-group-item"]')))
        
    def oksms_child(self,number):
        soup = self.call_async_request(number['receive_link'])
        messages_objects = soup.select('div[class="card mb-4 shadow-md"]')
        self.messages[number['number']] = list() 
        for message_object in messages_objects[3:]:
            timestamp =datetime.datetime.strptime(message_object.time['datetime'],'%Y-%m-%dT%H:%M:%S.%f').timestamp()
            content = list(filter(lambda x:x is not '',message_object.text.split('\n'))) 
            duration = content[0].strip(' ')
            sender = content[1].strip('From: \r')
            body = ''.join(content[2:]).strip()
            self.messages[number['number']].append(dict(timestamp=timestamp,duration=duration,sender=sender,body=body))    
    
    def free_sms(self):
       self.urls = list()
       soup =  self.call_async_request('https://receive-sms-free.cc/Free-USA-Phone-Number/1.html')
       pages = int(soup.select('div[class="pagination-wrap"] li')[-1].a['href'].split('/')[-1].strip('.html'))
       [self.urls.append('https://receive-sms-free.cc/Free-USA-Phone-Number/{page}.html'.format(page=i+1)) for i in range(1,pages)]
       self.get_results_freesms(soup)
       self.get_async_results(self.get_results_freesms)

    def get_results_freesms(self,soup):
        self.numbers.extend(list(dict(number=i.span.text.replace(' ',''),receive_link=i["href"],site='freesms',country="US") for i in soup.select('li[class="wow fadeInUp"] a')))

    def free_sms_child(self,number,page=1):   
        soup = self.call_async_request(f"{number['receive_link']}{page}.html")
        timestamp_now = int(datetime.datetime.now().timestamp())
        self.messages[number['number']] = list()
        for i in ["row border-bottom table-hover","row border-bottom table-hover bg-messages"]:
            elems = soup.select(f'div[class="{i}"]')
            for elem in elems:
                body_elem = elem.select('div[class="col-xs-12 col-md-8"]')
                detail_elem = elem.select(f'div[class="mobile_show message_head"]')                
                if body_elem not in [None,'',[]] and detail_elem not in [None,'',[]]:
                   body = body_elem[0].text
                   detail = detail_elem[0].text.strip(')').split('(') 
                else:continue                
                duration = detail[-1]
                sender = detail[0].strip('From')
                time = duration.split()[:-1]
                if time[-1] in ['min','mins']:
                    timestamp= (timestamp_now - (int(time[0])*60))
                elif time[-1] in ['hours', 'hour']:
                    timestamp= (timestamp_now-int(time[0])*60*60)
                elif time[-1] in ['weeks','week'] :
                    timestamp = (timestamp_now-(int(time[0])*60*60*24*7))
                elif time[-1] in ['second','seconds']:
                    timestamp =(timestamp_now-int(time[0]))
                else:
                
                    continue  
                self.messages[number['number']].append(dict(timestamp=timestamp,duration=duration,sender=sender,body=body))    
    
    def check_numbers(self,key):
        cnt=0
        for number in self.numbers:
            if number['number'] == key:
                return cnt,number
            cnt+=1        
        return  None,None       

    def __display_message(self,time_offset=None,filter_sender=None,filter_message=None,index=None,number_str=None,paginate=None):
        if number_str != None:
            check = self.messages.get(number_str)
            if check is not None:
                self.number_index,self.current_number = self.check_numbers(number_str)
                messages = check
            else:
                ind,num = self.check_numbers(number_str)     
                if None not in[ind,num]:
                    self.number_index,self.current_number = ind,num
                    self.get_message(self.current_number)
                    messages = self.messages[self.current_number['number']]
                else: return f"No Message found For Number {number_str}"
        elif index >= 0: 
            self.current_number = self.numbers[index]
            self.get_message(self.current_number)
            messages = self.messages[self.numbers[index]['number']]
            self.number_index = index 
        else:
            self.get_message(self.current_number)
            messages = self.messages[self.current_number['number']]
        print(f"\n\nMessages Received In The Last {time_offset} Seconds On {self.current_number['country']} Number {self.current_number['number']}")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") 
        now_timestamp = (datetime.datetime.now().timestamp() - time_offset)
        for message in messages:
            #print(f"Message From: {message['sender']} {message['duration']} \n\t{message['body']}")
            if message['timestamp'] > now_timestamp:
                print(f"FROM : {message['sender']}.Receieved about {message['duration']} \nMESSAGE : {message['body']}")
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                
            

Blocker()


        













    