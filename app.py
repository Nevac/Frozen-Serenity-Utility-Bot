import discord
import configparser
from mongoengine import *
from services.commandResolver import resolve_command

client = discord.Client()
config = configparser.ConfigParser()
config.read('app.config')

PREFIX = config['Discord']['CommandPrefix'] + ' '
TOKEN = config['Discord']['Token']

connect(config['Discord']['DbConnectionHost'],
        host=config['Discord']['DbConnectionHost'], port=int(config['Discord']['DbConnectionPort']))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(PREFIX):
        command = message.content.split(' ', 2)[1]
        await resolve_command(command)(message, client)


client.run(TOKEN)