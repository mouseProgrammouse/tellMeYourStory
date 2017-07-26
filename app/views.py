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
    return render_template('index.html',
        title='test',
        user=user)


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
        """ Add post to DB """
        new_post = Posts(user_id=g.user.get_id(),
            title=form.title.data,
            text=form.text.data,
            pub_date=form.date.data,
            img=filename)
        db.session.add(new_post)
        db.session.commit()
        """ Success message """
        flash('Done')
        return (redirect(url_for("index")))
    return render_template('addpost.html',
        title='Create new post',
        form=form)
