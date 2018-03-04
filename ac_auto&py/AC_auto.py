# hdu 
import requests
import re
import time
from bs4 import BeautifulSoup

user = 'jnxxhzzz'
userpass = '2887678z'

class AC_auto(object):
    def __init__(self):
        self.session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
        self.session.headers.update(headers)

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
        for item in res:
            if re.match("blog.csdn.net", item.text):
                solutionurls.append(item['href'])
        for item in solutionurls:
            r = baidusession.get(item)
            soup = BeautifulSoup(r.text, 'html.parser')
            #print(soup)
            code = soup.find('pre',attrs={'name': 'code'})
            if code:
                solutions.append(code.text)
                #print(code.text)
        return solutions
    
    def acc(self, start=6216, end=6263, interval=15):
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
