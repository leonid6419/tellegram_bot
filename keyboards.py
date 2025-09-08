from pyrogram.types import KeyboardButton
from pyrogram.types import ReplyKeyboardMarkup
from pyrogram import emoji
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup

# Кнопки для основного меню
btn_info = KeyboardButton(f"{emoji.INFORMATION} Инфо")
btn_games = KeyboardButton(f"{emoji.VIDEO_GAME} Игры")
btn_profile = KeyboardButton(f"{emoji.PERSON} Профиль")


#кнопка квеста
inline_kb_start_quest = InlineKeyboardMarkup([
    [InlineKeyboardButton("Пройти квест",callback_data = "start_quest" )]
])
# Кнопки для игр
btn_rps = KeyboardButton(f'{emoji.PLAY_BUTTON} Камень ножницы бумага')
btn_quest = KeyboardButton(f'{emoji.CITYSCAPE_AT_DUSK} Квест')
btn_back = KeyboardButton(f'{emoji.BACK_ARROW} Назад')

# Кнопки для игры "Камень, ножницы, бумага"
btn_rock = KeyboardButton(f'{emoji.ROCK} Камень')
btn_scissors = KeyboardButton(f'{emoji.SCISSORS} Ножницы')
btn_paper = KeyboardButton(f'{emoji.NOTEBOOK} Бумага')
btn_rang = KeyboardButton(f"📈 рейтинг")

#кнопки для квеста
inline_kb_choice_door = InlineKeyboardMarkup([
    [InlineKeyboardButton("🚪⬅️  левая дверь ", callback_data="left_door" )],
    [InlineKeyboardButton("➡️🚪  правая дверь" , callback_data="right_door")]
])

inline_kb_left_door = InlineKeyboardMarkup([
    [InlineKeyboardButton("🐉  сражаться с драконом", callback_data="dragon")],
    [InlineKeyboardButton("🏃  попытаться убежать", callback_data="run")],
    [InlineKeyboardButton("🫣   попытаться спрятаться", callback_data="hide")]
])

inline_kb_right_door = InlineKeyboardMarkup([
    [InlineKeyboardButton("👑 золотая корона", callback_data="gold_crown")],
    [InlineKeyboardButton("🗡  серебренный кинжал", callback_data="silver_dagger")],
    [InlineKeyboardButton("📕  старая книга", callback_data="old_book")]
])

# Клавиатура для игры "Камень, ножницы, бумага"
kb_rps = ReplyKeyboardMarkup(
    keyboard=[
        [btn_rock, btn_scissors, btn_paper],
        [btn_back, btn_rang]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора игр
kb_games = ReplyKeyboardMarkup(
    keyboard=[
        [btn_rps],
        [btn_quest, btn_back]
    ],
    resize_keyboard=True
)

# Основная клавиатура
kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [btn_info, btn_games, btn_profile]
    ],
    resize_keyboard=True
)