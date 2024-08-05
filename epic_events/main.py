import click
import sentry_sdk
from epic_events.users.users_commands import users
from epic_events.events.events_commands import events

sentry_sdk.init(
    dsn="https://c0969fe0342f43c011e6d8816ed00682@o4507176519925760.ingest.de.sentry.io/4507176522350672",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    pass


if __name__ == "__main__":
    cli.add_command(users)
    cli.add_command(events)
    cli()
