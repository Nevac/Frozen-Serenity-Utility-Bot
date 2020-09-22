from services.localizationService import i18n
from collections import defaultdict
from commands.unknown import unknown
import boto3
from configparser import ConfigParser

config = ConfigParser()
config.read('app.config')
server = boto3.client('lightsail',
                      aws_access_key_id=config['Minecraft']['AwsServerPublicKey'],
                      aws_secret_access_key=config['Minecraft']['AwsServerSecretKey'],
                      region_name=config['Minecraft']['ServerRegion'])


def cmd_not_found():
    return unknown


async def start(message, client):
    server.start_instance(instanceName=config['Minecraft']['Instance'])
    await message.channel.send(i18n.t('dialogs.minecraft.start'))


async def status(message, client):
    instance = server.get_instance_state(instanceName=config['Minecraft']['Instance'])
    if instance['state']['name'] == 'running':
        await message.channel.send(i18n.t('dialogs.minecraft.online'))
    else:
        await message.channel.send(i18n.t('dialogs.minecraft.offline'))


commands = defaultdict(cmd_not_found)
commands.update({
    i18n.t('commands.minecraft.start'): start,
    i18n.t('commands.minecraft.status'): status
})


async def minecraft(message, client):
    command = message.content.split(' ')
    await commands[command[2]](message, client)
