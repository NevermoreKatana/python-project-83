import requests
from bs4 import BeautifulSoup


def check_url(url):
    result = {
        'errors': {},
        'status_code': None,
        'h1': '',
        'title': '',
        'description': '',
    }

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        result['errors']['danger'] = 'Произошла ошибка при проверке'
    else:
        result['status_code'] = response.status_code
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            result['title'] = title_tag.text
        h1_tag = soup.find('h1')
        if h1_tag:
            result['h1'] = h1_tag.text
        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description:
            result['description'] = meta_description['content']

    return result
