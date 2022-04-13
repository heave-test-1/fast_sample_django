import datetime
import json
import logging

import boto3
import redis
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from fast_sample_django.settings import REDIS_HOSTNAME, REDIS_PORT, REDIS_DB, SQS_URL, CHATS_TABLE, AWS_REGION
from polls.models import Question


r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, db=REDIS_DB)
sqs = boto3.client('sqs', region_name=AWS_REGION)
dynamo = boto3.client('dynamodb', region_name=AWS_REGION)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def add_question_database(request):
    data = json.loads(request.body.decode('utf-8'))

    # Access database
    question = Question(question_text=data['question_text'], pub_date=datetime.datetime.now())
    question.save()
    logging.info("Created entry in database")

    return HttpResponse(f"Created new question with id {question.id}")


@csrf_exempt
def add_question_redis(request):
    data = json.loads(request.body.decode('utf-8'))

    # Access redis
    r.set("1", data['question_text'])
    logging.info("Created entry in redis")

    return HttpResponse(f"Created new question with id 1")


@csrf_exempt
def add_question_sqs(request):
    data = json.loads(request.body.decode('utf-8'))

    # Access SQS
    logging.info(f"SQS: {SQS_URL}")
    sqs.send_message(QueueUrl=SQS_URL, MessageBody=json.dumps(data))
    logging.info("Created entry in SQS")

    return HttpResponse(f"Created new question")


@csrf_exempt
def add_question_dynamo(request):
    data = json.loads(request.body.decode('utf-8'))

    # Access DynamoDB
    dynamo.put_item(TableName=CHATS_TABLE, Item={'uid': {'S': data['question_text']}, 'id': {'N': '1'}})
    logging.info("Created entry in DynamoDB")

    return HttpResponse(f"Created new question with id 1")
