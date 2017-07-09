from flask.ext.wtf import Form
import wtforms


class LoginForm(Form):
    login = wtforms.TextField('login', validators=[wtforms.validators.Required()])
    password = wtforms.PasswordField('password', validators=[wtforms.validators.Required()])
    remember_me = wtforms.BooleanField('remember_me', default=False)


class RegistrationForm(Form):
    name = wtforms.TextField('name', validators=[wtforms.validators.Required()])
    surname =  wtforms.TextField('surname', validators=[wtforms.validators.Required()])
    login =  wtforms.TextField('login', validators=[wtforms.validators.Required(), wtforms.validators.Length(min=4, max=25)])
    password =  wtforms.PasswordField('password', validators=[wtforms.validators.Required(), wtforms.validators.EqualTo('confirm', message='Passwords must match')])
    confirm =  wtforms.PasswordField('repeat password', validators=[wtforms.validators.Required()])
