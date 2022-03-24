from flask import render_template, redirect, url_for, current_app,request
from flask_login import current_user, login_required
from flask_babel import _, get_locale

from app import db
from app.book.forms import addbookForm
from app.models import User, Post, Books
from app.book import bp




@bp.route('/books' ,methods=['GET', 'POST'])
@login_required
def books():

    form=addbookForm()
    if form.validate_on_submit():
        book = Books(bookname=form.bookname.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('book.books'))
    page = request.args.get('page', 1, type=int)
    posts = Books.query.order_by(Books.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('book.books', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('book.books', page=posts.prev_num) if posts.has_prev else None
    return render_template('book/books.html', title=_('Books'),form=form,posts=posts.items, next_url=next_url,prev_url=prev_url)