import re
import requests
import json
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.exceptions import *
BOJ_URL = 'https://www.acmicpc.net'
from utils.slack_utils import message

last_submission_id = None

class Boj:

    def __init__(self):
        self.user_id = None
        self.cookie = None
        print(settings.BASE_DIR)
        self.file_path = settings.BASE_DIR + "/utils/last_submission_id"
        print(self.file_path)
        self.slack = message()
        with open(self.file_path, 'r') as f:
            tmp_last_submission_id = f.read()
            if len(tmp_last_submission_id) == 0:
                self.last_submission_id = None
            else:
                self.last_submission_id = int(tmp_last_submission_id)

    def login_boj(self, id, password):
        url = 'https://www.acmicpc.net/signin'
        post_body = {
            'login_user_id': id,
            'login_password': password
        }

        res = requests.post(url=url, data=post_body, allow_redirects=False)

        if (res.status_code != 302) or (not 'Set-Cookie' in res.headers) or (not 'Location' in res.headers) or ('error' in res.headers['Location']):
            return False

        cookie = ''
        cookie_cfduid = False
        cookie_oj = False
        for element in re.split(',| ', res.headers['Set-Cookie']):
            if '__cfduid' in element:
                cookie += element + ' '
                cookie_cfduid = True
            if 'OnlineJudge' in element:
                cookie += element
                cookie_oj = True

        if not (cookie_cfduid and cookie_oj):
            return False

        self.user_id = id
        self.cookie = cookie
        return True

    def get_group_solving_log(self, top=None):
        url = 'https://www.acmicpc.net/status'
        headers = {'Cookie' : self.cookie}
        if top is None:
            params = {"language_id":"-1", "result_id":"4", "group_id":"543"}
        else:
            params = {"language_id": "-1", "result_id": "4", "group_id": "543", "top": top}
        res = requests.get(url=url, headers=headers, params=params)

        if res.status_code != 200:
            return False
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find(id='status-table').tbody
        rows = table.find_all('tr')
        new_solved_list = []
        for row in rows:
            try:
                items = row.find_all('td')

                problem = {}
                problem['submission_id'] = int(items[0].text)
                problem['user_id'] = items[1].a.text
                problem['problem_id'] = items[2].a.text
                problem['problem_title'] = items[2].a['title']
                problem['memory'] = items[4].text
                problem['time'] = items[5].text
                problem['language'] = items[6].text
                problem['length'] = items[7].text
                problem['date'] = items[8].a['title']
                if (self.last_submission_id == None):
                    new_solved_list.append(problem)
                    break
                elif (self.last_submission_id < problem['submission_id']):
                    new_solved_list.append(problem)
                else:
                    break
            except Exception as e:
                print(items)
                self.message.send_message(message=e, channel="#dev-playground", username="SCCC Playground")
                self.message.send_message(message=str(items), channel="#dev-playground", username="SCCC Playground")
                pass
   
        if len(rows) == len(new_solved_list):
            tmp_list = self.get_group_solving_log(top=new_solved_list[-1]['submission_id'])
            new_solved_list.extend(tmp_list)

        if len(new_solved_list) != 0 and top is None:
            self.last_submission_id = new_solved_list[0]['submission_id']
            with open(self.file_path, 'w') as f:
                f.write(str(self.last_submission_id))
        return new_solved_list

