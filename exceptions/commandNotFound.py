import i18n


class CommandNotFound(Exception):
    def __init__(self):
        self.message = i18n.t('dialogs.error.command_not_found')

    def __str__(self):
        return str(self.message)
