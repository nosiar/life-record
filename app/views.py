from flask import render_template, request, jsonify, redirect, url_for
from sqlalchemy import desc
from datetime import datetime, timedelta
from . import app, db
from .models import Category, Item, Record
from .forms import AddForm, ActForm


@app.route('/')
def index():
    return add()


@app.route('/add', methods=['GET', 'POST'])
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


def get_name(choices, value):
    idx = [x[0] for x in choices].index(value)
    return choices[idx][1]


def get_value(choices, name):
    idx = [x[1] for x in choices].index(name)
    return choices[idx][0]


@app.route('/act', methods=['GET', 'POST'])
def act():
    form = ActForm()

    names = [c[1] for c in form.category.choices]
    r = (
        Record.query.order_by(desc(Record.start_date)).join(Item)
        .filter(Item.name.in_(names)).first()
    )
    if r is not None and r.end_date is None:
        running = get_value(form.category.choices, r.item.name)
        start_date = r.start_date
    else:
        running = ''
        start_date = None

    if act_form_validate(form, running, request):
        if running != '':
            r.end_date = datetime.now()
        else:
            name = get_name(form.category.choices, form.category.data)

            c = Category.query.filter_by(name=name).first()
            if c is None:
                c = Category(name)
                db.session.add(c)
            i = Item.query.filter_by(name=name).first()
            if i is None:
                i = Item(name, c)
                db.session.add(i)
            r = Record(i, '', datetime.now())
            db.session.add(r)
        db.session.commit()
        return redirect(url_for('act'))
    return render_template('act.html', form=form,
                           running=running, start_date=start_date)


@app.route('/json/categories')
def get_categories():
    q = request.args.get('q') or ''
    categories = Category.query.filter(Category.name.contains(q)).all()
    return jsonify(matching_results=[c.name for c in categories])


@app.route('/json/items')
def get_items():
    q = request.args.get('q') or ''
    items = Item.query.filter(Item.name.contains(q)).all()
    return jsonify(matching_results=[i.name for i in items])


@app.route('/all')
@app.route('/i/<item>')
@app.route('/c/<category>')
@app.route('/d/<date>')
def show(item=None, category=None, date=None):
    if category is not None:
        c = Category.query.filter_by(name=category).first()
        if c is None:
            return render_template('404.html'), 404
        records = (
            Record.query.order_by(desc(Record.start_date)).join(Item)
            .filter(Item.category_id == c.id).all()
        )
    elif item is not None:
        i = Item.query.filter_by(name=item).first()
        if i is None:
            return render_template('404.html'), 404
        records = (
            Record.query.order_by(desc(Record.start_date))
            .filter_by(item_id=i.id).all()
        )
    elif date is not None:
        s = datetime.strptime(date, '%Y-%m-%d')
        e = s + timedelta(days=1)
        records = (
            Record.query.order_by(desc(Record.start_date))
            .filter(Record.start_date.between(s, e)).all()
        )
    else:
        records = Record.query.order_by(desc(Record.start_date)).all()

    return render_template('show.html', records=records)


@app.route('/delete/<id>')
def delete(id):
    redirect_to = request.referrer or url_for('index')

    try:
        id = int(id)
    except ValueError:
        return redirect(redirect_to)

    r = Record.query.get(id)
    if r is not None:
        i = r.item
        db.session.delete(r)

        if not i.records.all():
            c = i.category
            db.session.delete(i)

            if not c.items.all():
                db.session.delete(c)

        db.session.commit()

    return redirect(redirect_to)


@app.route('/category')
def category():
    categories = Category.query.all()
    return render_template('category.html', categories=categories)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
