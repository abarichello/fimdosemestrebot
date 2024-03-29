import re, pytz
import fimdosemestrebot.strings as strings
import fimdosemestrebot.config as config

from logging import info
from datetime import datetime, date
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode

tz = pytz.timezone('America/Sao_Paulo')


def start(bot, update):
    update.message.reply_text(check(get_end_date() - today()))
    update.message.reply_text(strings.INLINE)
    info(str(update))


# Read file and return datetime object
def get_end_date():
    file = open('file.date', 'r')
    end_date = datetime.strptime(file.readline(), '%d-%m-%Y %H:%M')
    return tz.localize(end_date)


# Function called when bot is used inline
def inline(bot, update):
    phrase = check(get_end_date() - today())

    results = []
    results.append(
        InlineQueryResultArticle(
            id=1,
            title=phrase,
            input_message_content=InputTextMessageContent(phrase),
            parse_mode=ParseMode.MARKDOWN,
        )
    )
    info(str(update))
    update.inline_query.answer(results)


# Returns a string according to n of days left
def check(days_left):
    string = strings.START_STRINGS
    if get_end_date().month >= 8:
        string = strings.END_STRINGS

    end_date = get_end_date().strftime("%d/%m/%y")
    end_date_str = f"({end_date})"
    time_left = ''
    if days_left.days < 0:
        return f'{strings.PALM_TREE} O semestre {string[2]} da UFSC {string[0]}! {end_date_str} {strings.CONFETTI} {strings.HORN}'
    elif days_left.days == 0:
        hours_left = int(days_left.total_seconds() // 3600)
        if hours_left == 1:
            time_left = "hora"
        else:
            time_left = "horas"
        return f'{strings.PALM_TREE} O semestre {string[2]} da UFSC {string[1]} em {hours_left} {time_left} {end_date_str}'
    elif days_left.days == 1:
        time_left = "dia"
    else:
        time_left = "dias"
    return f'{strings.PALM_TREE} O semestre {string[2]} da UFSC {string[1]} em {days_left.days} {time_left} {end_date_str}'


def today():
    return datetime.now(tz=tz)


# Used to change the target date
def set_date(bot, update, job_queue, chat_data):
    if str(update.message.chat.id) == config.MAINTAINER:
        contents = update.message.text.strip('/set ')
        update.message.reply_text("Set date as: " + contents)
        file = open('file.date', 'w')
        file.write(contents)
    else:
        update.message.reply_text(
            strings.DENIED + "\nYour id: " + str(update.message.chat.id)
        )


def get_help(bot, update):
    update.message.reply_text(strings.HELP_TXT)
