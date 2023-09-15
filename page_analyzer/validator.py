import re
def validate(url):
    errors = {}
    patern = r"(http(|s)://)(|www.)([a-zA-Z0-9-]+)\.(com|ru|org)"
    if url == '':
        errors['url'] = 'URL обязателен'
    elif re.findall(patern, url) == []:
        errors['url'] = 'Некорректный URL'
    return errors