import i18n
import configparser

config = configparser.ConfigParser()
config.read('app.config')
LOCALE = config['Discord']['Locale']

i18n.load_path.append('./locales')
i18n.set('locale', LOCALE)
i18n.set('fallback', 'en')