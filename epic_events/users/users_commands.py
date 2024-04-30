import click
from ..database import sessionLocal
from ..models import User
from dotenv import load_dotenv
import os

session = sessionLocal()

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")


def save_token_to_file(token):
    with open("token.txt", "w") as file:
        file.write(str(token))


def remove_token_file():
    try:
        os.remove("token.txt")
        click.echo("Fichier token supprimé avec succès.")
    except FileNotFoundError:
        click.echo("Aucun fichier token trouvé.")


@click.group()
def users():
    pass


@users.command()
def login():
    """Connexion avec email et mot de passe"""
    email = click.prompt("Email")
    password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
    user = session.query(User).filter_by(email=email, password=password).first()
    if user:
        token = User.generate_token(SECRET_KEY, user.id)
        save_token_to_file(token)
        click.echo(f"Connecté avec succès. Token: {token}")
    else:
        click.echo("Email ou mot de passe incorrect.")


@users.command()
def logout():
    """Déconnexion et suppression du fichier token"""
    remove_token_file()
    click.echo("Déconnecté avec succès.")
