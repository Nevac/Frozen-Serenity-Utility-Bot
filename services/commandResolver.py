from services.localizationService import i18n
from commands.warning import warning, warnings

commands = {
    i18n.t('commands.warning.warning'): warning,
    i18n.t('commands.warning.warnings'): warnings
}


def resolve_command(command):
    return commands[command]
