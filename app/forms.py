from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required, Length, EqualTo

class LoginForm(Form):
    login = TextField('login', validators = [Required()])
    password = PasswordField('password',validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class RegistrationForm(Form):
	name = TextField('name', validators = [Required()])
	surname = TextField('surname', validators = [Required()])
	login = TextField('login', validators = [Required(), Length(min=4, max=25)])
	password = PasswordField('password',validators = [Required(), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('repeat password',validators = [Required()])
