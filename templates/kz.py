from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration de la base de données SQLite et de la clé secrète pour la session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Le fichier de base de données
app.config['SECRET_KEY'] = 'your_secret_key'  # Clé secrète pour sécuriser les sessions
db = SQLAlchemy(app)

# Modèle pour les utilisateurs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique de l'utilisateur
    username = db.Column(db.String(150), unique=True, nullable=False)  # Nom d'utilisateur
    password = db.Column(db.String(150), nullable=False)  # Mot de passe haché

# Route d'accueil
@app.route('/')
def home():
    return render_template('home.html')  # Rendu du template de la page d'accueil

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Récupération des données du formulaire de connexion
        username = request.form['username']
        password = request.form['password']
        
        # Recherche de l'utilisateur en base de données
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):  # Vérification du mot de passe
            session['user_id'] = user.id  # Enregistrement de l'ID de l'utilisateur dans la session
            flash('Connexion réussie!', 'success')  # Message de succès
            return redirect(url_for('home'))  # Redirection vers la page d'accueil
        else:
            flash('Identifiants incorrects.', 'danger')  # Message d'erreur si les identifiants sont incorrects
    return render_template('login.html')  # Rendu du template de la page de connexion

# Route d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Récupération des données du formulaire d'inscription
        username = request.form['username']
        password = request.form['password']
        
        # Vérification si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur est déjà pris.', 'danger')
            return redirect(url_for('register'))
        
        # Hachage du mot de passe avant de l'enregistrer
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Création d'un nouvel utilisateur et ajout à la base de données
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()  # Sauvegarde de l'utilisateur
        
        flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))  # Redirection vers la page de connexion
    return render_template('register.html')  # Rendu du template de la page d'inscription

# Route de déconnexion
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Suppression de l'ID de l'utilisateur de la session
    flash('Déconnexion réussie.', 'success')  # Message de succès
    return redirect(url_for('home'))  # Redirection vers la page d'accueil

# Route pour la page Appareil Photo
@app.route("/photo")
def photo():
    appareils = [
        {"marque": "Canon", "modele": "EOS 1500D", "date": "2019", "score": 4},
        {"marque": "Nikon", "modele": "D3500", "date": "2018", "score": 3}
    ]
    return render_template('photo.html', appareils=appareils)

# Route pour les Téléscopes
@app.route("/telescope")
def telescope():
    teles = [
        {"marque": "Celestron", "modele": "AstroMaster 70AZ", "date": "2020", "score": 4},
        {"marque": "Skywatcher", "modele": "Skymax 127", "date": "2021", "score": 5}
    ]
    return render_template('telescope.html', teles=teles)

# Route pour les Photographies
@app.route("/photography")
def photography():
    photos = [
        {"titre": "Nuit étoilée", "url": "photo1.jpg"},
        {"titre": "Aurore boréale", "url": "photo2.jpg"}
    ]
    return render_template('photography.html', photos=photos)

# Lancement de l'application Flask
if __name__ == '__main__':
    with app.app_context():  # 🔹 Ajout du contexte
        db.create_all()  # Création des tables dans la base de données si elles n'existent pas
    app.run(debug=True)  # Lancement de l'application en mode debug