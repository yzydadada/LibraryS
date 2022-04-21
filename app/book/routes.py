from PIL import ImageFile
from flask import render_template, redirect, url_for, current_app,request,flash
from flask_login import current_user, login_required
from flask_babel import _, get_locale
import sys
from app import db
from app.book.forms import addbookForm,BooksSearchForm
from app.models import User, Post, Books, borrowing
from app.book import bp
from config import basedir


@bp.route('/books' ,methods=['GET', 'POST'])
@login_required
def books():
    form=addbookForm()
    if request.method == 'POST' and form.validate_on_submit():
        bookimage = request.files.get('image')
        file_name = form.bookname.data
        path = basedir+"/app/static/photo/"
        file_path = path+bookimage.filename
        file="/static/photo/"+bookimage.filename
        bookimage.save(file_path)
        book = Books(bookname=form.bookname.data,image_name=file_name, bookimage=file)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('book.books'))
    page = request.args.get('page', 1, type=int)
    posts = Books.query.order_by(Books.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('book.books', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('book.books', page=posts.prev_num) if posts.has_prev else None
    return render_template('book/books.html', title=_('Books'),form=form,posts=posts.items, next_url=next_url,prev_url=prev_url)

@bp.route('/delbook/<id>')
@login_required
def delbook(id):

    res = Books.query.filter_by(id=id).first()
    # res = db.session.query(WtMenu).filter(WtMenu.menuid.in_(menuids)).delete(synchronize_session=False)
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('book.books'))

@bp.route('/Searchbooks' ,methods=['GET', 'POST'])
@login_required
def Searchbooks():

    post=request.form.get('post')
    posts = Books.query.filter(Books.bookname.like("%" + post + "%") if post is not None else "").all()
    return render_template('book/books.html', title=_(str(post)),posts=posts)

@bp.route('/outbook/<id>')
@login_required
def outbook(id):
    sys.path.append('C:/Users/YZY/PycharmProjects/LibraryS/facenet-retinaface-pytorch-main')
    user = User.query.filter_by(id=current_user.id).first()
    from predict import facex
    tf = facex(user.userid)
    if tf == 1:
        res = borrowing(user_id=current_user.id, book_id=id)
        db.session.add(res)
        db.session.commit()
        flash('out ok')
    else:
        flash('face F')


    return redirect(url_for('book.books'))

@bp.route('/inbook/<id>')
@login_required
def inbook(id):
    sys.path.append('C:/Users/YZY/PycharmProjects/LibraryS/facenet-retinaface-pytorch-main')
    user = User.query.filter_by(id=current_user.id).first()
    from predict import facex
    tf = facex(user.userid)
    if tf == 1:
        res = borrowing.query.filter_by(id=id).first()
        db.session.delete(res)
        db.session.commit()
        flash('back ok')
    else:
        flash('face F')
    return redirect(url_for('book.borrowingS'))

@bp.route('/userinbook')
@login_required
def userinbook():
    sys.path.append('C:/Users/YZY/PycharmProjects/LibraryS/facenet-retinaface-pytorch-main')
    from predict import facex
    tf = facex(current_user.userid)
    if tf == 1:
        res = borrowing.query.filter_by(user_id=current_user.id).first()
        db.session.delete(res)
        db.session.commit()
        flash('back ok')
    else:
        flash('face F')
    return redirect(url_for('book.borrowingS'))

@bp.route('/borrowingS')
@login_required
def borrowingS():

    posts = borrowing.query.all()

    return render_template('book/borrowingS.html', title=_('borrowing'),posts=posts)