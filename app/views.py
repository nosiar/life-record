from flask import render_template
from . import app
from .models import Category


@app.route('/')
def show_all():
    with app.app_context():
        eat = Category.query.filter_by(name='처먹').first()
        items = eat.items.all()
        records = [item.records.all() for item in items]
        records = [record for sublist in records for record in sublist]

        return render_template('show.html', records=records)


@app.route('/<name>')
def hello_name(name):
    return render_template('hello.html', name=name)


if __name__ == "__main__":
    app.run()
