import json
import boto3
import os
import telebot

def handler(event, context):

    S3_ACCESS_KEY = os.environ['S3_ACCESS_KEY']
    S3_SECRET_KEY = os.environ['S3_SECRET_KEY']
    DB_ACCESS_KEY = os.environ['DB_ACCESS_KEY']
    DB_SECRET_KEY = os.environ['DB_SECRET_KEY']
    DB_BUCKET = os.environ['DB_BUCKET']
    DB_MESSAGE_OBJECT = os.environ['DB_MESSAGE_OBJECT']
    DB_NAME_OBJECT = os.environ['DB_NAME_OBJECT']
    IMAGES_BUCKET_ID = os.environ['IMAGES_BUCKET_ID']
    TG_TOKEN = os.environ['TG_TOKEN']
    CHAT_ID = int(os.environ['CHAT_ID'])
    
    s3 = boto3.resource(service_name='s3', endpoint_url='https://storage.yandexcloud.net',
                        aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)

    db_s3 = boto3.resource(service_name='s3', endpoint_url='https://storage.yandexcloud.net',
                        aws_access_key_id=DB_ACCESS_KEY, aws_secret_access_key=DB_SECRET_KEY)
    
    data = json.loads(event["body"])
    message = data['message']
    message_text = message['text']

    if 'entities' in message:
        entities = message['entities']
        splited_message = message_text.split(maxsplit = 1)
        if (entities[0]['type'] == 'bot_command') and (splited_message[0] == "/find"):
            b_names = downloadFileLikeObject(db_s3, DB_BUCKET, DB_NAME_OBJECT)
            dic_names = json.loads(b_names)
            name = splited_message[1]
            paths = getImagesPath(name, dic_names)
            sendInfoByName(TG_TOKEN, CHAT_ID, name, paths, s3, IMAGES_BUCKET_ID)

    if 'reply_to_message' in message:
    
        repl_message_id = message['reply_to_message']['message_id']
        b_dic = downloadFileLikeObject(db_s3, DB_BUCKET, DB_MESSAGE_OBJECT)
        b_names = downloadFileLikeObject(db_s3, DB_BUCKET, DB_NAME_OBJECT)

        dic = json.loads(b_dic)
        names = json.loads(b_names)
       
        if str(repl_message_id) in dic:
            
            object_id = dic[str(repl_message_id)]
            addName(message_text, object_id, names)
            j = json.dumps(names)
            uploadObjectLikeFile(db_s3, DB_BUCKET, DB_NAME_OBJECT, j)
            
    return {
        'statusCode': 200,
        'body': 'Fine',
    }

def downloadFileLikeObject(s3, bucketId, objectId):
    response = s3.Object(bucketId, objectId).get()
    print(response)
    return response['Body'].read()


def uploadObjectLikeFile(s3, bucketId, objectId, fileBody):
    newFile = s3.Object(bucketId, objectId)
    newFile.put(Body=fileBody)

def addName(name, object_id, d):
    if name in d:
        if object_id not in d[name]:
            new_list = d[name]
            new_list.append(object_id)
    else:
        d[name] = [object_id]

def getImagesPath(name, d):
    if name in d:
        return d[name]
    else:
        return []

def sendInfoByName(token, chat_id, name, object_list, s3, bucketId):
    if len(object_list) == 0:
        message = "Фотографии с " +  name +" не найдены"
        sendMessage(token, chat_id, message)
    else:
        sendImages(token, chat_id, object_list, s3, bucketId)   

def sendImages(token, chat_id, object_list, s3, bucketId):
    for object_id in object_list:
        b = downloadFileLikeObject(s3, bucketId, object_id)
        sendImageToUser(token, chat_id, b)

def sendImageToUser(token, chat_id, img):
    tb = telebot.TeleBot(token)
    tb.send_photo(chat_id, img)

def sendMessage(token, chat_id, message):
    tb = telebot.TeleBot(token)
    tb.send_message(chat_id, message)