import os
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from forms import LoginForm, SignUpForm, CommentForm, CreateArtForm


EMAIL = "YOUR EMAIL"
PASS = "YOUR PASSWORD"
app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ['CLIENT_ID']
app.config['SECRET_ID'] = os.environ['CLIENT_SECRET']
ckeditor = CKEditor(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

# *****CONNECT TO DB********

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ******AUTHENTICATION and WORK API********
# below code is comment because the api token has already expired and data has been extract from art api

# client_id = os.environ['CLIENT_ID']
# client_secret = os.environ['CLIENT_SECRET']

# api_url = "https://api.artsy.net/api/tokens/xapp_token"
# parameters = {
#     "client_id": client_id,
#     "client_secret": client_secret,
# }
# response = requests.post(api_url, params=parameters)
# response.raise_for_status()
# xapp_token = response.json()["token"]
# header = {
#     "client_id": client_id,
#     "client_secret": client_secret,
#     "xapp_token": xapp_token
# }
# artworks_response = requests.get("https://api.artsy.net/api/artworks", params=header)
# artworks_response.raise_for_status()
# artworks = artworks_response.json()["_embedded"]["artworks"]
#
# img_ver = []
# img_link = []
# for i in artworks:
#     artworks_id = i["id"]
#     # print(artworks_id)
#     artworks_slug = i["slug"]
#     # print(artworks_slug)
#     artworks_created_at = i["created_at"]
#     splitted_dt = re.split("T", artworks_created_at, 1)
#     dt = splitted_dt[0]
#     time = splitted_dt[1].split("+")[0]
#     d_t = (dt, time)
#     artworks_created_at_date = " ".join(d_t)
#     # print(artworks_created_at_date)
#
#
#     artworks_updated_at = i["updated_at"]
#     splitted_dt = re.split("T", artworks_updated_at, 1)
#     dt = splitted_dt[0]
#     time = splitted_dt[1].split("+")[0]
#     d_t = (dt, time)
#     artworks_updated_at_date = " ".join(d_t)
#     # print(artworks_updated_at_date)
#     title = i["title"]
#     # print(title)
#
#     category = i["category"]
#     # print(category)
#
#     medium = i["medium"]
#     # print(medium)
#
#     date = i["date"]
#     # print(date)
#
#     dimensions_in = i["dimensions"]["in"]["text"]
#     # print(dimensions_in)
#
#     dimensions_cm = i["dimensions"]["cm"]["text"]
#     # print(dimensions_cm)
#
#     collecting_institution = i["collecting_institution"]
#     # print(collecting_institution)
#
#     additional_information = i["additional_information"]
#     # print(additional_information)
#
#     image_rights = i["image_rights"]
#     # print(image_rights)
#
#     image_versions = i["image_versions"]
#     img_ver.append(image_versions)
#
#     thumbnail_links = i["_links"]["thumbnail"]["href"]
#     # print(thumbnail_links)
#
#     image_links = i["_links"]["image"]["href"]
#     img_link.append(image_links)

# img_links = []
# for vers in img_ver:
#     for v in vers:
#         img_sizes = v
#         for l in img_link:
#             all_img_links = l.split("{image_version}")[0] + img_sizes + ".jpg"
#             img_links.append(all_img_links)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


gravatar = Gravatar(app=app, size=1, rating='g', default='mp', force_default=False, force_lower=False,
                    use_ssl=False, base_url=None)


## CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    # ********ONE TO MANY RELATIONSHIP ***********

    arts = relationship('Adminart', back_populates='admin')
    comments = relationship("Comment", back_populates='comment_user')
    # *********************************************
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)  # should be checked by username


# db.create_all()

class Adminart(db.Model):
    __tablename__ = "artist_artworks"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(250), unique=True, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # **********Parent_class(User) 'users.id'
    # which in the format of Camel_Case converted into
    # 'camel_case'***********

    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(250), nullable=False)
    medium = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    dimension_in = db.Column(db.String(250), nullable=False)
    dimension_cm = db.Column(db.String(250), nullable=False)
    collecting_institution = db.Column(db.String(250), nullable=False)
    additional_information = db.Column(db.String(250), nullable=False)
    image_rights = db.Column(db.String(250), nullable=False)
    thumbnail_link = db.Column(db.String(250), nullable=False)
    large_img_link = db.Column(db.String(250), nullable=False)
    larger_img_link = db.Column(db.String(250), nullable=False)
    medium_img_link = db.Column(db.String(250), nullable=False)
    medium_rec_img_link = db.Column(db.String(250), nullable=False)
    normalized_img_link = db.Column(db.String(250), nullable=False)
    small_img_link = db.Column(db.String(250), nullable=False)
    square_img_link = db.Column(db.String(250), nullable=False)
    tall_img_link = db.Column(db.String(250), nullable=False)

    # ***********PARENT RELATIONSHIP ***************
    comments = relationship('Comment', back_populates='admin_post')
    admin = relationship('User', back_populates='arts')


# db.create_all()

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_user = relationship('User', back_populates='comments')

    # ***********CHILD RELATIONSHIP *********
    artist_artworks_id = db.Column(db.Integer, db.ForeignKey('artist_artworks.id'), nullable=False)
    admin_post = relationship('Adminart', back_populates='comments')
    body = db.Column(db.Text, nullable=False)


# db.create_all()

def admin_only(f):
    @wraps(f)
    def forbidden(*args, **kwargs):
        if current_user.id != 1:
            abort(403)
        return f(*args, **kwargs)

    return forbidden


# ******READ ALL ARTS**********
@app.route("/")
def get_all_arts():
    arts = Adminart.query.all()

    return render_template("index.html", all_arts=arts, date=datetime.today().strftime('%B %d %Y'),)


# *****LOGIN*******
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        Email = request.form['email']
        Password = request.form['password']

        # Comparing user's entered email against email stored in database
        user = User.query.filter_by(email=Email).first()

        # Email doesn't exist
        if not user:
            flash("That email does not exist. Please try again.")
        # Password incorrect

        elif not check_password_hash(user.password, Password):
            flash("Password incorrect, Please try again.")

        # Email exists and password correct
        else:
            login_user(user)
            return redirect(url_for('get_all_arts'))
    return render_template("login.html", form=form)


# ******SIGNUP*******
@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if request.method == "POST":
        if User.query.filter_by(email=request.form['email']).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        new_user = User()
        new_user.email = request.form['email']
        new_user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
        new_user.username = request.form['Username']

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('get_all_arts'))
    return render_template("signup.html", form=form)


# ******LOGOUT******
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('get_all_arts'))


@app.route("/art/<int:artist_artworks_id>", methods=["GET", "POST"])
def view_art(artist_artworks_id):
    requested_art = Adminart.query.get(artist_artworks_id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or sign up to comment.")
            return redirect(url_for('login'))
        new_comment = Comment(body=form.comment_body.data, comment_user=current_user, admin_post=requested_art)
        db.session.add(new_comment)
        db.session.commit()
    return render_template("art.html", art=requested_art, form=form, current_user=current_user)


# *******ADDING RECORD**********
@app.route("/new-art", methods=["GET", "POST"])
@admin_only
def make_art():
    form = CreateArtForm()

    if form.validate_on_submit():
        admin_art = Adminart(slug=form.slug.data, admin_id=current_user.id,
                             created_at=form.created_at.data, updated_at=form.updated_at.data, title=form.title.data,
                             category=form.category.data,
                             medium=form.medium.data, date=form.date.data, dimension_in=form.dimension_in.data,
                             dimension_cm=form.dimension_cm.data,
                             collecting_institution=form.collecting_institution.data,
                             additional_information=form.additional_information.data,
                             image_rights=form.image_rights.data, thumbnail_link=form.thumbnail_url.data,
                             large_img_link=form.large_img_url.data,
                             larger_img_link=form.larger_img_url.data, medium_img_link=form.medium_img_url.data,
                             medium_rec_img_link=form.medium_rectangle_url.data,
                             normalized_img_link=form.normalized_img_url.data, small_img_link=form.small_img_url.data,
                             square_img_link=form.square_img_url.data,
                             tall_img_link=form.tall_img_url.data)
        db.session.add(admin_art)
        db.session.commit()
        return redirect(url_for("get_all_arts"))
    return render_template("make-art.html", form=form, current_user=current_user)


# ******UPDATE RECORD*******
@app.route("/edit-art/<artist_artworks_id>", methods=["GET", "POST"])
@admin_only
def edit_art(artist_artworks_id):
    art = Adminart.query.get(artist_artworks_id)
    edit_form = CreateArtForm(slug=art.slug, admin_id=current_user.id,
                              created_at=art.created_at, updated_at=art.updated_at, title=art.title,
                              category=art.category,
                              medium=art.medium, date=art.date, dimension_cm=art.dimension_cm,
                              dimension_in=art.dimension_in,
                              collecting_institution=art.collecting_institution,
                              additional_information=art.additional_information,
                              image_rights=art.image_rights, thumbnail_link=art.thumbnail_link,
                              large_img_link=art.large_img_link,
                              larger_img_link=art.larger_img_link, medium_img_link=art.medium_img_link,
                              medium_rec_img_link=art.medium_rec_img_link,
                              normalized_img_link=art.normalized_img_link, small_img_link=art.small_img_link,
                              square_img_link=art.square_img_link,
                              tall_img_link=art.tall_img_link
                              )
    if edit_form.validate_on_submit():
        art.slug = edit_form.slug.data
        art.medium = edit_form.medium.data
        art.large_img_link = edit_form.large_img_url.data
        art.dimension_cm = edit_form.dimension_cm.data
        art.dimension_in = edit_form.dimension_in.data
        art.additional_information = edit_form.additional_information.data
        art.date = edit_form.date.data
        art.created_at = edit_form.created_at.data
        art.updated_at = edit_form.updated_at.data
        art.category = edit_form.category.data
        art.collecting_institution = edit_form.collecting_institution.data
        art.image_rights = edit_form.image_rights.data
        art.larger_img_link = edit_form.larger_img_url.data
        art.medium_img_link = edit_form.medium_img_url.data
        art.medium_rec_img_link = edit_form.medium_rectangle_url.data
        art.square_img_link = edit_form.square_img_url.data
        art.tall_img_link = edit_form.tall_img_url.data
        art.small_img_link = edit_form.small_img_url.data
        art.normalized_img_link = edit_form.normalized_img_url.data
        art.title = edit_form.title.data
        art.thumbnail_link = edit_form.thumbnail_url.data
        db.session.commit()
        return redirect(url_for("view_art", artist_artworks_id=art.id))
    return render_template("make-art.html", form=edit_form, is_edit=True, current_user=current_user)


# *********DELETE RECORD**********
@app.route("/delete/<artist_artworks_id>")
@admin_only
def delete_art(artist_artworks_id):
    art = db.session.query(Adminart).get(artist_artworks_id)
    if art:
        db.session.delete(art)
        db.session.commit()
        return redirect(url_for("get_all_arts"))
    return render_template("login.html", artist_artworks_id=art.id)


if __name__ == "__main__":
    app.run(debug=True)
