from collections import defaultdict

from services.localizationService import i18n

from commands.unknown import unknown, none
from commands.help import help
from commands.hello import hello
from commands.warning import warning, warnings
from commands.statistic import giver, taker


def cmd_not_found():
    return unknown


commands = defaultdict(cmd_not_found)
commands.update({
    i18n.t('commands.help'): help,
    i18n.t('commands.warning.warning'): warning,
    i18n.t('commands.warning.warnings'): warnings,
    i18n.t('commands.statistic.giver'): giver,
    i18n.t('commands.statistic.taker'): taker
})
commands.update({cmd.strip(): hello for cmd in i18n.t('commands.hello').split(',')})


def resolve_command(input_command):
    command_fragments = input_command.split(' ')

    if len(command_fragments) <= 1:
        return none

    command = command_fragments[1]
    return commands[command]
