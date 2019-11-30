from services.localizationService import i18n
from commands.warning import warning

commands = {
    i18n.t('commands.warning'): warning
}

def resolve_command(command):
    return commands[command]
