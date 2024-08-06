import click
from ..database import sessionLocal, init_db
from ..models import User, Client, Contract, Event
from dotenv import load_dotenv
import os

init_db()

session = sessionLocal()

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")


def verify_token(token):
    user_id = User.verify_token(token, SECRET_KEY)
    return user_id


def read_token_from_file():
    try:
        with open("token.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


@click.group()
@click.pass_context
def events(ctx):
    token = read_token_from_file()
    if not token:
        click.echo("Vous n'êtes pas connecté.")
        raise click.Abort()
    user_id = verify_token(token)
    if user_id is None:
        click.echo("Token invalide ou expiré.")
        raise click.Abort()
    ctx.obj["user_id"] = user_id


@events.command()
def list_users():
    """Lister tous les utilisateurs"""
    users = session.query(User).all()
    for user in users:
        click.echo(f"Utilisateur: {user.email}, Rôle: {user.department}")


@events.command()
def list_clients():
    """Lister tous les clients"""
    clients = session.query(Client).all()
    for client in clients:
        click.echo(
            f"Nom: {client.full_name}, Email: {client.email}, Téléphone: {client.phone}"
        )


@events.command()
def list_contracts():
    """Lister tous les contrats"""
    contracts = session.query(Contract).all()
    for contract in contracts:
        click.echo(
            f"ID: {contract.id}, Client: {contract.client_id}, Montant: {contract.total_amount}"
        )


@events.command()
def list_events():
    """Lister tous les événements"""
    events = session.query(Event).all()
    for event in events:
        click.echo(
            f"ID: {event.id}, Nom: {event.name}, Date de début: {event.start_date}, Lieu: {event.location}"
        )

