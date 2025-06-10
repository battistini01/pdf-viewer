import os
import json
import boto3
import base64

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

s3 = boto3.client('s3')

def lambda_handler(event, context):

    media_bucket = os.environ.get('MEDIA_BUCKET')
    mongo_uri = os.environ.get('MONGO_URI')
    
    if media_bucket is None:
        raise Exception('MEDIA_BUCKET environment variable not set')
    
    if mongo_uri is None:
        raise Exception('MONGO_URI environment variable not set')
    
    action = event['pathParameters']['action']
    postid = event['pathParameters']['postid']
    filename = event['pathParameters']['filename']

    match action:
        case 'view':
            action = 'inline'
        case 'download':
            action = 'attachment'

    try:
        postid = ObjectId(postid)
    except Exception:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid post id: " + postid})}

    try:
        client = MongoClient(mongo_uri, ServerSelectionTimeoutMS=5000)
        db = client['data']
        collection = db['posts']

        post = collection.find_one({ 'type': 'pdf', '_id': ObjectId(postid) })

        if not post:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": 'Post not found'})
            }
        
        post['_id'] = str(post['_id'])

        s3_response = s3.get_object(
            Bucket=media_bucket,
            Key=f'{post["brand"]}/posts/orig/{post["_id"]}.pdf'
        )

        pdf = s3_response['Body'].read()

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/pdf',
                'Content-Disposition': f'{action}; filename="{filename}"'
            },
            'isBase64Encoded': True,
            'body': base64.b64encode(pdf).decode('utf-8')
        }
    
    except ConnectionFailure as e:
        return {
            "statusCode": 500,
            "body": f"Database connection failed: {str(e)}"
        }
