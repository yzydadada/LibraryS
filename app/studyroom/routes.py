from flask import render_template, redirect, url_for, current_app,request
from flask_login import current_user, login_required
from flask_babel import _, get_locale

from app import db
from app.book.forms import addbookForm
from app.models import User, Post, Books, Studyrooms,seats
from app.studyroom import bp
from app.studyroom.forms import addroomForm, addseatForm


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

# @bp.route('/control/<roomname>/', methods=['POST','GET'])
# @login_required
# def control(roomname): # 获取url中的变量
#     '''
#     <id>:id是什么内容，下面可直接用
#     '''
#     return roomname,redirect(url_for('studyroom.addseat'))

@bp.route('/addseat/<roomname>/' ,methods=['GET', 'POST'])
@login_required
def addseat(roomname):
    id=Studyrooms.query.filter_by(roomname=roomname).first()
    form = addseatForm()
    if form.validate_on_submit():
        post = seats(seatid=form.seatid.data,state=0,thein=id)
        db.session.add(post)
        db.session.commit()
    return render_template('studyroom/rooms.html', title=_('AddSEATS'), form=form)

@bp.route('/seatS/<roomname>/',methods=['GET', 'POST'])
@login_required
def seatS(roomname):
    id=Studyrooms.query.filter_by(roomname=roomname).first()
    posts = seats.query.filter_by(room_id=id.id)
    return render_template('studyroom/seats.html', title=_('SEATS'),posts=posts)

@bp.route('/delseat/<id>')
@login_required
def delseat(id):


    res = seats.query.filter_by(id=id).first()
    # res = db.session.query(WtMenu).filter(WtMenu.menuid.in_(menuids)).delete(synchronize_session=False)
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('studyroom.rooms'))

@bp.route('/upstate/<id>')
@login_required
def upstate(id):
    seat=seats.query.filter_by(id=id).first()
    if seat.state <3:
        seats.query.filter(seats.id == id).update({'state': seats.state + 1,'user_id':current_user.id})
        db.session.commit()
    else:
        seats.query.filter(seats.id == id).update({'state':0,'user_id':current_user.id})
        db.session.commit()

    return redirect(url_for('studyroom.rooms'))