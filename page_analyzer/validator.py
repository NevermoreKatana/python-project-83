import validators


def validate(url):
    errors = {}
    if url == '':
        errors['url'] = 'URL обязателен'
    elif not validators.url(url):
        errors['url'] = 'Некорректный URL'
    elif len(url) > 255:
        errors['url'] = 'URL превышает 255 символов'
    return errors
