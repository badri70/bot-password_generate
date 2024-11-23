from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from generate_password import generate_password_logic


router = Router()
password_settings = {}
passwords = {}


class PasswrodState(StatesGroup):
    length = State()
    digits = State()
    letters = State()
    special_characters = State()


class SavePasswordState(StatesGroup):
    waiting_for_signature = State()


@router.message(CommandStart())
async def start(message: Message):
    keybord = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Сгенерировать пароль"), KeyboardButton(text="Настроить генерацию пароля")],
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
async def generate(message: Message, state: FSMContext):
    keybord = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сохранить пароль", callback_data="save")]
    ])

    user_data = await state.get_data()

    length = password_settings.get("length", 12)
    digits = password_settings.get("digits", True)
    letters = password_settings.get("letters", True)
    specials = password_settings.get("special_characters", True)

    password = generate_password_logic(length, digits, letters, specials)
    await state.update_data(password=password)
    await message.answer(f"Ваш пароль: {password}", reply_markup=keybord)


# Обработка нажатия кнопки "Сохранить пароль"
@router.callback_query(lambda call: call.data == "save")
async def save_password(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите подпись к паролю:")
    await state.set_state(SavePasswordState.waiting_for_signature)


@router.message(SavePasswordState.waiting_for_signature)
async def get_signature(message: Message, state: FSMContext):
    user_data = await state.get_data()
    password = user_data.get("password")
    signature = message.text

    # Логика сохранения пароля с подписью
    passwords[f'{signature}'] = f'{password}'
    # Здесь можно сохранить в базу данных, файл или отправить куда-либо
    await message.answer(f"Пароль сохранен!\nПодпись: {signature}\nПароль: {password}")
    await state.clear()


@router.message(lambda message: message.text == "Настроить генерацию пароля")
async def configure_password(message: Message, state: FSMContext):
    await message.answer("Введите длину пароля (например, 12):")
    await state.set_state(PasswrodState.length)


@router.message(PasswrodState.length)
async def set_length(message: Message, state: FSMContext):
    await state.update_data(length=int(message.text))
    await message.answer("Включать цифры? (да/нет):")
    await state.set_state(PasswrodState.digits)


@router.message(PasswrodState.digits)
async def set_digits(message: Message, state: FSMContext):
    include_digits = message.text.lower() in ["да", "yes"]
    await state.update_data(digits=include_digits)
    await message.answer("Включать буквы? (да/нет):")
    await state.set_state(PasswrodState.letters)


@router.message(PasswrodState.letters)
async def set_letters(message: Message, state: FSMContext):
    include_letters = message.text.lower() in ["да", "yes"]
    await state.update_data(letters=include_letters)
    await message.answer("Включать спецсимволы? (да/нет):")
    await state.set_state(PasswrodState.special_characters)


@router.message(PasswrodState.special_characters)
async def save_custom_settings(message: Message, state: FSMContext):
    include_specials = message.text.lower() in ["да", "yes"]
    await state.update_data(special_characters=include_specials)
    settings = await state.get_data()
    password_settings['length'] = settings.get("length", 12)
    password_settings['digits'] = settings.get("digits", True)
    password_settings['letters'] = settings.get("letters", True)
    password_settings['special_characters'] = settings.get("special_characters", True)
    await message.answer("Настройки сохранены! Вы можете теперь сгенерировать пароль.")
    await state.clear()


@router.message(lambda message: message.text == "Сохраненные пароли" or message.text == "/saved")
async def show_all_passwords(message: Message):
    for key, value in passwords.items():
        await message.answer(f"{key}: {value}")


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
