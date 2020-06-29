import discord
import configparser
from mongoengine import connect

from services.commandResolver import resolve_command

client = discord.Client()
config = configparser.ConfigParser()
config.read('app.config')

PREFIX = config['Discord']['CommandPrefix']
TOKEN = config['Discord']['Token']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(PREFIX):
        await resolve_command(message.content)(message, client)


if len(TOKEN) == 0:
    print('Token not provided')
    exit()

connect(config['Discord']['DbConnectionHost'], host=config['Discord']['DbConnectionHost'], port=int(config['Discord']['DbConnectionPort']))
client.run(TOKEN)
