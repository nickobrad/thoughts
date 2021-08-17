import os
from flask.helpers import flash
from config import Config, DevConfig
from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from . import main
from ..models import User, Pitch, PitchComment,Category
from .forms import PitchForm, CommentForm
from .. import db, photos

@main.route('/home')
@login_required
def home():
    title = "Welcome to Cactus"

    love = Pitch.query.filter_by(categoryOfPitch = 1).all()
    work = Pitch.query.filter_by(categoryOfPitch = 2).all()
    hate = Pitch.query.filter_by(categoryOfPitch = 3).all()

    return render_template('index.html', love = love, work = work, hate = hate, title = title)

@main.route('/post/pitch', methods = ['GET', 'POST'])
@login_required
def post_pitch():
    title = "Post a pitch"
    if request.form:
        pitch = request.form['pitch']
        category = request.form['category']

        if pitch != "" or category != "":
            cat = category.lower()
            if cat == 'love':
                pitch = Pitch(pitch = pitch, categoryOfPitch = 1, user = current_user.username)
                pitch.save_pitch()
                return redirect(url_for('main.home'))
            elif cat == 'work':
                pitch = Pitch(pitch = pitch, categoryOfPitch = 2, user = current_user.username)
                pitch.save_pitch()
                return redirect(url_for('main.home'))
            elif cat == 'displeasure':
                pitch = Pitch(pitch = pitch, categoryOfPitch = 3, user = current_user.username)
                pitch.save_pitch()
                return redirect(url_for('main.home'))
            else:
                flash("Please type in a proper category")

    return render_template('new_pitch.html', title = title)

@main.route('/post/pitch/category/<int:id>', methods = ['GET', 'POST'])
def category(id):

    pitches = Pitch.query.filter_by(id = id).all()
    
    if id == 1:
        title = "Love"
    elif id == 2:
        title = "Work"
    elif id == 3:
        title = "Displeasure"
    return render_template('category.html', categ = pitches, title = title)

@main.route('/post/pitch/<id>/comments', methods = ['GET', 'POST'])
def make_comment(id):

    comment_form = CommentForm()
    pitch = Pitch.query.filter_by(id = id).first()
    comments = PitchComment.query.filter_by(pitch_id = id).all()

    title = f'Comment on pitch {pitch.id}'

    if request.form:
        comment = request.form['comment']
        if comment != "":
            new_comment = PitchComment(pitch_id = pitch.id, comment = comment, user = current_user.username)
            new_comment.save_comment()
            return redirect(url_for('main.show_comments', id = pitch.id))

    return render_template('comments.html', pitch = pitch, comments = comments, title = title)

@main.route('/post/pitch/<id>/comments')
def show_comments(id):

    comments = PitchComment.query.filter_by(pitch_id = id).all()
    pitch = Pitch.query.filter_by(id = id).first()

    title = f'Comments on Pitch {pitch.id}'

    return render_template('comments.html', pitch = pitch, comments = comments, title = title)

@main.route('/post/pitch/<id>/comments',methods = ['GET','POST'])
def plus(id):

    comments = PitchComment.query.filter_by(pitch_id = id).all()
    pitch = Pitch.query.filter_by(id = id).first()
    title = f'Comments on Pitch {pitch.id}'

    if request.form:
        if request.form['like'] == "upvote":
            print(request.form['like'])
            if pitch.upvote == 0:
                pitch.upvote = 1
                db.session.add(pitch)
                db.session.commit()
            return redirect(url_for('main.show_comments', id = pitch.id))
        elif pitch.upvote > 0:
            pitch.upvote = pitch.upvote + 1
            db.session.add(pitch)
            db.session.commit()
            return redirect(url_for('main.show_comments', id = pitch.id))
    
    return redirect(url_for('main.show_comments', comments = comments, pitch = pitch, id = pitch.id))

@main.route('/post/pitch/<id>/comments')
def minus(id):

    pitch = Pitch.query.filter_by(id = id).first()
    title = f'Comments on Pitch {pitch.id}'

    if pitch.downvote == 0:
        pitch.downvote = 1
        db.session.add(pitch)
        db.session.commit()
        return redirect(url_for('main.show_comments', id = pitch.id))
    elif pitch.downvote > 0:
        pitch.downvote = pitch.upvote + 1
        db.session.add(pitch)
        db.session.commit()
        return redirect(url_for('main.show_comments', id = pitch.id))
    
    return redirect(url_for('main.show_comments', id = pitch.id))

@main.route('/user/profile/<userss>', methods = ['GET', 'POST'])
def profile(userss):

    user = User.query.filter_by(username = userss).first()
    title = f'{user.username}\'s Profile'

    if user is None:
        abort(404) 

    mypitches = Pitch.query.filter_by(user = userss).all()
    mycomments = PitchComment.query.filter_by(user = userss).all()

    return render_template('profile/profile.html', mypitches = mypitches, mycomments = mycomments, title = title, user = user)

@main.route('/user/profile/update/<userss>', methods = ['GET', 'POST']) 
def gotoupdate(userss):
    user = User.query.filter_by(username = userss).first()
    title = f'Update {user.username}\'s Profile'

    if user is None:
        abort(404)

    return render_template('/profile/update_profile.html', user = user, title = title)

@main.route('/user/profile/update', methods = ['GET', 'POST'])
def update_profile():
    user = User.query.filter_by(username = current_user.username).first()

    if user is None:
        abort(404)

    if request.form:
        bio = request.form['bio']
        if bio != "":
            user.profile_bio = bio
            db.session.add(user)
            db.session.commit()
    
    if request.files:
            if request.files['photo'] != "":
                filename = photos.save(request.files['photo'])
                path = f'profile_photos/{filename}'
                user.profile_picture = path
                db.session.add(user)
                db.session.commit()
            else:
                return redirect(url_for('main.profile', userss = user.username))

            
    return redirect(url_for('main.profile', userss = user.username))

    





        
