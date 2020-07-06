from exceptions.commandIncomplete import CommandIncomplete
from exceptions.emptyDocument import EmptyDocument
from exceptions.userNotFound import UserNotFound
from services.localizationService import i18n

from util.utility import add_warning, get_user, add_quote, get_warnings, get_quote_random
from validators.validateUserId import validate_user_id

async def quote(message, client):
    command = message.content.split(' ')

    try:
        validate_quote(command)
        quotee_id = validate_user_id(command[2])
        quoter_id = message.author.id

        quoter = get_user(client, quoter_id)
        quotee = get_user(client, quotee_id)

        # Give warning if bot is
        if quotee_id == client.user.id:
            add_warning(giver=get_user(client, client.user.id), taker=quoter,
                        reason=i18n.t('dialogs.quote.quote_bot_warning'))
            dialog = i18n.t('dialogs.quote.quote_bot').format(get_warnings(quoter))
        else:
            quote_ = add_quote(quoter=quoter, quotee=quotee, quote=' '.join(command[3:]).strip())
            if quotee_id == message.author.id:
                dialog = i18n.t('dialogs.quote.quote_self') + '\n'
            else:
                dialog = i18n.t('dialogs.quote.quote') + '\n'
            nick_quotee = message.guild.get_member(quotee_id).nick
            nick_quoter = message.guild.get_member(quoter_id).nick
            dialog += formulate_quote(quote_=quote_, nick_quotee=nick_quotee, nick_quoter=nick_quoter)
        await message.channel.send(dialog)
    except UserNotFound as e:
        await message.channel.send(e.message)
    except CommandIncomplete as e:
        await message.channel.send(e.message + '\n' + i18n.t('dialogs.error.command_incomplete'))


async def quotes(message, client):
    try:
        quote_ = get_quote_random()
        nick_quotee = message.guild.get_member(quote_.quotee.id).nick
        nick_quoter = message.guild.get_member(quote_.quoter.id).nick
        dialog = formulate_quote(quote_=quote_, nick_quotee=nick_quotee, nick_quoter=nick_quoter)
        await message.channel.send(dialog)
    except EmptyDocument as e:
        await message.channel.send(i18n.t('dialogs.quote.quote_empty'))

def formulate_quote(quote_, nick_quotee, nick_quoter):
    dialog = '>>> **"{0}"** — *{1}*\n\n`{2}\t{3}`'.format(quote_.quote, nick_quotee, quote_.date.strftime('%m.%d.%y'), nick_quoter)
    return dialog

def validate_quote(command: list):
    if len(command) == 3:
        raise CommandIncomplete('{0} {1} {2} **[{3}]**'.format(command[0], command[1], command[2],
                                                             i18n.t('dialogs.quote.missing_quote')))
    elif len(command) <= 2:
        raise CommandIncomplete(
            '{0} {1} **[@{2}] [{3}]**'.format(command[0], command[1], i18n.t('dialogs.quote.missing_quotee'),
                                          i18n.t('dialogs.warning.missing_quote')))
