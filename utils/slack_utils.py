from slacker import Slacker
from django.conf import settings
class AttachmentsTemplate:
    default_attachment = [{
        "text": "기본 템플릿"
    }]
    solving_attachment = [
            {
                "fallback": "fail",
                "color": "#36a64f",
                "pretext": "누가 어떤 문제를 풀었어요",
                "title": "Baekjoon Online Judge",
                "title_link": "http://acmicpc.net",
                "fields": [
                    {
                        "title": "언어",
                        "value": "C++"

                    },
                    {
                        "title": "실행 시간",
                        "value": "C++"

                    },
                    {
                        "title": "메모리",
                        "value": "C++"
                    }
                ]
            }
        ]

class message:
    def __init__(self):
        self.token = settings.SLACK_KEY
        self.slack = Slacker(self.token)
    def send_solve_log(self, user_id, problem_id, problem_title, memory, time, language):
        attachments = AttachmentsTemplate.solving_attachment
        attachments[0]['pretext'] = "%s 가  %s 문제를 풀었습니다"% (user_id, problem_title)
        attachments[0]["title"] = str(problem_title)
        attachments[0]["title_link"] = "https://www.acmicpc.net/problem/%s"%(problem_id)
        attachments[0]["fields"][0]["value"] = str(language)
        attachments[0]["fields"][1]["value"] = "%s ms"%(time)
        attachments[0]["fields"][2]["value"] = "%s B"%(memory)
        self.send_message(channel="#solvelog", attachments=attachments)

    def send_message(self, message=None, channel="#dev-playground", username="SCCC Playground", attachments=None):
        self.slack.chat.post_message(channel=channel,text=message, username=username, attachments=attachments)



