from collections import defaultdict
from services.localizationService import i18n

from commands.unknown import unknown
from commands.help import _help
from commands.warning import warning, warnings


def cmd_not_found():
    return unknown


commands = defaultdict(cmd_not_found)
commands.update({
    i18n.t('commands.help'): _help,
    i18n.t('commands.warning.warning'): warning,
    i18n.t('commands.warning.warnings'): warnings
})


def resolve_command(input_command):
    command_fragments = input_command.split(' ')

    if len(command_fragments) <= 1:
        return commands[i18n.t('commands.help')]

    command = command_fragments[1]
    return commands[command]
