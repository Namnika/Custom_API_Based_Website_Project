from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, URL


##WTFORM
class CreateArtForm(FlaskForm):
    slug = StringField('Slug', validators=[DataRequired()])
    created_at = DateTimeField("Created At", validators=[DataRequired()])
    updated_at = DateTimeField("Updated At", validators=[DataRequired()])
    title = StringField('Art Title', validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    medium = StringField('Medium', validators=[DataRequired()])
    date = StringField("Artworks Date", validators=[DataRequired()])
    dimension_in = StringField("Dimensions (in)", validators=[DataRequired()])
    dimension_cm = StringField("Dimensions (cm)", validators=[DataRequired()])
    collecting_institution = StringField("Collecting Institution", validators=[DataRequired()])
    additional_information = StringField("Additional Information")
    image_rights = StringField("Image Rights")
    thumbnail_url = StringField("Thumbnail URL", validators=[DataRequired(), URL()])
    large_img_url = StringField("Large Image URL", validators=[DataRequired(), URL()])
    larger_img_url = StringField("Larger Image URL", validators=[DataRequired(), URL()])
    medium_img_url = StringField("Medium Image URL", validators=[DataRequired(), URL()])
    medium_rectangle_url = StringField("Medium Rectangle Image URL", validators=[URL()])
    normalized_img_url = StringField("Normalized Image URL", validators=[URL()])
    small_img_url = StringField("Small Image URL", validators=[DataRequired(), URL()])
    square_img_url = StringField("Square Image URL", validators=[DataRequired(), URL()])
    tall_img_url = StringField("Tall Image URL", validators=[URL()])
    submit = SubmitField("Submit Art")


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Username', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class CommentForm(FlaskForm):
    comment_body = CKEditorField("Comment")
    submit = SubmitField("Submit")
