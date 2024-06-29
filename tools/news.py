import pytz
import requests
import json
import time
from datetime import datetime, timedelta
from dateutil import parser


COMPANY_LIST = ['ABB', 'ABM', 'Raiffeisen', 'Siemens', 'UBS']


def _req(company, from_index, batch_size):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer X',
    }

    payload = {
        "type": "filterArticles",
        "isPublic": False,
        "queryString": f'title:"{company}" OR description:"{company}"',
        "from": from_index,
        "size": batch_size,
        "sort": {"publishedAt": {"order": "desc"}},
    }
    response = requests.post(
        'https://api.newsfilter.io/actions', headers=headers, data=json.dumps(payload)
    )
    return response.json()


def get_news(company):
    end_date = datetime.utcnow().replace(tzinfo=pytz.UTC)
    start_date = end_date - timedelta(days=180)

    articles = []
    from_index = 0
    batch_size = 50
    more_articles = True

    while more_articles:
        response_data = _req(company, from_index, batch_size)
        time.sleep(1)
        if 'articles' in response_data:
            for article in response_data['articles']:
                # Parse the publication date of the article
                published_at = parser.parse(article['publishedAt'])
                if published_at >= start_date:
                    articles.append(article)
                else:
                    more_articles = False
                    break

            from_index += batch_size
        else:
            more_articles = False

    with open(f"articles/{company}.json", "w") as final:
        json.dump(articles, final)


get_news(company='IBM')
# gather_news_with_company_name = get_news
