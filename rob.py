import login
import threading
import json
import sys
import time
from bs4 import BeautifulSoup
import requests

THREAD_FLAG = True

def logging(foo):
    def wrapper(*args):
        print('[*]尝试登录中...')
        foo(*args)
        print('[*]登录成功!')
        print('[*]启动线程中...')
    return wrapper

class Rob_Lessons(login.Loginer):
    
    def __init__(self, user, passwd, lesson_id):
        super().__init__(user, passwd)
        self.lesson_id = lesson_id
        self.header_1 = {
            'Accept':'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',	
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep-alive',
            'Content-Length':'470',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'202.119.206.62',
            'Referer':'http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su='+self.user,
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'	
        }        
               
    def lessons_info(self):
        self.header_2 = {
            'Accept':'application/json, text/javascript, */*; q=0.01',	
            'Accept-Encoding':'gzip, deflate',
            'Host':'jwxt.cumt.edu.cn',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded;charset=utf-8',
            'Referer':'http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su='+self.user,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'X-Requested-With':	'XMLHttpRequest',
            'Cookie':self.cookie
        }                 
        print('[*]尝试获取课程信息...')
        try:
            index_url = 'http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su='+self.user
            search_url = 'http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su='+self.user
            choose_url = 'http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su='+self.user
            rob_url = 'http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_xkBcZyZzxkYzb.html?gnmkdm=N253512&su='+self.user
            text = BeautifulSoup(login.httpmthd.sessions.get(index_url, headers = self.header_1).text, "html.parser")
            xkkz = text.findAll(name='input', attrs={'type':"hidden",'name':"firstXkkzId",'id':"firstXkkzId"})[0].attrs['value']
            data = {
                'bh_id':'161031108',
                'bklx_id':'0',
                'ccdm':'3',
                'filter_list[0]':self.lesson_id,
                'jg_id':'03',
                'jspage':'10',
                'kkbk':'0',
                'kkbkdj':'0',
                'kklxdm':'10',
                'kspage':'1',
                'njdm_id':'2016',
                'njdmzyh':' ',
                'rwlx':'2',
                'sfkcfx':'0',
                'sfkgbcx':'0',
                'sfkknj':'0',
                'sfkkzy':'0',
                'sfkxq':'0',
                'sfrxtgkcxd':'1',
                'sfznkx':'0',
                'tykczgxdcs':'10',
                'xbm':'1',
                'xh_id':self.user,
                'xkly':'0',
                'xkxnm':'2018',
                'xkxqm':'3',
                'xqh_id':'2',
                'xsbj':'4294967296',
                'xslbdm':'421',
                'zdkxms':'0',
                'zyfx_id':'wfx',
                'zyh_id':'0311'         
            }
            search_result = requests.post(search_url, data = data, headers = self.header_2).json()
            kch = search_result['tmpList'][0]['kch_id']
            jxb = search_result['tmpList'][0]['jxb_id']
            kcmc = search_result['tmpList'][0]['kcmc']
            self.kcmc = kcmc
            xf = search_result['tmpList'][0]['xf']
            self.rob_data = {
                'cxbj':'0',
                'jxb_ids':jxb,
                'kch_id':kch,
                'kcmc':'('+self.lesson_id+')'+kcmc+'+-+'+xf+'学分',
                'kklxdm':'10',
                'njdm_id':'2016',
                'qz':'0',
                'rlkz':'1',
                'rlzlkz':'0',
                'rwlx':'2',
                'sxbj':'1',
                'xkkz_id':xkkz,
                'xklc':'1',
                'xkxnm':'2018',
                'xkxqm':'3',
                'xsbxfs':'0',
                'xxkbj':'0',
                'zyh_id':'0311'        
            }
            print('[*]课程信息获取成功!')
        except:
            print('[*]获取失败，请查验课程代号')
            sys.exit()
            
            
    def _get_csrftoken(self):                   
        url = 'http://202.119.206.62/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=' + str(self.time)
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        self.token = soup.find('input', attrs={'id':'csrftoken'}).attrs['value'] 
        
        
    def lessons(self, no):
        global THREAD_FLAG
        url = 'http://jwxt.cumt.edu.cn/jwglxt/xsxk/zzxkyzb_xkBcZyZzxkYzb.html?gnmkdm=N253512&su=' + self.user
        print('[*]Thread-'+no+' Start')
        while True:
            if THREAD_FLAG:
                try:
                    response = requests.post(url, data = self.rob_data, headers = self.header_2, timeout = 5)
                    if len(response.text) > 10000:
                        #self.reflush_time()
                        #self.get_public()
                        #self._get_csrftoken()
                        #self.post_data()
                        self.login_us()
                    print('[*]Thread-'+no+'  请求成功')
                    if response.json()['flag'] != '1':
                        print('[*]Thread-'+no+'  异常!')
                        print('[*]异常状态码: '+response.json()['msg'])
                        raise Exception
                    print('[*]Thread-'+no+'  Success!')
                    print('[*]'+self.kcmc+'  抢课成功!')
                    print('[*]程序即将退出...')
                    THREAD_FLAG = False
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    print('[*]Thread-'+no+'  Fail')
            else:
                print('[*]Thread-'+no+' Close')
                return

    def generate_thread(self,count):
        self.thread=[]
        for i in range(count):
            self.thread.append(threading.Thread(target=self.lessons, args=(str(i+1),)))      
    
    @logging
    def login_us(self):
        self.reflush_time()
        self.get_public()
        self.get_csrftoken()
        self.post_data()
        
    def rob_it(self, count):
        self.login_us()
        self.generate_thread(count)
        self.lessons_info()
        for pro in self.thread:
            pro.start()

def config():
    user_passwd = []
    try:
        with open('config.json', 'r') as conf:
            data = json.load(conf)
            return [data['user'].strip(), data['passwd'].strip(), data['lesson_id'].strip()]
    except:
        print('[*]Error')
        print('[*]请检查配置文件config.json')
        sys.exit()

def welcome():
    print('')
    print(" _                                                 _              _             ___          ")
    print("|_)   _   |_     |    _    _   _   _   ._    _    |_   _   ._    /   | |  |\/|   |    _   ._ ")
    print("| \  (_)  |_)    |_  (/_  _>  _>  (_)  | |  _>    |   (_)  |     \_  |_|  |  |   |   (/_  |  ")
    print('')
    print('')
    print('[+]Made By EddieIvan')
    print('[+]Github: http://github.com/eddieivan01')
    print('')
    
if __name__ == '__main__':
    welcome()
    MAX_PROCESS = int(input("[*]Please Input The Count of Thread:(1-8) "))
    if MAX_PROCESS > 8:
        print('同学，为学校的服务器考虑一下...')
        sys.exit()
    user_config = config()
    Robber = Rob_Lessons(user_config[0], user_config[1], user_config[2])
    Robber.rob_it(MAX_PROCESS)
