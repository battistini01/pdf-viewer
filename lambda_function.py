import os
import json
import boto3
import base64

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

s3 = boto3.client('s3')

client = None
db = None

def get_mongo_client():
    global client, db
    
    if client is not None:
        return client, db
    
    # Fetch env vars only once too
    config_bucket = os.environ.get('CONFIG_BUCKET')
    node_env = os.environ.get('NODE_ENV')
    
    # Fetch MongoDB URI from S3
    key = f"mongodb/mongodb_credentials_{node_env}.json"
    configResponse = s3.get_object(Bucket=config_bucket, Key=key)
    body = configResponse["Body"].read().decode("utf-8")
    db_credentials = json.loads(body)
    mongo_uri = db_credentials.get("MONGO_URL")
    if not mongo_uri:
        raise Exception("MONGO_URL not found in credentials")
    
    # FOR LOCAL TESTING ONLY: Use the commented line below to allow invalid certificates
    # client = MongoClient(mongo_uri, ServerSelectionTimeoutMS=5000, tls=True, tlsAllowInvalidCertificates=True)
    client = MongoClient(mongo_uri, ServerSelectionTimeoutMS=5000)
    db_name = 'data' if node_env == 'development' else 'data-prod'
    db = client[db_name]
    
    return client, db

def lambda_handler(event, context):
    
    config_bucket = os.environ.get('CONFIG_BUCKET')
    node_env = os.environ.get('NODE_ENV')
    media_url = os.environ.get('MEDIA_URL')
    
    if not config_bucket or not node_env or not media_url:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Environment variables not set"})
        }
    
    postid = event['pathParameters']['postid']

    try:
        postid = ObjectId(postid)
    except Exception:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid post id: " + postid})}

    try:
        db = get_mongo_client()[1]
        collection = db['posts']

        post = collection.find_one({ 'type': 'pdf', '_id': ObjectId(postid) })

        if not post:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": 'Post not found'})
            }
        
        post['_id'] = str(post['_id'])

        return {
            'statusCode': 302,
            "headers": {
                "Location": f"{media_url}/{post['brand']}/posts/orig/{post['_id']}.pdf",
                "Cache-Control": "max-age=31536000, public",
            },
            'body': ""
        }
    
    except ConnectionFailure as e:
        return {
            "statusCode": 500,
            "body": f"Database connection failed: {str(e)}"
        }
