import click
from datetime import datetime
from ..database import sessionLocal, init_db
from epic_events.events.events_commands import events
from ..models import User, DepartmentEnum, Event

init_db()

session = sessionLocal()


@events.group()
@click.pass_context
def support(ctx):
    user_id = ctx.obj.get("user_id")
    department = User.get_user_department(session, user_id)
    if department != DepartmentEnum.support.value:
        click.echo('Accès refusé. Le département doit être "support".')
        raise click.Abort()
    else:
        click.echo('Accès autorisé. Vous êtes dans le département "support".')


@support.command()
@click.pass_context
def update_event(ctx):
    """Modifier un événement"""
    event_id = click.prompt("ID événement")
    event = session.query(Event).filter_by(id=event_id).first()
    if not event:
        click.echo(f"L'événement avec l'ID {event_id} n'existe pas.")
        return
    if event.support_contact_id != ctx.obj.get("user_id"):
        click.echo("Vous n'etes pas responsable de cet événement")
        return

    event.name = click.prompt("Nom", default=event.name)
    event.location = click.prompt("Lieu", default=event.location)
    event.attendees = click.prompt("Participants", default=event.attendees)
    event.notes = click.prompt("Notes", default=event.notes)
    while True:
        start_date_str = click.prompt(
            "Date de début (YYYY-MM-DD)", default=event.start_date
        )
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            event.start_date = start_date
            break
        except ValueError:
            click.echo("Format de date invalide. Utilisez le format YYYY-MM-DD.")
    while True:
        end_date_str = click.prompt(
            "Date de début (YYYY-MM-DD)", default=event.end_date
        )
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            event.end_date = end_date
            break
        except ValueError:
            click.echo("Format de date invalide. Utilisez le format YYYY-MM-DD.")

    session.commit()
    click.echo(f"L'événement avec l'ID {event_id} mises à jour avec succès.")


@support.command()
@click.pass_context
def list_user_events(ctx):
    """Liste des événements attribués"""
    events = session.query(Event).filter(
        Event.support_contact_id == ctx.obj.get("user_id")
    )
    for event in events:
        click.echo(
            f"ID: {event.id}, Nom: {event.name}, Date de début: {event.start_date}, Lieu: {event.location}"
        )
