from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate  # Import Flask-Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Ganti dengan path ke database kamu
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)  # Inisialisasi Flask-Migrate

# Model User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    games_played = db.Column(db.String(200), nullable=True)

# Ensure the database and tables are created
with app.app_context():
    db.create_all()  # Membuat tabel jika belum ada

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form['name']
    games_played = request.form['games_played']
    user = User(name=name, games_played=games_played)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('greeting', name=name))

@app.route("/view_users")
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)

@app.route("/greeting/<name>")
def greeting(name):
    return render_template('greeting.html', name=name)

@app.route("/about")
def about():
    return render_template("about.html")

# Menjalankan aplikasi
if __name__ == "__main__":
    app.run(debug=True)
