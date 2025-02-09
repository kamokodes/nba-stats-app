# app.py (Backend)
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Float)
    rebounds = db.Column(db.Float)
    assists = db.Column(db.Float)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    city = db.Column(db.String(50))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    players = db.relationship('Player', backref='team', lazy=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    
    # Add these relationships
    home_team = db.relationship('Team', foreign_keys=[home_team_id])
    away_team = db.relationship('Team', foreign_keys=[away_team_id])

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/players')
def players():
    all_players = Player.query.all()
    return render_template('players.html', players=all_players)

@app.route('/teams')
def teams():
    all_teams = Team.query.all()
    return render_template('teams.html', teams=all_teams)

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    results = Player.query.filter(Player.name.ilike(f'%{search_term}%')).all()
    return render_template('search_results.html', results=results)

@app.route('/player/<int:player_id>')
def player_detail(player_id):
    player = Player.query.get_or_404(player_id)
    return render_template('player_detail.html', player=player)

@app.route('/team/<int:team_id>')
def team_detail(team_id):
    team = Team.query.get_or_404(team_id)
    games = Game.query.filter((Game.home_team_id == team_id) | (Game.away_team_id == team_id)).all()
    return render_template('team_detail.html', team=team, games=games)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)