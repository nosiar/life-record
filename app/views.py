from flask import render_template, request, jsonify, redirect, url_for
from sqlalchemy import desc
from datetime import datetime
from . import app, db
from .models import Category, Item, Record
from .forms import AddForm, ActForm


@app.route('/', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
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
    return render_template('add.html', form=form)


def act_form_validate(form, running, request):
    if form.validate_on_submit():
        submit = request.form['submit']
        return ((submit == 'start' and running == '')
                or (submit == 'end' and running == form.category.data))
    return False


@app.route('/act', methods=['GET', 'POST'])
def act():
    form = ActForm()

    choices = [c[0] for c in form.category.choices]
    r = (
        Record.query.order_by(desc(Record.start_date)).join(Item)
        .filter(Item.name.in_(choices)).first()
    )
    if r is not None and r.end_date is None:
        running = r.item.name
        start_date = r.start_date
    else:
        running = ''
        start_date = None

    if act_form_validate(form, running, request):
        if running != '':
            r.end_date = datetime.now()
        else:
            c = Category.query.filter_by(name=form.category.data).first()
            if c is None:
                c = Category(form.category.data)
                db.session.add(c)
            i = Item.query.filter_by(name=form.category.data).first()
            if i is None:
                i = Item(form.category.data, c)
                db.session.add(i)
            r = Record(i, '', datetime.now())
            db.session.add(r)
        db.session.commit()
        return redirect(url_for('act'))
    return render_template('act.html', form=form,
                           running=running, start_date=start_date)


@app.route('/categories')
def get_categories():
    q = request.args.get('q') or ''
    categories = Category.query.filter(Category.name.contains(q)).all()
    return jsonify(matching_results=[c.name for c in categories])


@app.route('/items')
def get_items():
    q = request.args.get('q') or ''
    items = Item.query.filter(Item.name.contains(q)).all()
    return jsonify(matching_results=[i.name for i in items])


@app.route('/show')
@app.route('/show/<category>')
def show(category=None):
    if category is not None:
        c = Category.query.filter_by(name=category).first()
        if c is None:
            return render_template('404.html'), 404
        records = (
            Record.query.order_by(desc(Record.start_date)).join(Item)
            .filter(Item.category_id == c.id).all()
        )
    else:
        records = Record.query.order_by(desc(Record.start_date)).all()

    return render_template('show.html', records=records)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
