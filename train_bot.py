import telebot
import nltk_yes_no
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

TOKEN = ''  # add your bot token here

bot = telebot.TeleBot(TOKEN)
classifier = nltk_yes_no.teach()

saved_messages = {}


def _get_yes_no_keyboard(message_id):
    message_id = str(message_id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Correct', callback_data='correct-' + message_id
        ),
        telebot.types.InlineKeyboardButton(
            'Incorrect', callback_data='incorrect-' + message_id
        )
    )

    return keyboard


def _save_message(message_id, text):
    saved_messages[message_id] = text


def _get_message(message_id):
    return saved_messages[message_id]


def _remove_message(message_id):
    del saved_messages[message_id]


def _add_text_to_intention(text, intention):
    with open('data/' + intention + '.txt', "a") as intention_file:
        intention_file.write('\n' + text)
    intention_file.close()


def _get_choose_intentions_keyboard(message_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text='AGREE', callback_data='i:' + message_id + ':AGREE'),
        InlineKeyboardButton(text='DISAGREE', callback_data='i:' + message_id + ':DISAGREE')
    )

    return keyboard


@bot.message_handler(regexp='.*')
def all_other_text_messages_handler(message):
    chat_id = message.chat.id
    text = message.text
    message_id = str(chat_id) + '_' + str(message.message_id)
    print(message_id)
    _save_message(message_id, text)
    bot.send_message(
        chat_id=chat_id,
        text='<b>Agree:</b> ' + str(nltk_yes_no.classify_prob(classifier, text, 'AGREE')) + '\n' +
             '<b>Disagree:</b> ' + str(nltk_yes_no.classify_prob(classifier, text, 'DISAGREE')) + '\n' +
             '<b>Solution:</b> ' + nltk_yes_no.classify(classifier, text),
        parse_mode='HTML',
        reply_markup=_get_yes_no_keyboard(message_id)
    )


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    bot.answer_callback_query(query.id)
    data = query.data
    chat_id = query.message.chat.id
    telegram_message_id = query.message.message_id

    if data.startswith('correct-'):
        message_id = str(data[8:])
        _remove_message(message_id)
        bot.edit_message_reply_markup(chat_id, telegram_message_id, reply_markup=None)
    elif data.startswith('incorrect-'):
        message_id = data[10:]
        bot.edit_message_reply_markup(chat_id, telegram_message_id,
                                      reply_markup=_get_choose_intentions_keyboard(message_id))
    elif data.startswith('i:'):
        global classifier
        parsed_data = data.split(':')
        print(parsed_data)
        message_id = parsed_data[1]
        intention = parsed_data[2]
        text = _get_message(message_id)
        bot.edit_message_reply_markup(chat_id, telegram_message_id, reply_markup=None)
        _add_text_to_intention(text, intention)
        _remove_message(message_id)
        classifier = nltk_yes_no.teach()
        bot.send_message(chat_id, 'Saved as "' + parsed_data[2] + '" intention. And reteached!')


bot.polling(none_stop=True)
