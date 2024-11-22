import string
import random
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup



router = Router()


class PasswrodState(StatesGroup):
    length = State()
    digits = State()
    letters = State()
    Special_characters = State()


@router.message(CommandStart())
async def start(message: Message):
    keybord = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Сгенерировать пароль"), KeyboardButton(text="Настройки генерации")],
            [KeyboardButton(text="Сохраненные пароли"), KeyboardButton(text="Рекомендации по безопасности")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Привет! 👋\n"

        "Я — бот для генерации надежных и безопасных паролей. 🔐\n"
        "С моей помощью ты можешь:\n"

        "- Сгенерировать уникальный пароль любой сложности.\n"
        "- Настроить параметры пароля: длину, использование специальных символов и др.\n"
        "- Сохранить пароли для удобного доступа.\n"
        "- Узнать советы по безопасности.\n\n"

        "💡 Используй меню ниже или введи команды:\n"
        "- **/generate** — начать генерацию пароля.\n"
        "- **/settings** — настроить параметры генерации.\n"
        "- **/saved** — посмотреть сохраненные пароли.\n"
        "- **/help** — получить помощь.\n"
        "Давай сделаем твои пароли надежнее! 🚀"
                         
    , parse_mode="Markdown", reply_markup=keybord)


@router.message(lambda message: message.text == "Сгенерировать пароль" or message.text == "/generate")
async def generate(message: Message):
    keybord = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сохранить пароль", callback_data="save")]
    ])

    char = ""
    char+=string.ascii_letters
    char+=string.digits
    char+=string.punctuation

    password = []

    for el in range(14):
        letter = random.choice(char)
        password.append(letter)
    
    await message.answer("Ваш сгенерированный пароль: " + "".join(password), reply_markup=keybord)


@router.message(lambda message: message.text == "Рекомендации по безопасности" or message.text == "/help")
async def help(message: Message):
    help_text = """
    🔒 **Рекомендации по созданию надежных паролей**

    1. **Длина имеет значение**:
    Минимальная длина пароля должна быть не менее 12 символов. Чем длиннее, тем лучше.

    2. **Смешивайте символы**:
    Используйте буквы (заглавные и строчные), цифры и специальные символы (`!@#$%^&*`).

    3. **Не используйте личную информацию**:
    Избегайте использования имени, даты рождения или других легко угадываемых данных.

    4. **Уникальность пароля**:
    Используйте уникальный пароль для каждого аккаунта. Это предотвращает взлом всех ваших учетных записей, если один из паролей будет скомпрометирован.

    5. **Не используйте популярные пароли**:
    Избегайте комбинаций вроде `123456`, `password`, `qwerty` или подобных.

    6. **Регулярная смена паролей**:
    Периодически обновляйте свои пароли, особенно для важных учетных записей.

    7. **Используйте менеджер паролей**:
    Храните сложные пароли в надежных менеджерах, чтобы не запоминать их вручную.

    8. **Двухфакторная аутентификация (2FA)**:
    Всегда включайте 2FA там, где это возможно, для дополнительной защиты.
    """
    await message.answer(help_text, parse_mode="Markdown")
