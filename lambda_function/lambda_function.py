import json
import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime

# DynamoDBのセットアップ
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('news')

# Goal.com ニュースページのURL
# URL = "https://www.goal.com/jp/%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9"
URL = "https://www.goal.com/en/news"

def lambda_handler(event, context):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article')

    result = []
    for article in articles:
        title = article.find('h3').get_text(strip=True)
        link = article.find('a')['href']
        img = article.find('img').attrs['src']

        result.append({
            'id': str(hash(title)),  # タイトルからハッシュを生成してIDとして使用
            'title': title,
            'image': img,
            'link': f"https://www.goal.com{link}"
        })

        # DynamoDBに保存
        # table.put_item(Item={
        #     'id': str(hash(title)),  # タイトルからハッシュを生成してIDとして使用
        #     'title': title,
        #     'image': img,
        #     'link': f"https://www.goal.com{link}",
        #     'lang': 'en',
        #     'timestamp': datetime.now().isoformat()
        # })

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
