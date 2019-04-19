from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class NewEmployee(FlaskForm):
    id = IntegerField('Employee_id', validators=[DataRequired()])
    name = StringField('Employee Full name', validators=[DataRequired()])
    position = StringField('Employee position', validators=[DataRequired()])
    manager_id = IntegerField('Employee`s manager id', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    work_start = StringField('Joined structure', validators=[DataRequired()])
