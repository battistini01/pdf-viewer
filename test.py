from dotenv import load_dotenv
from lambda_function import lambda_handler
import os

load_dotenv()
media_bucket = os.environ.get('MEDIA_BUCKET')


test_event = {
    "pathParameters": {
        "postid": "686e50a2ff55401a8d6a1e74"
    }
}

response = lambda_handler(test_event, None)

print("Lambda response:", response)
