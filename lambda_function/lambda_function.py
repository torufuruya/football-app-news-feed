import json
import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime

# DynamoDBのセットアップ
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('news')

# Goal.com ニュースページのURL
URL_en = "https://www.goal.com/en/news"
URL_es = "https://www.goal.com/es/noticias"
URL_jp = "https://www.goal.com/jp/%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9"

def lambda_handler(event, context):
    query_params = event.get('queryStringParameters', {})
    lang = query_params.get('lang')

    source = URL_en
    if lang == 'es':
        source = URL_es
    elif lang == 'ja':
        source = URL_jp

    response = requests.get(source)
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
            'link': f"https://www.goal.com{link}",
            'source': 'goal.com'
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
