import i18n


class UserNotFound(Exception):
    def __init__(self):
        self.message = i18n.t('dialogs.error.user_not_found')

    def __str__(self):
        return str(self.message)
