from flask import Flask, render_template, request, flash, redirect
from page_analyzer.validator import validate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VANYA LOVE'

@app.route('/', methods=['GET'])
def index():
    errors = {}
    return render_template('index.html', errors=errors)


@app.route('/urls', methods=['POST'])
def urls():
    url = request.form.get('url')
    errors = validate(url)
    if len(errors) > 0:
        flash('asdas')
        return render_template('index.html', errors=errors), 422
    return f'jopa suka blya == {errors}'