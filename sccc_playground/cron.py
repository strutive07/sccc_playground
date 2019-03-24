from django.conf import settings
from utils.slack_utils import message
from utils.scraping import Boj

def scheduler():
    boj = Boj()
    boj.login_boj(settings.BOJ_ID, settings.BOJ_PASSWORD)
    solved_problems = boj.get_group_solving_log()
    broker = message()
    for problem in reversed(solved_problems):
        user_id = problem['user_id']
        problem_id = problem['problem_id']
        problem_title = problem['problem_title']
        memory = problem['memory']
        time = problem['time']
        language = problem['language']
        broker.send_solve_log(
            user_id=user_id,
            problem_id=problem_id,
            problem_title=problem_title,
            memory=memory, time=time,
            language=language
        )
