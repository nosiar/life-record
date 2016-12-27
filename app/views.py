from flask import render_template, request, jsonify
from . import app
from .models import Category


@app.route('/')
def add():
    return render_template('add.html')


@app.route('/categories')
def get_categories():
    q = request.args.get('q') or ''
    with app.app_context():
        categories = Category.query.filter(Category.name.contains(q)).all()
        return jsonify(matching_results=[c.name for c in categories])


@app.route('/all/')
def show_all():
    with app.app_context():
        eat = Category.query.filter_by(name='처먹').first()
        items = eat.items
        records = [item.records for item in items]
        records = [record for sublist in records for record in sublist]

        return render_template('show.html', records=records)


@app.route('/<name>')
def hello_name(name):
    return render_template('hello.html', name=name)
