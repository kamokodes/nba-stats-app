from app import app, db, Player, Team, Game  # Make sure Game is imported

with app.app_context():
    # Delete existing tables
    db.drop_all()
    
    # Create new tables
    db.create_all()

    # Create sample teams
    lakers = Team(name='Lakers', city='Los Angeles', wins=45, losses=25)
    warriors = Team(name='Warriors', city='Golden State', wins=40, losses=30)
    celtics = Team(name='Celtics', city='Boston', wins=50, losses=20)

    # Create sample players
    lebron = Player(name='LeBron James', points=27.5, rebounds=8.0, assists=8.5, team=lakers)
    curry = Player(name='Stephen Curry', points=29.5, rebounds=5.5, assists=6.5, team=warriors)
    tatum = Player(name='Jayson Tatum', points=26.5, rebounds=7.0, assists=4.5, team=celtics)

    # Create sample games
    game1 = Game(
        date='2024-03-15',
        home_team_id=lakers.id,
        away_team_id=warriors.id,
        home_score=112,
        away_score=108
    )
    game2 = Game(
        date='2024-03-16',
        home_team_id=celtics.id,
        away_team_id=lakers.id,
        home_score=120,
        away_score=115
    )

    # Add and commit all data
    db.session.add_all([lakers, warriors, celtics, lebron, curry, tatum, game1, game2])
    db.session.commit()

print("Database initialized successfully!")
