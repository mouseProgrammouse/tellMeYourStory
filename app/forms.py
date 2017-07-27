from datetime import datetime, date
from flask.ext.wtf import Form
import flask.ext.wtf.file
import wtforms

class LoginForm(Form):
    login = wtforms.TextField('login', render_kw={'placeholder': 'login'}, validators=[wtforms.validators.Required()])
    password = wtforms.PasswordField('password', render_kw={'placeholder': 'password'}, validators=[wtforms.validators.Required()])
    remember_me = wtforms.BooleanField('remember_me', default=False)


class RegistrationForm(Form):
    name = wtforms.TextField('name', render_kw={'placeholder': 'name'}, validators=[wtforms.validators.Required()])
    surname =  wtforms.TextField('surname', render_kw={'placeholder': 'surname'}, validators=[wtforms.validators.Required()])
    login =  wtforms.TextField('login', render_kw={'placeholder': 'login'}, validators=[wtforms.validators.Required(), wtforms.validators.Length(min=4, max=25)])
    password =  wtforms.PasswordField('password', render_kw={'placeholder': 'password'}, validators=[wtforms.validators.Required(), wtforms.validators.EqualTo('confirm', message='Passwords must match')])
    confirm =  wtforms.PasswordField('repeat password', render_kw={'placeholder': 'repeat password'}, validators=[wtforms.validators.Required(), wtforms.validators.EqualTo('password', message='')])


class CreatePost(Form):
    title = wtforms.TextField(render_kw={'placeholder': 'title'}, validators=[wtforms.validators.Required()])
    text = wtforms.TextAreaField(render_kw={'placeholder': 'write your story'}, validators=[wtforms.validators.Required()])
    date = wtforms.DateTimeField(render_kw={'placeholder': 'format: YYYY-mm-dd HH:MM'}, default=datetime.now, format='%Y-%m-%d %H:%M', validators=[wtforms.validators.Required()])
    image = wtforms.FileField(validators=[flask.ext.wtf.file.FileRequired(), flask.ext.wtf.file.FileAllowed(['png', 'jpg', 'jpeg'], message='Wrong file type')])
