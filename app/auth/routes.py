import sys

from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, seats
from app.auth.email import send_password_reset_email
import os
import cv2

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(userid=form.userid.data,username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'),
                           form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@bp.route('/Change_password', methods=['GET', 'POST'])
def Change_password():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)
@bp.route('/getface/<userid>', methods=['GET', 'POST'])
def getface(userid):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    flag = cap.isOpened()
    index = 1
    id=userid
    while (flag):
        ret, frame = cap.read()
        cv2.imshow("Capture_Paizhao", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('s'):  # 按下s键，进入下面的保存图片操作
            cv2.imwrite("facenet-retinaface-pytorch-main/face_dataset/"+id +"_"+ str(index) + ".jpg", frame)
            user= User.query.filter_by(userid=id).first()
            user.facedata="facenet-retinaface-pytorch-main/face_dataset/"+id +"_"+ str(index) + ".jpg"
            db.session.commit()
            print("save" +id +"_"+ str(index) + ".jpg successfuly!")
            index += 1
            break
    cap.release() # 释放摄像头
    cv2.destroyAllWindows()# 释放并销毁窗口
    os.system('python facenet-retinaface-pytorch-main/encoding.py')
    return render_template('index.html')

@bp.route('/face/<userid>', methods=['GET', 'POST'])
def face(userid):

    sys.path.append('C:/Users/YZY/PycharmProjects/LibraryS/facenet-retinaface-pytorch-main')

    from predict import facex
    tf=facex(userid)
    user = User.query.filter_by(userid=userid).first()
    if tf==1:
        seats.query.filter(seats.user_id == user.id).update({'state': seats.state + 1})
        db.session.commit()
    else:
        flash('face F')
    return render_template('index.html')
