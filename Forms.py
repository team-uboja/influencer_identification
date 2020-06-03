from wtforms import Form, BooleanField, StringField, validators, PasswordField, SubmitField

class LoginForm(Form):

    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.Length(min=6, max=35)])
    submit = SubmitField('Submit')

