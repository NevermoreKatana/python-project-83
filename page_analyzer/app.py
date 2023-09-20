import os
import dotenv
from flask import Flask, render_template, request, flash, redirect
from urllib.parse import urlparse
from page_analyzer.validator import validate
from page_analyzer.checker import check_url
from page_analyzer.database import (add_new_url,
                                    take_url_id,
                                    take_url_info,
                                    take_all_entity,
                                    add_new_check,
                                    take_url_checks_info,
                                    availability_check_url)
dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def index():
    url = ''
    return render_template('index.html', url=url)


@app.route('/urls', methods=['POST'])
def urls():
    url_status = {}
    url = request.form.get('url')
    errors = validate(url)
    if errors:
        flash(errors['url'])
        return render_template('index.html', url=url), 422
    parse = urlparse(url)
    url = parse.scheme + '://' + parse.netloc
    if availability_check_url(url):
        url_status['added'] = 'Страница успешно добавлена'
        add_new_url(url)
        flash(url_status)
    url_status['exists'] = 'Страница уже существует'
    flash(url_status)
    id = take_url_id(url)
    return redirect(f'/urls/{id}')


@app.route('/urls/<id>', methods=['GET'])
def show_one_url(id):
    info_about_url = take_url_info(id)
    checks_info = take_url_checks_info(id)
    return render_template('/urls/one.html',
                           url=info_about_url,
                           checks_info=checks_info)


@app.route('/urls/<id>/checks', methods=['POST'])
def urls_id_checks(id):
    url = take_url_info(id)[0][1]
    result = check_url(url)

    errors = result['errors']
    status_code = result['status_code']
    h1 = result['h1']
    title = result['title']
    description = result['description']

    if errors:
        flash(errors)
        return redirect(f'/urls/{id}')

    add_new_check(id, status_code, h1, title, description)
    flash('Страница успешно проверена')
    return redirect(f'/urls/{id}')


@app.route('/urls', methods=['GET'])
def show_urls():
    info = take_all_entity()
    return render_template('/urls/all_urls.html', info=info)
