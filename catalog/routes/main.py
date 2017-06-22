from catalog import app
from flask import render_template


@app.route('/')
@app.route('/catalog')
def index():
    return render_template('index.html', categories=service().all())


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


def service():
    from catalog.services.category_service import CategoryService
    return CategoryService()
