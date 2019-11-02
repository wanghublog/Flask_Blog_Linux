#import FlaskForm
from flask_wtf import Form
from wtforms import (
	StringField, 
	TextField,
	TextAreaField,
	PasswordField,
	BooleanField,
	ValidationError,
	SubmitField,
    widgets
	)
from wtforms.validators import DataRequired, Length,EqualTo,URL
from wanghublog.models import User
from flask import flash
class LoginForm(Form):
    """Login Form"""

    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    verify_code = StringField('验证码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    def validate(self):
        """Validator for check the account information."""
        check_validata = super(LoginForm, self).validate()#字段检验器

        # If validator no pass
        if not check_validata:
            return False

        # Check the user whether exist.#在父类检验器基础上增加的功能
        user = User.query.filter_by(username=self.username.data).first()
	    
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False

        # Check the password whether right.
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password.')
            return False

        return True 


class CommentForm(Form):
    """Form vaildator for comment."""

    # Set some field(InputBox) for enter the data.
    # patam validators: setup list of validators
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)])

    text = TextField(u'Comment', validators=[DataRequired()])

class RegisterForm(Form):
    """Register Form."""

    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    comfirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])
    #recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        # If validator no pass
        if not check_validate:
            flash('两次输入的密码不一致',category="error")
            return False

        # Check the user whether exist.
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            flash('用户名已存在',category='error')
            self.username.errors.append('User with that name already exists.')
            return False
        return True

class PostForm(Form):
	title = StringField('Title',[DataRequired(),Length(max=255)])
	text = TextAreaField('Blog Content',[DataRequired()])

class CKTextAreaWidget(widgets.TextArea):
    """CKeditor form for Flask-Admin."""

    def __call__(self, field, **kwargs):
        """Define callable type(class)."""

        # Add a new class property ckeditor: `<input class=ckeditor ...>`
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    """Create a new Field type."""

    # Add a new widget `CKTextAreaField` inherit from TextAreaField.
    widget = CKTextAreaWidget()