import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

FIO, AGE, CITY, PHONE, MAIL, DEGREE, SKILLS, EXP, PROJECTS, SALARY, SOURCE, DECISION = range(12)

recruitable = True

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
#    reply_keyboard = [['Boy', 'Girl', 'Other']]

#    update.message.reply_text(
#        'Hi! My name is Professor Bot. I will hold a conversation with you. '
#        'Send /cancel to stop talking to me.\n\n'
#        'Are you a boy or a girl?',
#        reply_markup=ReplyKeyboardMarkup(
#            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Boy or Girl?'
#        ),
#    )

    user = update.message.from_user
    update.message.reply_text(
        'Здравствуйте!:\n'
        'Нажмите /cancel, чтобы перестать общаться со мной'
    )

    update.message.reply_text('Ваше ФИО:')

    return FIO


def fio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("ФИО: %s", update.message.text)
    update.message.reply_text('Ваш возраст:')

    return AGE


def age(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Возраст: %s", update.message.text)
    if int(update.message.text) > 70:
        global recruitable
        recruitable = False
    update.message.reply_text('Ваш город проживания:')

    return CITY


def city(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Город проживания: %s", update.message.text)
    update.message.reply_text('Номер телефона:')
    return PHONE


def phone(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Номер телефона: %s", update.message.text)
    update.message.reply_text('Ваш E-mail:')
    return MAIL


def mail(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Электронная почта: %s", update.message.text)

    reply_keyboard = [['Да', 'Нет']]

    update.message.reply_text(
            'Есть ли у вас образование в сфере дизайна?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Да или Нет?'
            ),
        )
    return DEGREE


def degree(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Образовние дизайна: %s", update.message.text)
    if update.message.text == 'Нет':
        global recruitable
        recruitable = False
    reply_keyboard = [['Да', 'Нет']]

    update.message.reply_text(
            'Умеете ли вы работать в Adobe Illustrator и Photoshop?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Да или Нет?'
            ),
        )
    return SKILLS


def skills(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Навыки программ: %s", update.message.text)
    if update.message.text == 'Нет':
        global recruitable
        recruitable = False
    update.message.reply_text('Стаж работы дизайнером(в месяцах):')
    return EXP


def exp(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Стаж работы: %s", update.message.text)
    if int(update.message.text) < 12:
        global recruitable
        recruitable = False
    update.message.reply_text('Ссылка на портфолио:')
    return PROJECTS


def projects(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Ссылка на портфолио: %s", update.message.text)
    reply_keyboard = [['Да', 'Нет']]

    update.message.reply_text(
            'Готовы ли вы к работе на полную занятость в нашей компании, 5-8ч/день?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Да или Нет?'
            ),
        )

    return SALARY


def salary(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Полная занятость: %s", update.message.text)
    if update.message.text == 'Нет':
        global recruitable
        recruitable = False
    update.message.reply_text('Предпочитаемый уровень зарплаты:')
    return SOURCE


def source(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Предпочитаемый уровень зарплаты: %s", update.message.text)
    if int(update.message.text) > 70000:
        global recruitable
        recruitable = False
    update.message.reply_text('Спасибо за ответы!')
    if recruitable:
        update.message.reply_text('Мы приглашаем вас на собеседование!')
    else:
        update.message.reply_text('К сожалению, вы нам не подходите')
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2029907840:AAEHFt2qStkNbTZs3hxo2LicnzIf0w1J4bM")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIO: [MessageHandler(Filters.text & ~Filters.command, fio)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            CITY: [MessageHandler(Filters.text & ~Filters.command, city)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, phone)],
            MAIL: [MessageHandler(Filters.text & ~Filters.command, mail)],
            DEGREE: [MessageHandler(Filters.regex('^(Да|Нет)$'), degree)],
            SKILLS: [MessageHandler(Filters.regex('^(Да|Нет)$'), skills)],
            EXP: [MessageHandler(Filters.text & ~Filters.command, exp)],
            PROJECTS: [MessageHandler(Filters.text & ~Filters.command, projects)],
            SALARY: [MessageHandler(Filters.regex('^(Да|Нет)$'), salary)],
            SOURCE: [MessageHandler(Filters.text & ~Filters.command, source)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()