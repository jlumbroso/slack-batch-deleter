# Slack Batch Deleter

## Introduction

Slack Message Manager is a command-line tool designed to interact with Slack channels. It allows users to list available channels, dump messages from a specific channel into a CSV file, and process a CSV file to delete selected messages.

## Setup

1. Clone the repository:
    ```bash
    git clone [repository_url]
    cd [repository_directory]
    ```

2. Install the required packages using pipenv:
    ```bash
    pipenv install
    ```

3. Run the tool:
    ```bash
    pipenv run python slack_batch_deleter.py [command]
    ```

## Export Format

Messages are exported in the following CSV format:

```csv
delete_or_not,timestamp,sender userID,content,ts,channel_id
```

Example:

```csv
delete_or_not,timestamp,sender userID,content,ts,channel_id
X,2023-10-06 10:00:00,User123,Hello there,1234567890.123456,ABCDEF123
,2023-10-06 10:05:00,User456,Hi!,1234567890.123457,ABCDEF123
```

In the above example, the message "Hello there" is marked for deletion with an "X" in the `delete_or_not` column.

## Obtaining a User Token with Required Scopes

Using this app requires access to the Slack API, using a user token with specific permissions. Follow these steps to obtain one:

1. Go to your Slack App settings page (or go to "Build" and "Create an App" to build one).
2. Navigate to the "OAuth & Permissions" section.
3. Under "User Token Scopes", click on "Add an OAuth Scope".
4. Add the following scopes:
   - `channels:read`: Allows the tool to view basic information about public channels in a workspace.
   - `channels:write`: Enables the tool to manage a user’s public channels and create new ones on their behalf.
   - `chat:write`: Grants permission to send messages on a user’s behalf.
   - `groups:read`: Provides access to view basic information about a user’s private channels.
   - `im:read`: Lets the tool view basic information about a user’s direct messages.
   - `mpim:read`: Allows viewing of basic information about a user’s group direct messages.
5. Once you've added these scopes, install or re-install your app to a workspace.
6. After installation, you'll be provided with a user token. Use this token with the Slack Message Manager.

Remember to keep your user token confidential. Do not share it or expose it in public repositories.

You can create a `.env` file in the root directory of this project, and add the following line to it (because this filename is listed in `.gitignore` it will not be committed accidentally):
```bash
SLACK_USER_TOKEN=[your_user_token]
```

## License

This project is licensed under the MIT License.

## Contributions

Contributions are welcome! Please submit a pull request with your proposed changes.