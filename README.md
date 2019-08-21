# Gatekeeper bot
This Telegram bot automatically prevents new users from posting anything. It also uses an inline keyboard which the newly joined user can use to prove that he/she is not a robot.

## Setting up
Set your bot token and chat id as env variables. Add the bot to your group as an admin, so it can read the messages.

## Operation
Every time a new user joins your group, the bot prevents the user from saying anything until he/she answers a question using the inline keyboard. Upon answering correctly, all restrictions will be lifted. If the answer is incorrect, the bot points this out and the user's restrictions have to be removed manually by an admin.
