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


class AdminLogoutForm(FlaskForm):
    submit = SubmitField("退出登录")

class AdminNameEditForm(FlaskForm):
    admin_name = StringField(
        "管理员名称",
        render_kw={"placeholder": "修改管理员名称"},
        validators=[InputRequired()]
    )
    submit = SubmitField("提交")

class AdminPasswordEditForm(FlaskForm):
    password = PasswordField(
        "管理员密码",
        render_kw={"placeholder": "修改密码"},
        validators=[InputRequired()]
    )
    password_confirm = PasswordField(
        "确认密码",
        render_kw={"placeholder": "确认密码"},
        validators=[InputRequired(), EqualTo("password", message="两次密码不一致")]
    )
    submit = SubmitField("提交")