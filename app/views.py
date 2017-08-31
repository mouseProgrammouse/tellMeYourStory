from app import app, bcrypt, db, login_manager
from forms import LoginForm, RegistrationForm, CreatePost
from flask import flash, g, redirect, render_template, request, session, url_for 
from flask.ext.login import current_user, login_required, login_user, logout_user
from models import Posts, User
from werkzeug.utils import secure_filename
import calendar, os, time


@app.login_manager.user_loader
def user_loader(id):
    """Given *id*, return the associated User object."""
    return User.query.filter_by(id=id).first()


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@login_required
def index():
    """ Start page """
    user = { 'name':g.user.name,
        'surname':g.user.surname}
    posts = Posts.query.filter_by(user_id=g.user.get_id())
    return render_template('index.html',
        title='test',
        user=user,
        folder=os.path.join('/static/uploads/', str(g.user.get_id())),
        posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ If the user is already logged in """
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        """ Try to find user in DB """
        user = User.query.filter_by(login=form.login.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                """ Correct user's data """
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for("index"))
            else:
                flash('Username or Password is invalid','error')
                return redirect(url_for('login'))
        else:
            """ Create error message"""
            flash('Username is invalid','error')
            return redirect(url_for('login'))
    return render_template('login.html',
        title='sign in',
        form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """ Logout the current user. """
    logout_user()
    return redirect(url_for("login"))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if g.user is not None and g.user.is_authenticated():
        flash('Please Log out before registration')
        return redirect(url_for('index'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        """ check is it avaliable login """
        if User.query.filter_by(login=form.login.data).first():
            """ Create error message """
            flash('Choose another login', 'error')
        else:
            """ Add new user to DB """
            new_user = User(login=form.login.data, 
                password=bcrypt.generate_password_hash(form.password.data),
                name=form.name.data,
                surname=form.surname.data)
            db.session.add(new_user)
            db.session.commit()
            """ Success message """
            flash('Done')
            return redirect(url_for("login"))
    return render_template('registration.html',
        title='Registration',
        form=form)


@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def add_post():
    form = CreatePost()
    if request.method == 'POST' and form.validate_on_submit():
        """ Get image info """
        if (form.image.data):
            image = form.image.data
            """ Create new file name """
            old_filename, extension = os.path.splitext(image.filename)
            filename = str(int(calendar.timegm(time.gmtime()))) + extension
            """ Check directory """
            directory = os.path.join(app.config['UPLOAD_FOLDER'], str(g.user.get_id()))
            if not os.path.exists(directory):
                os.makedirs(directory)
            """ Save image """
            image.save(os.path.join(directory, filename))
        else:
            filename = None
        """ Add post to DB """
        new_post = Posts(user_id=g.user.get_id(),
            title=form.title.data,
            text=form.text.data,
            pub_date=form.date.data,
            img=filename,
            public=form.public.data)
        db.session.add(new_post)
        db.session.commit()
        """ Success message """
        flash('Done')
        return (redirect(url_for("index")))
    return render_template('addpost.html',
        title='Create new post',
        form=form)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_post():
    form = CreatePost()
    if request.method == 'POST':
        post = Posts.query.filter_by(id=request.args['id']).first()
        """ UPDATE DATA """
        post.title = form.title.data
        post.text = form.text.data
        post.pub_date = form.date.data
        """ Get image info """
        if (form.image.data):
            image = form.image.data
            """ Create new file name """
            old_filename, extension = os.path.splitext(image.filename)
            filename = str(int(calendar.timegm(time.gmtime()))) + extension
            """ Check directory """
            directory = os.path.join(app.config['UPLOAD_FOLDER'], str(g.user.get_id()))
            if not os.path.exists(directory):
                os.makedirs(directory)
            """ Save image """
            image.save(os.path.join(directory, filename))
            """ add new imagename """
            post.img = filename
        post.public = form.public.data
        """ UPDATE DATA IN DB """
        db.session.commit()
        """ Succes message """
        flash('Done')
        return (redirect(url_for("index")))
    elif request.method == 'GET':
        """ Get info for post """
        post = Posts.query.filter_by(id=request.args['id']).first()
        if post is not None and post.user_id == g.user.get_id():
            return render_template('edit.html',
                    post=post,
                    title='Update post',
                    form=form)
    flash('Something is wrong')
    return redirect(url_for("index"))


@app.route('/delete', methods=['GET'])
@login_required
def delete_post():
    if request.method == 'GET':
        post = Posts.query.filter_by(id=request.args['id']).first()
        if post is not None and post.user_id == g.user.get_id():
            db.session.delete(post)
            db.session.commit()
            """ Success message """
            flash("Post was deleted")
            return (redirect(url_for("index")))
    flash('Something is wrong')
    return (redirect(url_for("index")))


@app.route('/share')
@login_required
def share():
    return render_template('share.html',
        title='Share story',
        id=g.user.get_id())


@app.route('/story', methods=['GET'])
def get_story():
    user_info = User.query.filter_by(id=request.args['id']).first()
    user = { 'name':user_info.name,
        'surname':user_info.surname}
    posts = Posts.query.filter((Posts.public).is_(1) & (Posts.user_id==request.args['id']))
    return render_template('story.html',
        title='',
        user=user,
        folder=os.path.join('/static/uploads/', str(request.args['id'])),
        posts=posts)
