from flask import render_template, request, jsonify, redirect, url_for
from sqlalchemy import desc
from . import app, db
from .models import Category, Item, Record
from .forms import AddForm


@app.route('/', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        with app.app_context():
            c = Category.query.filter_by(name=form.category.data).first()
            if c is None:
                c = Category(form.category.data)
                db.session.add(c)
            i = Item.query.filter_by(name=form.item.data).first()
            if i is None:
                i = Item(form.item.data, c)
                db.session.add(i)
            r = Record(i, '', form.start.data)
            db.session.add(r)
            db.session.commit()

            return redirect(url_for('add'))
    message = 'error' if request.method == 'POST' else ''
    return render_template('add.html', form=form, message=message)


@app.route('/categories')
def get_categories():
    q = request.args.get('q') or ''
    with app.app_context():
        categories = Category.query.filter(Category.name.contains(q)).all()
        return jsonify(matching_results=[c.name for c in categories])


@app.route('/items')
def get_items():
    q = request.args.get('q') or ''
    with app.app_context():
        items = Item.query.filter(Item.name.contains(q)).all()
        return jsonify(matching_results=[i.name for i in items])


@app.route('/show')
@app.route('/show/<category>')
def show(category=None):
    with app.app_context():
        if category is not None:
            c = Category.query.filter_by(name=category).first()
            if c is None:
                return render_template('404.html'), 404
            items = c.items
            records = [item.records for item in items]
            records = [record for sublist in records for record in sublist]
        else:
            records = Record.query.order_by(desc(Record.start_date)).all()

        return render_template('show.html', records=records)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
