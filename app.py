import discord
import configparser
from mongoengine import *

from exceptions.commandNotFound import CommandNotFound
from services.commandResolver import resolve_command

client = discord.Client()
config = configparser.ConfigParser()
config.read('app.config')

PREFIX = config['Discord']['CommandPrefix']
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
        try:
            await resolve_command(message.content)(message, client)
        except CommandNotFound as e:
            await message.channel.send(e.message)


client.run(TOKEN)
