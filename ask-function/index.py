 
import json
import boto3
import requests
import os
import telebot

def handler(event, context):
    print(event)
    S3_ACCESS_KEY = os.environ['S3_ACCESS_KEY']
    S3_SECRET_KEY = os.environ['S3_SECRET_KEY']
    DB_ACCESS_KEY = os.environ['DB_ACCESS_KEY']
    DB_SECRET_KEY = os.environ['DB_SECRET_KEY']
    DB_BUCKET = os.environ['DB_BUCKET']
    DB_OBJECT = os.environ['DB_OBJECT']

    TG_TOKEN = os.environ['TG_TOKEN']
    CHAT_ID = int(os.environ['CHAT_ID'])

    s3 = boto3.resource(service_name='s3', endpoint_url='https://storage.yandexcloud.net',
                        aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)

    db_s3 = boto3.resource(service_name='s3', endpoint_url='https://storage.yandexcloud.net',
                        aws_access_key_id=DB_ACCESS_KEY, aws_secret_access_key=DB_SECRET_KEY)

    data = event['messages'][0]
    if data['event_metadata']['event_type'] == 'yandex.cloud.events.messagequeue.QueueMessage':
        j_data = data['details']['message']['body']
        j = json.loads(j_data)
        print(j)
        bucket_id = j['bucketId']
        object_id = j['objectId']
       
        b = downloadFileLikeObject(s3, bucket_id, object_id)
        message_id = sendMessageToUser(TG_TOKEN, CHAT_ID, b, object_id)
        b_dic = downloadFileLikeObject(db_s3, DB_BUCKET, DB_OBJECT)
        dic = json.loads(b_dic)
        add_new_row(dic, message_id, object_id)
        j = json.dumps(dic)
        uploadObjectLikeFile(db_s3, DB_BUCKET, DB_OBJECT, j)

    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }

def downloadFileLikeObject(s3, bucketId, objectId):
    response = s3.Object(bucketId, objectId).get()
    return response['Body'].read()

def sendMessageToUser(token, chat_id, img, object_id):
    tb = telebot.TeleBot(token)
    message = "Кто это?"
    return tb.send_photo(chat_id, img, caption=message).message_id

def add_new_row(dic, message_id, object_id):
    dic[message_id] = object_id

def uploadObjectLikeFile(s3, bucketId, objectId, fileBody):
    newFile = s3.Object(bucketId, objectId)
    newFile.put(Body=fileBody)
