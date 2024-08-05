import click
from datetime import datetime
from ..database import sessionLocal, init_db
from epic_events.events.events_commands import events
from ..models import User, DepartmentEnum, Client, Contract, Event

init_db()

session = sessionLocal()


def get_user_department(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user.department if user else None


@events.group()
@click.pass_context
def gestion(ctx):
    user_id = ctx.obj.get("user_id")
    department = get_user_department(user_id)
    if department != DepartmentEnum.gestion.value:
        click.echo('Accès refusé. Le département doit être "gestion".')
        raise click.Abort()
    else:
        click.echo('Accès autorisé. Vous êtes dans le département "gestion".')


@gestion.command()
def create_user():
    """Créer un nouvel utilisateur"""
    email = click.prompt("Email")
    password = click.prompt("Mot de Passe", hide_input=True, confirmation_prompt=True)

    valid_departments = ["commercial", "support", "gestion"]
    department = click.prompt("Department", type=click.Choice(valid_departments))

    new_user = User(email=email, password=password, department=department)
    session.add(new_user)
    session.commit()
    click.echo(
        f"Utilisateur '{email}' créé avec succès avec le département '{department}'."
    )


@gestion.command()
def update_user():
    """Modifier un utilisateur"""
    user_id = click.prompt("ID utilisateur")
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        click.echo(f"L'utilisateur avec l'ID {user_id} n'existe pas.")
        return

    user.email = click.prompt("Email", default=user.email)
    user.password = click.prompt(
        "Mot de Passe", hide_input=True, confirmation_prompt=True, default=user.password
    )

    valid_departments = ["commercial", "support", "gestion"]
    user.department = click.prompt(
        "Department", type=click.Choice(valid_departments), default=user.department
    )

    session.commit()
    click.echo(
        f"Informations de l'utilisateur avec l'ID {user_id} mises à jour avec succès."
    )


@gestion.command()
def delete_user():
    """Supprimer un utilisateur"""
    user_id = click.prompt("ID utilisateur")
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        click.echo(f"L'utilisateur avec l'ID {user_id} n'existe pas.")
        return

    confirmation = click.confirm(
        f"Êtes-vous sûr de vouloir supprimer l'utilisateur {user.email} ?"
    )
    if confirmation:
        session.delete(user)
        session.commit()
        click.echo(f"L'utilisateur avec l'ID {user_id} a été supprimé avec succès.")
    else:
        click.echo("Suppression annulée.")


@gestion.command()
def create_contract():
    """Créer un nouveau contrat"""

    client_id = click.prompt("ID client")
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        click.echo(f"Le client {client_id} n'existe pas.")
        return

    total_amount = click.prompt("Coût total")
    remaining_amount = click.prompt("Coût restant")
    is_signed = click.prompt("Contrat signé? (True/False)", type=bool)

    new_contract = Contract(
        client_id=client_id,
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        is_signed=is_signed,
        created_at=datetime.now(),
    )
    session.add(new_contract)
    session.commit()
    click.echo("Contrat crée avec succès.")


@gestion.command()
def update_contract():
    """Modifier un contrat"""
    contract_id = click.prompt("ID contrat")
    contract = session.query(Contract).filter_by(id=contract_id).first()
    if not contract:
        click.echo(f"Le contrat avec l'ID {contract_id} n'existe pas.")
        return

    client_id = click.prompt("ID client", default=contract.client)
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        click.echo(f"Le client {client_id} n'existe pas.")
        return
    contract.client_id = client_id

    contract.total_amount = click.prompt("Coût total", default=contract.total_amount)
    contract.remaining_amount = click.prompt(
        "Coût restant", default=contract.remaining_amount
    )
    contract.is_signed = click.prompt(
        "Contrat signé? (True/False)", type=bool, default=contract.is_signed
    )

    session.commit()
    click.echo(
        f"Informations du contrat avec l'ID {contract_id} mises à jour avec succès."
    )


@gestion.command()
def add_user_to_event():
    """Ajouter un utilisateur support à un événement"""
    event_id = click.prompt("ID événement")
    event = session.query(Event).filter_by(id=event_id).first()
    if not event:
        click.echo(f"L'événement avec l'ID {event_id} n'existe pas.")
        return

    support_contact_id = click.prompt("ID client")
    support_contact = (
        session.query(User)
        .filter_by(id=support_contact_id, department="support")
        .first()
    )
    if not support_contact:
        click.echo(f"L'utilisateur support {support_contact_id} n'existe pas.")
        return

    event.support_contact_id = support_contact_id
    session.commit()
    click.echo(
        f"Le collaborateur de l'événement avec l'ID {event_id} mises à jour avec succès."
    )


@gestion.command()
def list_events_without_support():
    """Liste des événements sans support"""
    events = session.query(Event).filter(Event.support_contact_id is None)
    for event in events:
        click.echo(
            f"ID: {event.id}, Nom: {event.name}, Date de début: {event.start_date}, Lieu: {event.location}"
        )
