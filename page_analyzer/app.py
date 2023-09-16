from flask import Flask, render_template, request, flash, redirect
from page_analyzer.validator import validate
import os, dotenv, requests
from page_analyzer.database import add_new_url, take_url_id, take_url_info, take_all_entity, add_new_check, take_url_checks_info
from urllib.parse import urlparse
from bs4 import BeautifulSoup
dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def index():
    errors = {}
    url =''
    return render_template('index.html', errors=errors, url=url)


@app.route('/urls', methods=['POST'])
def urls():
    url = request.form.get('url')
    parse = urlparse(url)
    url = parse.scheme + '://' + parse.netloc
    errors = validate(url)
    if errors:
        return render_template('index.html', errors=errors, url=url), 422
    add_new_url(url)
    id = take_url_id(url)
    return redirect(f'/urls/{id}')

@app.route('/urls/<id>', methods=['GET'])
def show_one_url(id):
    info_about_url = take_url_info(id)
    checks_info = take_url_checks_info(id)
    return render_template('/urls/one.html', url = info_about_url, checks_info=checks_info)


@app.route('/urls/<id>/checks', methods=['POST'])
def urls_id_checks(id):
    add_new_check(id)
    return redirect(f'/urls/{id}')


@app.route('/urls', methods=['GET'])
def show_urls():
    info = take_all_entity()
    return render_template('/urls/all_urls.html', info=info)

