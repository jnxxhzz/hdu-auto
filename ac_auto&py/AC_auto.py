# hdu 
import requests
import re
import time
from bs4 import BeautifulSoup

user = 'jnxxhzzz'
userpass = '2887678z'
http_headers = { 'Accept': '*/*','Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}

class AC_auto(object):
    def __init__(self):
        self.session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
        self.session.headers.update(headers)

    def get_real_url(self,url,try_count = 1):
        rs = requests.get(url,headers=http_headers,timeout=10)
        while rs.status_code > 400:
            rs = requests.get(url,headers=http_headers,timeout=10)
            try_count = try_count + 1
            if (try_count > 3):
                break
        return rs.url
        
    def login(self, username, password):
        url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
        data = {
            'username': username,
            'userpass': password,
            'login': 'Sign In'
        }
        r = self.session.post(url, data=data)

    def submit(self, problemID, code, language=0):
        url = 'http://acm.hdu.edu.cn/submit.php?action=submit'
        code = code.encode('utf-8').decode()
        # print(code)
        data = {
            'check': 0,
            'problemid': str(problemID),
            'language': str(language),
            'usercode': code
        }
        se = self.session
        r = se.post(url, data=data)

    def getsolved(self, username):
        url = 'http://acm.hdu.edu.cn/userstatus.php?user=%s' %username
        solved = []
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        res = soup.find('p', align='left')
        # print(res)
        str = res.text.split(';')
        for item in str:
            if item:
                item = re.search(r'\d{4}', item)
                solved.append(item.group(0))
        return solved

    def getcsdn(self, problemID):
        solutions = []
        solutionurls = []
        url = r'http://www.baidu.com/s?wd=hdu%20' + str(problemID) +'%20csdn' #r防止转义
        baidusession = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
        baidusession.headers.update(headers)
        r = baidusession.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        res = soup.find_all('a', attrs={'target': '_blank', 'class': 'c-showurl', 'style': 'text-decoration:none;'})
        csdn = "blog.csdn.net"
        for item in res:
            realurl = str(ac.get_real_url(item['href']))
            if csdn in realurl:
                solutionurls.append(realurl)

        for item in solutionurls:
            r = baidusession.get(item)
            soup = BeautifulSoup(r.text, 'html.parser')
            #print(soup)
            code = soup.find('code',attrs={'class': 'language-cpp'})
            if code:
                solutions.append(code.text)
        return solutions
    
    def acc(self, start=6287, end=6500, interval=15):
        language = 0
        for problemID in range(start, end):
            print("Problem",problemID,end=" ")
            if str(problemID) not in ac.getsolved(user):
                answer = ac.getcsdn(problemID)
                if answer:
                    flag = 0
                    for ans in answer:
                        if ans.find('Scanner') != -1:
                            language = 5
                        else:
                            language = 0
                        if str(problemID) not in ac.getsolved(user):
                            ac.submit(problemID, ans, language=language)
                            time.sleep(interval)
                        else:
                            flag = 1
                            break
                    if flag:
                        print('Accepted')
                    else:
                        print('')
            else:
                print("Accepted")


if __name__ == '__main__':   
    ac = AC_auto()
    ac.login(user, userpass)
    ac.acc()
