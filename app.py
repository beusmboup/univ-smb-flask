from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialisation de Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Base de données SQLite
app.config['SECRET_KEY'] = 'your_secret_key'  # Clé secrète pour sécuriser les sessions
db = SQLAlchemy(app)

# Modèle pour les utilisateurs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Route d'accueil
@app.route('/')
def home():
    return render_template('home.html')

# Route d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur est déjà pris.', 'danger')
            return redirect(url_for('register'))

        # Hasher le mot de passe et l'enregistrer
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Inscription réussie! Connectez-vous maintenant.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Connexion réussie!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Identifiants incorrects.', 'danger')
    
    return render_template('login.html')

# Route de déconnexion
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('home'))

@app.route("/photo")
def photo():
    appareils = [
        {"marque": "Canon", "modele": "EOS 1500D", "date": "2019", "score": 4},
        {"marque": "Nikon", "modele": "D3500", "date": "2018", "score": 3},
        {"marque": "Sony", "modele": "Alpha 7R III", "date": "2021", "score": 5}
    ]
    return render_template('photo.html', appareils=appareils)


@app.route("/photography")
def photography():
    photos = [
        {"titre": "Nuit étoilée", "url": "images/photo1.jpg"},
        {"titre": "Aurore boréale", "url": "images/photo2.jpg"},
        {"titre": "Voie lactée", "url": "images/photo3.jpg"}
    ]
    return render_template('photography.html', photos=photos)


@app.route("/telescope")
def telescope():
    teles = [
        {"marque": "Celestron", "modele": "AstroMaster 70AZ", "date": "2020", "score": 4},
        {"marque": "Skywatcher", "modele": "Skymax 127", "date": "2021", "score": 5},
        {"marque": "Orion", "modele": "StarBlast 4.5", "date": "2019", "score": 3}
    ]
    return render_template('telescope.html', teles=teles)


# Lancement de l'application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Création des tables
    app.run(debug=True)
