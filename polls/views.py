import datetime
import json

import boto3
import redis
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from fast_sample_django.settings import REDIS_HOSTNAME, REDIS_PORT, REDIS_DB, SQS_URL
from polls.models import Question


r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, db=REDIS_DB)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def add_question(request):
    data = json.loads(request.body.decode('utf-8'))
    question = Question(question_text=data['question_text'], pub_date=datetime.datetime.now())
    question.save()
    r.set(question.id, question.question_text)
    sqs = boto3.client('sqs', region_name='ap-southeast-1')
    sqs.send_message(QueueUrl=SQS_URL, MessageBody=json.dumps({'id': question.id}))
    return HttpResponse(f"Created new question with id {question.id}")