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
        attachments[0]['pretext'] = f"{user_id} 가  {problem_title} 문제를 풀었습니다"
        attachments[0]["title"] = f"{problem_title}"
        attachments[0]["title_link"] = f"https://www.acmicpc.net/problem/{problem_id}"
        attachments[0]["fields"][0]["value"] = f"{language}"
        attachments[0]["fields"][1]["value"] = f"{time} ms"
        attachments[0]["fields"][2]["value"] = f"{memory} B"
        self.send_message(channel="#dev-playground", attachments=attachments)

    def send_message(self, message=None, channel="#dev-playground", username="SCCC Playground", attachments=None):
        self.slack.chat.post_message(channel=channel,text=message, username=username, attachments=attachments)



