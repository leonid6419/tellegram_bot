import os
from pyrogram import Client, filters
import datetime
import json
import random
from pyrogram.filters import reply
from FusionBrain_AI import generate
import config
import keyboards
import base64

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="my_bot",
)

def button_filter(button):
    async def func(_, __, msg):
        return msg.text.strip() == button.text.strip()
    return filters.create(func, "ButtonFilter", button=button)

if not os.path.exists("users.json"):
    with open("users.json", "w") as file:
        json.dump({}, file)

@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply("Добро пожаловать!", reply_markup=keyboards.kb_main )
    await bot.send_sticker(message.chat.id,"CAACAgQAAxkBAAENGypnMjCCgA_6VdcplrIAAae7GeK2rjgAAvsPAAJ0UylSBpgo6K2GlCM2BA")
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}
    if str(message.from_user.id) not in users.keys():
        users[message.from_user.id] = 100
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

@bot.on_message(filters.command("info") | button_filter(keyboards.btn_info))
async def info(bot, message):
    await message.reply("Привет! Тут описание что может этот бот и список команд")

@bot.on_message(filters.command("image"))
async def image(bot, message):
    if len(message.text.split()) > 1:
        query = message.text.replace('/image', '')
        await message.reply_text(f"Генерирую изображение по запросу '{query}', подождите немного…")
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1 , 200)
            with open(f"images/image{img_num}.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'images/image{img_num}.jpg', reply_to_message_id=message.id)
        else:
            await message.reply_text("Возникла ошибка, попробуйте еще раз", reply_to_message_id=message.id)
    else:
        await message.reply_text("Введите запрос")

@bot.on_message(filters.command("time"))
async def time(bot, message):
    await message.reply(f"Текущие дата и время: {datetime.datetime.now()}")

@bot.on_message(filters.command("games") | button_filter(keyboards.btn_games))
async def games(bot, message):
    await message.reply("Выбери игру", reply_markup=keyboards.kb_games)

@bot.on_message(filters.command("quest") | button_filter(keyboards.btn_quest))
async def kwest(bot, message):
    await message.reply_text("хотите отправиться в путешествие полное приключений и загадок", reply_markup=keyboards.inline_kb_start_quest)

@bot.on_callback_query()
async def handle_query(bot,query):

    if query.data =="start_quest":
        await bot.answer_callback_query(query.id,
        text="Добро пожаловать в квест под название Поиски Затерянного Сокровища! ",
        show_alert=True)
        await query.message.reply_text("Ты стоишь перед двумя дверьми .Какую из них выберешь?",reply_markup = keyboards.inline_kb_choice_door)
    elif query.data == 'left_door':
        await query.message.reply_text("Tы входишь в комнатy и видишь злого дракона! У тебя есть три варианта действий: ", reply_markup=keyboards.inline_kb_left_door)
    elif query.data == 'right_door':
        await query.message.reply_text("Ты входишь в комнатy, наполненную сокровищами!Тебе нужно выбрать только одно сокровище",reply_markup = keyboards.inline_kb_right_door)
    elif query.data == 'dragon':
        await bot.answer_callback_query(query.id, text="Ты сражаешься с драконом ,но он оказался сильнее.Ты погибаешь ☠",show_alert=True)
    elif query.data == 'run':
        await bot.answer_callback_query(query.id, text="Ты пытаешься убежать ,но дракон тебя догоняет и убивает ☠",show_alert=True)
    elif query.data == 'hide':
        await bot.answer_callback_query(query.id, text="Ты пытаешься спрятаться и дракон тебя не увидел.Ты выжил😃",show_alert=True)
    elif query.data == 'gold_crown':
        await bot.answer_callback_query(query.id, text="Ты берешь золотую корону и выходишь из комнаты .Поздравляю!Ты выиграл игру😃!", show_alert=True)
    elif query.data == 'silver_dagger':
        await bot.answer_callback_query(query.id, text="Ты берешь серебренный кинжал и выходишь из комнаты.К сожалению ,кинжал не чего не стоит 😐", show_alert=True)
    elif query.data == 'old_book':
        await bot.answer_callback_query(query.id, text="Ты берешь старую книгу и выходишь из комнаты.Книга оказалась магической!Ты открываешь станицу и исчезаешь😕 ",show_alert=True)
    await query.message.delete()

@bot.on_message(filters.command("back") | button_filter(keyboards.btn_back))
async def back(bot, message):
    await message.reply("Возврат в главное меню", reply_markup=keyboards.kb_main)

@bot.on_message(filters.command("game") | button_filter(keyboards.btn_rps))
async def game(bot, message):
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}
    if users.get(str(message.from_user.id), 0) >= 10:
        await message.reply("Твой ход", reply_markup=keyboards.kb_rps)
    else:
        await message.reply(f"Не хватает средств. На твоем счету {users.get(str(message.from_user.id), 0)}. Минимальная сумма для игры - 10")

@bot.on_message(filters.command("rang") | button_filter(keyboards.btn_rang))
async def rang(bot , message):
    try:

        with open("users.json", "r") as file:
            users = json.load(file)

        if not users:
            await message.reply("Список пользователей пуст! Похоже, никто ещё не добавлен.")
            return

        top_users = list(users.values())[:3]

        response = "Вот лучшие пользователи:\n"
        response += "\n".join([f"{i + 1}) {user}" for i, user in enumerate(top_users)])

        await bot.send_message(message.chat.id, response)

    except FileNotFoundError:
        await message.reply("Файл users.json не найден. Пожалуйста, добавьте пользователей!")
    except json.JSONDecodeError:
        await message.reply("Файл users.json повреждён. Проверьте его содержание!")

@bot.on_message(button_filter(keyboards.btn_rock) | button_filter(keyboards.btn_scissors) | button_filter(keyboards.btn_paper))
async def choice_rps(bot, message):
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    user = message.text
    pc = random.choice([keyboards.btn_rock.text, keyboards.btn_scissors.text, keyboards.btn_paper.text])

    if user == pc:
        await message.reply("Ничья")
    elif (user == keyboards.btn_rock.text and pc == keyboards.btn_scissors.text) or \
         (user == keyboards.btn_scissors.text and pc == keyboards.btn_paper.text) or \
         (user == keyboards.btn_paper.text and pc == keyboards.btn_rock.text):
        await message.reply(f"Ты выиграл. Бот выбрал {pc}", reply_markup=keyboards.kb_games)
        users[str(message.from_user.id)] = users.get(str(message.from_user.id), 0) + 10
    else:
        await message.reply(f"Ты проиграл. Бот выбрал {pc}", reply_markup=keyboards.kb_games)
        users[str(message.from_user.id)] = users.get(str(message.from_user.id), 0) - 10

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

try:
    bot.run()
except Exception as e:
    print(f"Ошибка при запуске бота: {e}")