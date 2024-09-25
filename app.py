from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)  # Aktiviert CORS für alle Routen

# Movie Model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

# Initialisiere die Datenbank
with app.app_context():
    db.create_all()

# --- CRUD Endpoints ---

# Create a new movie
@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    if not data or not 'title' in data or not 'director' in data or not 'year' in data:
        return jsonify({"error": "Missing required fields: 'title', 'director', 'year'"}), 400

    new_movie = Movie(title=data['title'], director=data['director'], year=data['year'])
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({"message": "Movie created successfully!"}), 201

# Get all movies
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([{'id': movie.id, 'title': movie.title, 'director': movie.director, 'year': movie.year} for movie in movies])

# Get a single movie by ID
@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get_or_404(id)
    return jsonify({'id': movie.id, 'title': movie.title, 'director': movie.director, 'year': movie.year})

# Update a movie by ID
@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    movie.title = data.get('title', movie.title)
    movie.director = data.get('director', movie.director)
    movie.year = data.get('year', movie.year)

    db.session.commit()
    return jsonify({"message": "Movie updated successfully!"})

# Delete a movie by ID
@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie deleted successfully!"})

# Starte the Server
if __name__ == '__main__':
    try:
        app.run(debug=True, port=5000)
    except OSError as e:
        if "Address already in use" in str(e):
            print("Port 5000 is in use. Starting on port 5001.")
            app.run(debug=True, port=5001)
