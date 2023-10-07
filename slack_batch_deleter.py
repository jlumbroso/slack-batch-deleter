import os
import csv
import click
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from loguru import logger
from datetime import datetime

load_dotenv()


def slack_format_scope_error(e: SlackApiError, log_msg: bool = True) -> str:
    if (
        e.response["error"] == "missing_scope"
        and "needed" in e.response
        and "provided" in e.response
    ):
        needed = set(e.response["needed"].split(","))
        provided = set(e.response["provided"].split(","))
        checklist_with_scopenames = [
            "[x] " + scope_name if scope_name in provided else "[ ] " + scope_name
            for scope_name in sorted(list(needed))
        ]

        msg = "Missing scopes to run this command:\n  - " + "\n  - ".join(
            checklist_with_scopenames
        )

        if log_msg:
            logger.error(msg)

        return msg


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--token", default=os.environ.get("SLACK_API_TOKEN"), help="Slack API Token"
)
def list_channels(token):
    """List all available channels."""
    client = WebClient(token=token)
    try:
        response = client.conversations_list()
        for channel in response["channels"]:
            logger.info(channel["name"])
    except SlackApiError as e:
        logger.error("Error listing channels")
        if slack_format_scope_error(e) is None:
            logger.error(f"Response: {e.response}, {e}")


@click.command()
@click.argument("channel_name")
@click.option(
    "--token", default=os.environ.get("SLACK_API_TOKEN"), help="Slack API Token"
)
def dump(channel_name, token):
    """Dump messages from a channel to a CSV file."""
    client = WebClient(token=token)
    try:
        channel_id = None
        response = client.conversations_list()
        for channel in response["channels"]:
            if channel["name"] == channel_name.lstrip("#"):
                channel_id = channel["id"]
                break

        if channel_id:
            messages = client.conversations_history(channel=channel_id)["messages"]
            with open(f"{channel_name}.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [
                        "delete_or_not",
                        "timestamp",
                        "sender username",
                        "content",
                        "ts",
                        "channel_id",
                    ]
                )
                for message in messages:
                    human_readable_timestamp = datetime.utcfromtimestamp(
                        float(message["ts"])
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow(
                        [
                            "",
                            human_readable_timestamp,
                            message.get("user", ""),
                            message.get("text", ""),
                            message["ts"],
                            channel_id,
                        ]
                    )
        else:
            logger.error(f"Channel {channel_name} not found.")
    except SlackApiError as e:
        logger.error(f"Error dumping messages: {e.response['error']}")


@click.command()
@click.argument("csv_file")
@click.option(
    "--token", default=os.environ.get("SLACK_API_TOKEN"), help="Slack API Token"
)
def process(csv_file, token):
    """Process a CSV file and delete messages marked with 'X'."""
    client = WebClient(token=token)
    with open(csv_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            delete, _, _, _, msgid, channel_id = row
            if delete.upper() == "X":
                try:
                    client.chat_delete(channel=row[5], ts=row[4])
                    logger.info(f"Deleted message with ID: {msgid}")
                except SlackApiError as e:
                    logger.error("Error deleting message")
                    if slack_format_scope_error(e) is None:
                        logger.error(f"Response: {e.response}, {e}")


cli.add_command(list_channels)
cli.add_command(dump)
cli.add_command(process)

if __name__ == "__main__":
    cli()
