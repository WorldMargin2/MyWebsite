from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired





class AdminLoginForm(FlaskForm):
    admin_name = StringField(
        "UserId",
        render_kw={"placeholder": "管理员名称"},
        validators=[InputRequired()]
    )
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "管理员密码"},
        validators=[InputRequired()]
    )
    submit = SubmitField("登录")