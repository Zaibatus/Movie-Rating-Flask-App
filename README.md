# Movie Rating App

This is a Flask-based web application that allows users to manage and rate their favorite movies. The app integrates with The Movie Database (TMDb) API to fetch movie information and stores user ratings and reviews in a local database.

## Features

- View a list of movies sorted by user ratings
- Add new movies by searching The Movie Database
- Edit movie ratings and reviews
- Delete movies from the list
- Automatically update movie rankings based on ratings

## Technologies Used

- Flask: Web framework for Python
- SQLAlchemy: ORM (Object Relational Mapper) for database management
- Flask-WTF: For handling web forms
- Flask-Bootstrap5: For responsive design
- Requests: For making HTTP requests to The Movie Database API

## Setup and Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/movie-rating-app.git
cd movie-rating-app
```
2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```
3. Install the required packages:
```
pip install -r requirements.txt
```
4. Set up environment variables. Create a `.env` file in the root directory and add the following:
```
SECRET_KEY=your_secret_key_here
MOVIES_DB_API_KEY=your_tmdb_api_key_here
DB_URI=sqlite:///movies-list.db
```

## Usage

- Navigate to `http://localhost:5000` in your web browser
- Use the "Add Movie" button to search for and add new movies
- Click on a movie to edit its rating and review
- Use the delete button to remove a movie from your list

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
