# Telegram Message Forwarding Bot 🤖

A Python-based Telegram bot that forwards messages from authorized users to a specific group and sends welcome messages to new members. The bot supports text messages, photos, and document-type images. 📱✨

## ✨ Features

- 📬 Message forwarding from authorized users to a target group
- 🖼️ Support for text messages and images (both as photos and documents)
- 👋 Automated welcome messages for new group members
- 📝 Comprehensive logging system with daily rotating logs
- ⚠️ Error handling and detailed debugging capabilities

## 🔧 Prerequisites

- 🐍 Python 3.7 or higher
- 📚 python-telegram-bot library (v20.0 or higher)
- 🔑 A Telegram Bot Token from [@BotFather](https://telegram.me/BotFather)
- 👥 Target group ID
- 🆔 Authorized user ID

## 🤖 Creating Your Bot with BotFather

1. Open Telegram and search for [@BotFather](https://telegram.me/BotFather) or click the link
2. Start a chat with BotFather and send `/newbot`
3. Follow the instructions to name your bot
4. Save the API token provided by BotFather - you'll need it for configuration!

## 🚀 Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install the required dependencies:
```bash
pip install python-telegram-bot
```

3. Configure the bot:
   - Open the main script
   - Set the following variables:
     - `TOKEN`: Your Telegram bot token from BotFather
     - `TARGET_GROUP_ID`: The ID of the group where messages will be forwarded
     - `YOUR_USER_ID`: Your Telegram user ID (for authorization)

## ⚙️ Configuration

The bot requires the following environment variables:

```python
TOKEN = "your_bot_token_here"  # Get this from BotFather
TARGET_GROUP_ID = "your_target_group_id_here"
YOUR_USER_ID = "your_user_id_here"
```

## 📱 Usage

1. Start the bot:
```bash
python main.py
```

2. Send the `/start` command to your bot to initiate interaction

3. Send any message or photo to the bot (only authorized users can use this feature)

4. The bot will forward your message to the specified group ✨

## 👋 Welcome Message

The bot automatically sends a welcome message to new members when they join the group. The welcome message includes:
- 🎉 A personalized greeting with the new member's name
- ℹ️ Information about the group's purpose
- 🎯 Key features and benefits
- 🌟 Encouragement for participation

## 📝 Logging

The bot implements a comprehensive logging system:
- 📁 Logs are stored in the `logs` directory
- 📅 Daily rotating log files are created
- 🖥️ Both file and console logging are enabled
- 🔍 Debug level logging for detailed troubleshooting
- 📊 Specific logging for member updates and message forwarding

## ⚠️ Error Handling

The bot includes robust error handling:
- 🚫 Unauthorized access attempts are logged and blocked
- ❌ Message forwarding errors are caught and reported
- 🔔 Member update processing errors are logged
- 🛠️ General error handler for unexpected issues

## 🔑 Bot Permissions

The bot requires the following permissions in the target group:
- 💬 Send messages
- 📷 Send media messages
- 👥 View members
- 👋 Send welcome messages to new members

## 🛠️ Troubleshooting

Common issues and solutions:

1. Bot not responding:
   - ✅ Check if the bot is running
   - 🔑 Verify the TOKEN is correct
   - 👮 Ensure the bot has necessary permissions

2. Messages not being forwarded:
   - 🆔 Confirm YOUR_USER_ID is correctly set
   - 👥 Verify TARGET_GROUP_ID is valid
   - 🔒 Check bot permissions in the target group

3. Welcome messages not sending:
   - 💌 Ensure the bot has permission to send private messages
   - 👑 Verify the bot is an admin in the group
   - 📝 Check the logs for specific errors

## 💬 Support

For support, please check the logs in the `logs` directory or create an issue in the repository. 🌟
