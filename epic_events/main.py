import click
from epic_events.users.users_commands import users
from epic_events.events.events_commands import events


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    pass


if __name__ == "__main__":
    cli.add_command(users)
    cli.add_command(events)
    cli()
