import click
from app import create_app
from app.models import db, User

app = create_app()

@app.cli.command('create-user')
@click.argument('username')
@click.argument('password')
def create_user(username, password):
    with app.app_context():
        if User.query.filter_by(username=username).first():
            print(f"User {username} already exists")
            return
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"User {username} created successfully")