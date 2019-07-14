import os
import secrets
from PIL import Image
from sqlalchemy import desc
from flask import render_template, url_for, flash, redirect, request, abort
from beforetheproduct import app, db, bcrypt
from beforetheproduct.forms import UserRegistrationForm, LoginForm, UpdateAccountForm, IdeaForm, CommentForm, UpdateIdeaForm
from beforetheproduct.models import User, Idea, IdeaYes, IdeaNo, Upvote, IdeaComment, Topic
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/home")
@app.route("/")
def home():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    else:
        image_file = ''
    new_ideas = Idea.query.order_by(desc(Idea.date_posted)).limit(8).all()
    top_ideas = Idea.query.join(Upvote).order_by(desc(Idea.upvotes)).limit(8).all()
    trending_ideas = Idea.query.order_by(desc(Idea.view_count)).limit(4).all()

    return render_template("index.html", image_file=image_file, new_ideas=new_ideas, top_ideas=top_ideas, trending_ideas=trending_ideas)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, full_name=form.full_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_thumbnail(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/thumbnails', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_main_image(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/main_images', picture_fn)

    output_size = (800, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.headline = form.headline.data
        db.session.commit()
        flash('Your account details has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.headline.data = current_user.headline
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)

@app.route("/idea/new", methods=['GET', 'POST'])
@login_required
def new_idea():
    form = IdeaForm()
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    else:
        image_file = ''
    if form.validate_on_submit():
        idea = Idea(title=form.title.data, link=form.link.data, description=form.description.data, user=current_user, topic=form.topic.data)
        if form.thumbnail_image.data:
            picture_file = save_thumbnail(form.thumbnail_image.data)
            idea.thumbnail = picture_file
        if form.main_image.data:
            picture_file = save_main_image(form.main_image.data)
            idea.main_image = picture_file
        db.session.add(idea)
        db.session.commit()
        flash('Your idea has been added!', 'success')
        return redirect(url_for('idea', idea_id=idea.id))
    return render_template('create_idea.html', form=form, image_file=image_file)

@app.route("/<int:idea_id>/comment/new", methods=['GET', 'POST'])
@login_required
def new_comment(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    form = CommentForm()
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    else:
        image_file = ''
    if form.validate_on_submit():
        comment = IdeaComment(content=form.content.data, user=current_user, idea=idea)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('idea', idea_id=idea_id))
    return render_template('create_comment.html', form=form, image_file=image_file)

@app.route("/idea/<int:idea_id>")
@login_required
def idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    main_image = url_for('static', filename='main_images/' + idea.main_image)
    thumbnail_image = url_for('static', filename='thumbnails/' + idea.thumbnail)
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    else:
        image_file = ''
    if idea.user != current_user:
        idea.view_count += 1
        db.session.commit()

    return render_template('idea.html', title=idea.title, idea=idea, image_file=image_file, main_image=main_image, thumbnail_image=thumbnail_image)

@app.route('/yes/<int:idea_id>/<action>')
@login_required
def yes_action(idea_id, action):
    idea = Idea.query.get_or_404(idea_id)
    if action == 'yes':
        current_user.yes_idea(idea)
        current_user.unno_idea(idea)
        db.session.commit()
    if action == 'unyes':
        current_user.unyes_idea(idea)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/no/<int:idea_id>/<action>')
@login_required
def no_action(idea_id, action):
    idea = Idea.query.get_or_404(idea_id)
    if action == 'no':
        current_user.no_idea(idea)
        current_user.unyes_idea(idea)
        db.session.commit()
    if action == 'unno':
        current_user.unno_idea(idea)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/upvote/<int:idea_id>/<action>')
@login_required
def upvote(idea_id, action):
    idea = Idea.query.get_or_404(idea_id)
    if action == 'upvote':
        current_user.upvote(idea)
        db.session.commit()
    if action == 'unupvote':
        current_user.unupvote(idea)
        db.session.commit()
    return redirect(request.referrer)

@app.route("/idea/<int:idea_id>/update", methods=['GET', 'POST'])
@login_required
def update_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    if idea.user != current_user:
        abort(403)
    form = UpdateIdeaForm()
    if form.validate_on_submit():
        idea.title = form.title.data
        idea.link = form.link.data
        idea.description = form.description.data
        idea.topic = form.topic.data
        if form.thumbnail_image.data:
            picture_file = save_thumbnail(form.thumbnail_image.data)
            idea.thumbnail = picture_file
        if form.main_image.data:
            picture_file = save_main_image(form.main_image.data)
            idea.main_image = picture_file
        db.session.commit()
        flash('Your idea has been updated!', 'success')
        return redirect(url_for('idea', idea_id=idea.id))
    elif request.method == 'GET':
        form.title.data = idea.title
        form.link.data = idea.link
        form.topic.data = idea.topic
        form.description.data = idea.description

        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        main_image = url_for('static', filename='main_images/' + idea.main_image)
        thumbnail_image = url_for('static', filename='thumbnails/' + idea.thumbnail)
        form_description = idea.description
    return render_template('create_idea.html', form=form, form_description=form_description, thumbnail_image=thumbnail_image, main_image=main_image, image_file=image_file)


@app.route("/idea/<int:idea_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    if idea.user != current_user:
        abort(403)
    db.session.delete(idea)
    db.session.commit()
    flash('Your idea has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/comment/<int:comment_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_comment(comment_id):
    comment = IdeaComment.query.get_or_404(comment_id)
    if comment.user != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(request.referrer)
