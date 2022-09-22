import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

newsapi = "b54ba07ecb6946fe971f9230816b79e1"
aplha_vantage_api = "X08GD9MRWJBCU0DG"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_SID = 'ACfbaf31b41bd88ee560fd2df3374c1653'
TWILIO_AUTH_TOKEN = '161aa0eb9a984ca58cb882178a150674'


url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+STOCK_NAME+'&outputsize=compact&apikey='+aplha_vantage_api
r = requests.get(url)
data = r.json()['Time Series (Daily)']
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']


day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']


positive_difference = round(abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price)))


percentage_difference = positive_difference/float(yesterday_closing_price)*100
print(round(percentage_difference,2))


if percentage_difference > 1:
    news_params = {
        'apiKey':newsapi,
        "qInTitle":COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]

    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
    print(client)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+12184131214",
            to="+918800662702"
        )