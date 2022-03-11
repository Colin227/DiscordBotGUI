import discord
from discord.ext import tasks
import asyncio
import commandHandler
import config

class MainBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.bg_task = self.loop.create_task(self.my_background_task())
        self.botStatus = "offline"

        self.my_background_task.start()
    
    async def on_ready(self):
        print('We have logged in as {0}!'.format(self.user))
        

    @tasks.loop(seconds=10)
    async def my_background_task(self):
        print("this is the background task")
        self.botStatus = "Connecting..."
        channel = self.get_channel(config.channel_id)
        await channel.send(self.botStatus)

    @my_background_task.before_loop
    async def before_my_task(self):
        print("this is the before my task")
        await self.wait_until_ready()
        print("this is the before my task but after wait until ready")





# if __name__ == "__main__":
#    # only to run when not called via 'import' here
client = MainBot()
client.run(config.api_token)
