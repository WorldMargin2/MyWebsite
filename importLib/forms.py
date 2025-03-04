from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, StringField, PasswordField, SubmitField,FileField,IntegerField
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


class PushArticleForm(FlaskForm):
    title = StringField(
        "标题",
        render_kw={"placeholder": "请输入标题"},
        validators=[InputRequired()]
    )
    show_weight=IntegerField(
        "权重",
        render_kw={"placeholder": "请输入权重"},
        validators=[InputRequired()]
    )
    topest=RadioField(
        "是否置顶",
        choices=[(0, '否'), (1, '是')],
        default=1,
        validators=[InputRequired()]
    )
    zipfile = FileField(
        "上传文件",
        validators=[InputRequired()]
    )
    publish_now=RadioField(
        "是否立即发布",
        choices=[(0, '否'), (1, '是')],
        default=1,
        validators=[InputRequired()]
    )
    submit = SubmitField("提交")