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
def commercial(ctx):
    user_id = ctx.obj.get("user_id")
    department = get_user_department(user_id)
    if department != DepartmentEnum.commercial.value:
        click.echo('Accès refusé. Le département doit être "commercial".')
        raise click.Abort()
    else:
        click.echo('Accès autorisé. Vous êtes dans le département "commercial".')


@commercial.command()
@click.pass_context
def create_client(ctx):
    """Créer un nouveau client"""
    full_name = click.prompt("Nom et Prénom")
    email = click.prompt("Email")
    phone = click.prompt("Téléphone")
    company_name = click.prompt("Entreprise")

    new_client = Client(
        full_name=full_name,
        email=email,
        phone=phone,
        company_name=company_name,
        creation_date=datetime.now(),
        last_contact_date=datetime.now(),
        commercial_contact_id=ctx.obj.get("user_id"),
    )
    session.add(new_client)
    session.commit()
    click.echo("Client creé avec succès")


@commercial.command()
@click.pass_context
def update_client(ctx):
    """Modifier un client"""
    client_id = click.prompt("ID client")
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        click.echo(f"Le client avec l'ID {client_id} n'existe pas.")
        return
    if client.commercial_contact_id != ctx.obj.get("user_id"):
        click.echo("Vous n'etes pas responsable de ce client")
        return

    client.full_name = click.prompt("Nom et Prénom", default=client.full_name)
    client.email = click.prompt("Email", default=client.email)
    client.phone = click.prompt("Téléphone", default=client.phone)
    client.company_name = click.prompt("Entreprise", default=client.company_name)

    session.commit()
    click.echo(f"Le client avec l'ID {client_id} mises à jour avec succès.")


@commercial.command()
@click.pass_context
def update_contract(ctx):
    """Modifier un contrat"""
    contract_id = click.prompt("ID contrat")
    contract = session.query(Contract).filter_by(id=contract_id).first()
    if not contract:
        click.echo(f"Le contrat avec l'ID {contract_id} n'existe pas.")
        return

    client = session.query(Client).filter_by(id=contract.client_id).first()
    if client.commercial_contact_id != ctx.obj.get("user_id"):
        click.echo("Vous n'etes pas responsable de ce client")
        return

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


@commercial.command()
@click.pass_context
def create_event(ctx):
    """Créer un nouvel événement"""

    contract_id = click.prompt("ID contrat")
    contract = session.query(Contract).filter_by(id=contract_id).first()
    if not contract:
        click.echo(f"Le contrat {contract_id} n'existe pas.")
        return
    if not contract.is_signed:
        click.echo(f"Le contrat {contract_id} n'est pas signé.")
        return
    client = session.query(Client).filter_by(id=contract.client_id).first()
    if client.commercial_contact_id != ctx.obj.get("user_id"):
        click.echo("Vous n'etes pas responsable de ce client")
        return

    support_contact_id = click.prompt("ID User")
    support_contact = (
        session.query(User)
        .filter_by(id=support_contact_id, department="support")
        .first()
    )
    if not support_contact:
        click.echo(f"L'utilisateur support {support_contact_id} n'existe pas.")
        return

    name = click.prompt("Nom")
    location = click.prompt("Lieu")
    attendees = click.prompt("Participants")
    notes = click.prompt("Notes")
    while True:
        start_date_str = click.prompt("Date de début (YYYY-MM-DD)")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            break
        except ValueError:
            click.echo("Format de date invalide. Utilisez le format YYYY-MM-DD.")
    while True:
        end_date_str = click.prompt("Date de début (YYYY-MM-DD)")
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            break
        except ValueError:
            click.echo("Format de date invalide. Utilisez le format YYYY-MM-DD.")

    new_event = Event(
        name=name,
        location=location,
        attendees=attendees,
        notes=notes,
        start_date=start_date,
        end_date=end_date,
        contract_id=contract_id,
    )
    session.add(new_event)
    session.commit()
    click.echo("Evenement creé avec succès")


@commercial.command()
def list_contracts_not_signed():
    """Lister des contrats non signés"""
    contracts = session.query(Contract).filter(Contract.is_signed == False)
    for contract in contracts:
        click.echo(
            f"ID: {contract.id}, Client: {contract.client_id}, Montant: {contract.total_amount}"
        )


@commercial.command()
def list_contracts_not_payed():
    """Lister des contrats non payés"""
    contracts = session.query(Contract).filter(Contract.remaining_amount != 0)
    for contract in contracts:
        click.echo(
            f"ID: {contract.id}, Client: {contract.client_id}, Montant: {contract.total_amount}"
        )
