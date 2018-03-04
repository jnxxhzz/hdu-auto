# hdu 
import requests
import re
import time
from bs4 import BeautifulSoup

user = 'RunnerUp'
userpass = 'runnerup'
user1 = 'jnxxhzzz'
userpass1 = '2887678z'


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
        
    def logout(self):
        url = 'http://acm.hdu.edu.cn/userloginex.php?action=logout'
        data={
            'action':'logout'
        }
        se=self.session
        r = se.post(url)

    def submit(self, problemID, code, language=0):
        ac.logout()
        ac.login(user1,userpass1)
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
        ac.logout()


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

    def getdm(self, nowproblem,problemID):
        solutions = []
        ac.logout()
        ac.login(user,userpass)
        data = {
            'username': user,
            'userpass': userpass,
            'login': 'Sign In'
        }
        url = 'http://acm.hdu.edu.cn/viewcode.php?rid='+str(nowproblem)
        se = self.session
        r = se.post(url,data=data)
        soup = BeautifulSoup(r.text, 'html.parser')
        #print(soup)
        soup1 = soup.find('textarea',attrs={'id':'usercode','style':'display:none;text-align:left;'})
        if soup1:
            solutions.append(soup1.text)
        else:
            print('not')    
        
        for codee in solutions:
            code = codee
            code = code.encode('utf-8').decode()
            ac.submit(problemID,code)
            return code


    def getcode(self, problemID):
        solutions = []
        solutionurls = []
        url = r'http://acm.hdu.edu.cn/status.php?first=&pid='+ str(problemID) +'&user=Runnerup&lang=0&status=5'
        baidusession = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
        baidusession.headers.update(headers)
        r = baidusession.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        soup2 = soup.find('td',attrs={'height':'22px'})
        solutions.append(soup2.text)
        flag = 0
        for codee in solutions:
            code=codee
            code = code.encode('utf-8').decode()
            nowproblem = int(code)
            problemID = int(problemID)
            print(nowproblem,end=' ')
            ans=ac.getdm(nowproblem,problemID)
            flag = 1
    
    def acc(self, start=1373, end=6000, interval=30):
        language = 0
        problemid = []
        allans = []
        for problemID in range(start, end):
            if str(problemID) in ac.getsolved(user):
                if str(problemID) not in ac.getsolved(user1):
                    print("Problem",problemID,end=" ")
                    ac.getcode(problemID)
                    print('Acceped')
                    time.sleep(interval)



if __name__ == '__main__':   
    ac = AC_auto()
    ac.acc()
