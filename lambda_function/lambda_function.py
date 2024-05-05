import json
import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime

# DynamoDBのセットアップ
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('NewsItems')

# Goal.com ニュースページのURL
URL = "https://www.goal.com/jp/%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9"

def lambda_handler(event, context):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article')
    
    for article in articles:
        headline = article.find('h3').get_text(strip=True)
        link = article.find('a')['href']
        img = article.find('img')
        print('-----------------')
        print(headline)
        print(img.attrs['src'])
        print(link)
        print('-----------------')
    
        # DynamoDBに保存
        table.put_item(Item={
            'id': str(hash(title)),  # タイトルからハッシュを生成してIDとして使用
            'title': title,
            'link': f"https://www.goal.com{link}",
            'timestamp': datetime.now().isoformat()
        })

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
