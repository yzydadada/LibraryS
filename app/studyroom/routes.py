from flask import render_template, redirect, url_for, current_app,request
from flask_login import current_user, login_required
from flask_babel import _, get_locale

from app import db
from app.book.forms import addbookForm
from app.models import User, Post, Books, Studyrooms
from app.studyroom import bp
from app.studyroom.forms import addroomForm


@bp.route('/rooms' ,methods=['GET', 'POST'])
@login_required
def rooms():

    form=addroomForm()
    if form.validate_on_submit():
        room = Studyrooms(roomname=form.roomname.data)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('studyroom.rooms'))
    page = request.args.get('page', 1, type=int)
    posts = Studyrooms.query.order_by(Studyrooms.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('studyroom.rooms', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('studyroom.rooms', page=posts.prev_num) if posts.has_prev else None
    return render_template('studyroom/rooms.html', title=_('Rooms'),form=form,posts=posts.items, next_url=next_url,prev_url=prev_url)