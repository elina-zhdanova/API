from app import create_app

app = create_app()

from scripts.create_user import create_user
app.cli.add_command(create_user)

if __name__ == "__main__":
    app.run()