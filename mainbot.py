import config
import discord
from discord.ext import commands
import getMessage
import stockTracker
from datetime import date
import asyncio
import commandHandler
#from QtCore import pyqtSignal
class MainBot(discord.Client):
    #sig = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.botUsername = "not defined"
        self.add_commands()
        #self.sig.connect()

        #self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('We have logged in as {0}!'.format(self.user))
        #self.sig.emit()
        
        
        self.botUsername = self.user
        #await self.change_presence(activity=discord.Game('Bite my shiny metal ass'))

    def add_commands(self):
        @self.event
        async def on_message(message):
            if message.author == self.user:
                return
            if message.content.startswith('!'):
                botMessage = getMessage.getCommand(message.content, message.author.display_name, message.author)

                try:
                    # Check if botMessage returned a dictionary
                    weatherDict = botMessage.items()
                except (AttributeError, TypeError):
                    # if botMessage does not have items, we returned a string, so send message.
                    await message.channel.send(botMessage)
                else: # TODO: Try/except for creating the embedded message
                    embed=discord.Embed(title=botMessage["location"], description="Weather", color=0xffbb00)
                    embed.add_field(name=f'It is currently', value=f'{botMessage["currentTemp"]} C and {botMessage["currentCondition"].lower()}', inline=False)
                    embed.add_field(name='Tomorrow will be:', value=f'{botMessage["forecastAvgTemp"]} C and {botMessage["forecastCondition"].lower()}', inline=False)
                    
                    embed.set_thumbnail(url=botMessage["iconUrl"])
                    await message.channel.send(embed=embed)
                    
                



            # Stock commands start with dollar sign. If numbers come after the dollar sign respond with gif instead of stock information
            if message.content.startswith("$"):

                if (message.content.split('$')[1].isdigit()):
                    await message.channel.send(file=discord.File('./img/bender-money.gif'))

                else:
                    stockDict = stockTracker.getStockPrice(message.content)

                    # Exception will return STOCK_NOT_FOUND, we then send an image of broken bot.
                    if stockDict == "STOCK_NOT_FOUND":
                        await message.channel.send(file=discord.File('./img/bender-broken.gif'))

                    #Build the embedded message
                    #Creates a formatted embedded message for easier to read stock information.
                    #Adds fields for price change and percent change.
                
                    else:
                        # Create the embedded message with appropriate fields and values.
                        embed=discord.Embed(title=stockDict["symbol"], description=stockDict["shortName"], color=0x00947b)
                
                        embed.add_field(name=f'Current Price: {stockDict["currency"]}', value=f'${stockDict["currentPrice"]}', inline=False)
                        embed.add_field(name="Value Change:", value=f'${str(round(stockDict["dollarChange"], 2))}', inline=False)
                        embed.add_field(name="Percent Change:", value=f'{str(round(stockDict["percentChange"], 2))}%', inline=False)

                        if (stockDict['logo']):
                            embed.set_thumbnail(url=stockDict["logo"])
                            await message.channel.send(embed=embed)

                        # If the stock has no url or it was not located, set the default thumbnail to bot picture.
                        else:
                            file=discord.File("./img/bender-head.png", filename="bender-head.png")
                            embed.set_thumbnail(url="attachment://bender-head.png")
                            await message.channel.send(file=file, embed=embed)
                    



            # TODO: must separate to handle listening for messages asyncronously
            # async def on_message(self, message):
            #     if (message.content.startswith('!')):
            #         msg = commandHandler.MessageHandler(message)
            #         print(msg.get_message_command())

        if __name__ == "__main__":
        # only to run when not called via 'import' here
            client = MainBot()
            client.run(config.api_token)
            