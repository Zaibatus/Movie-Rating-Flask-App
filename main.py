from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
MOVIES_DB_URL = "https://api.themoviedb.org/3/search/movie?query=Planet%20of%20apes&include_adult=false&language=en-US&page=1"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIES_DB_API_KEY = os.getenv('MOVIES_DB_API_KEY')
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-list.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(500), nullable=True)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)


class EditForm(FlaskForm):
    new_rating = FloatField('Your Rating Out of 10 e.g. 7.5')
    new_review = StringField('Your review')
    submit = SubmitField('Done')


class AddForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route("/")
def home():
    all_movies = []
    results = db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars()
    for result in results:
        all_movies.append(result)

    for movie in all_movies:
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.title == movie.title)).scalar()
        movie_to_update.ranking = all_movies.index(movie) + 1
        db.session.commit()

    return render_template("index.html", movies=all_movies)


@app.route("/edit/<int:id>", methods=['POST', 'GET'])
def edit(id):
    edit_form = EditForm()

    if request.method == "POST":
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        movie_to_update.rating = request.form.get("new_rating")
        movie_to_update.review = request.form.get("new_review")
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html", edit_form=edit_form)


@app.route('/del/<int:id>')
def delete(id):
    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['POST', 'GET'])
def add():
    add_form = AddForm()

    if add_form.validate_on_submit():
        movie_title = add_form.title.data
        response = requests.get(MOVIES_DB_URL, params={"api_key": MOVIES_DB_API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template('select.html', options=data)

    return render_template("add.html", add_form=add_form)


@app.route('/select/<int:movie_id>')
def select(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}",
                            params={"api_key": MOVIES_DB_API_KEY, "movie_id": movie_id})
    data = response.json()

    with app.app_context():
        new_movie = Movie(title=data["original_title"],
                          img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
                          year=data["release_date"].split("-")[0],
                          description=data["overview"],
                          rating=0.0)
        db.session.add(new_movie)
        db.session.commit()

        new_movie_id = new_movie.id

    return redirect(url_for('edit', id=new_movie_id))


if __name__ == '__main__':
    app.run(debug=True)
