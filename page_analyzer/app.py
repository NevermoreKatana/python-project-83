from flask import Flask, render_template, request, flash, redirect
from page_analyzer.validator import validate
import os, dotenv, logging
from page_analyzer.database import add_new_url, take_url_id, take_url_info, take_all_entity
dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.logger.setLevel(logging.DEBUG)

@app.route('/', methods=['GET'])
def index():
    errors = {}
    url =''
    return render_template('index.html', errors=errors, url=url)


@app.route('/urls', methods=['POST'])
def urls():
    url = request.form.get('url')
    errors = validate(url)
    if errors:
        return render_template('index.html', errors=errors, url=url), 422
    add_new_url(url)
    id = take_url_id(url)
    return redirect(f'/urls/{id}')

@app.route('/urls/<id>')
def show_one_url(id):
    info_about_url = take_url_info(id)
    return render_template('/urls/one.html', url = info_about_url)


@app.route('/urls', methods=['GET'])
def show_urls():
    entities = take_all_entity()
    return render_template('/urls/all_urls.html', entities = entities)

