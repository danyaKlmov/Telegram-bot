from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд.

    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_two_in_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками по 2 элемента в ряду

    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = []
    keyboard = []

    for item in items:
        row.append(KeyboardButton(text=item))

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if len(items) % 2 == 1:
        keyboard.append([KeyboardButton(text=items[-1])])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


