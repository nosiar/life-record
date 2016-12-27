from flask import render_template, request, jsonify, redirect, url_for
from . import app
from .models import Category
from .forms import AddForm


@app.route('/', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        with app.app_context():
            return redirect(url_for('add'))
    message = 'error' if request.method == 'POST' else ''
    return render_template('add.html', form=form, message=message)


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
