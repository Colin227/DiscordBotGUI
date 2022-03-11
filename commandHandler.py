import discord
message = discord.Message

class MessageHandler(message):
    def __init__(self, message):
        if message.content.startswith('!'):
            self.command = 'Message from {0.author}: {0.content}'.format(message)
        else:
            self.command = "no command"

    def get_message_command(self):
        return self.command