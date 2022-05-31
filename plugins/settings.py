from pyrogram import emoji
from database import database
from pystark import Stark, Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Stark.cmd('kang', description='Definir configurações de bot pessoais.', private_only=True)
async def settings(_, msg: Message):
    text, markup = await user_settings(msg.from_user.id)
    await msg.react(text, reply_markup=markup)


async def user_settings(user_id):
    data = await database.get('users', user_id)
    if not data:
        return False, False
    tick = ' ✔'
    cross = ' ✖️ '
    ask_emojis = "Peça emojis"
    ask_emojis_msg = f"Defina como True se quiser que o bot solicite emojis que serão definidos para o adesivo de vídeo ao adicionar ao pacote. Se definido como Falso, todos os adesivos usarão emoji padrão, que é - {emoji.RED_HEART}"
    get_webm = "Pegue WEBM"
    get_webm_msg = f"Defina como True se desejar obter arquivos webm ao enviar qualquer adesivo de vídeo existente. Dessa forma, você pode adicionar adesivos de pacotes de outras pessoas usando @Stickers. Se for False, o bot irá ignorar o adesivo."
    kang_mode = "Kang Modo"
    kang_mode_msg = "Defina como Verdadeiro se quiser adicionar adesivos ao seu pacote apenas enviando um adesivo de vídeo de algum pacote existente. Dessa forma, você pode adicionar adesivos de pacotes de outras pessoas ao seu pacote. Se for False, o bot irá ignorar o adesivo."
    default_emojis = "Emojis padrão"
    default_emojis_msg = f"Defina emojis padrão para serem usados ​​em seus adesivos. Se nada estiver definido, {emoji.RED_HEART} será usado."
    text = f'**Definições** \n\n'
    ask_emojis_db = data['ask_emojis']
    get_webm_db = data['get_webm']
    kang_mode_db = data['kang_mode']
    default_emojis_db = data['default_emojis']
    general_text = "**{}** : {} \n{} \n\n"
    if ask_emojis_db:
        text += general_text.format(ask_emojis, 'True', ask_emojis_msg)
        ask_emojis += tick
    else:
        text += general_text.format(ask_emojis, 'False', ask_emojis_msg)
        ask_emojis += cross
    if get_webm_db:
        text += general_text.format(get_webm, 'True', get_webm_msg)
        get_webm += tick
    else:
        text += general_text.format(get_webm, 'False', get_webm_msg)
        get_webm += cross
    if kang_mode_db:
        text += general_text.format(kang_mode, 'True', kang_mode_msg)
        kang_mode += tick
    else:
        text += general_text.format(kang_mode, 'False', kang_mode_msg)
        kang_mode += cross
    if default_emojis_db:
        text += general_text.format(default_emojis, default_emojis_db, default_emojis_msg)
        default_emojis += ' - SET'
    else:
        text += general_text.format(default_emojis, 'Not Set', default_emojis_msg)
        default_emojis += ' - NOT SET'
    text += 'Use below buttons to change values. A tick means True and cross means False'
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(ask_emojis, callback_data="emojis")],
        [InlineKeyboardButton(default_emojis, callback_data="default_emojis")],
        [InlineKeyboardButton(kang_mode, callback_data="kang_mode")],
        [InlineKeyboardButton(get_webm, callback_data="webm")],
    ])
    return text, markup


async def default_emojis_settings(user_id):
    data = await database.get('users', user_id)
    if not data:
        return False, False
    data = data['default_emojis']
    if data:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Alterar emojis', callback_data="change_default_emojis")],
            [InlineKeyboardButton('Remover emojis padrão', callback_data="remove_default_emojis")],
            [InlineKeyboardButton('<-- Volte', callback_data="back")],
        ])
        text = f'Os emojis padrão atuais são `{data}` \n\nUse os botões abaixo para alterá-los ou removê-los'
    else:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Adicionar emojis', callback_data="change_default_emojis")],
            [InlineKeyboardButton('<-- Volte', callback_data="back")],
        ])
        text = 'Atualmente nenhum Emoji está definido. Use o botão abaixo para adicioná-los.'
    return text, markup
