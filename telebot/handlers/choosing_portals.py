from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hlink

from keyboards.simple_row import make_two_in_row_keyboard
from model import get_by_url
from parsers.rss import rss_channels, news_urls, fun_urls

router = Router()


class Portal(StatesGroup):
    """
    Конечный автоматат для переключения
    между режимами "Новости" и "Развлекательные порталы"
    """
    choosing_news = State()
    choosing_fun = State()


@router.message(Command(commands=['news']))
async def cmd_choose(message: Message, state: FSMContext):
    """
    Выбор режима "новости".
    Отвечаем, создавая клавиатуру с выбором названия новостного портала.

    :param message: сообщение пользователя
    :param state: текущее состояние
    """
    await message.answer(
        text='Выберите портал:',
        reply_markup=make_two_in_row_keyboard(news_urls)
    )
    await state.set_state(Portal.choosing_news)


@router.message(Portal.choosing_news, F.text.in_(news_urls))
async def news_chosen(message: Message, state: FSMContext):
    """
    Обработчик ввода в режиме "Новости".
    Срабатывает, если введённый текст содержится в `news_urls`.

    :param message: сообщение пользователя
    :param state: текущее состояние
    """
    await state.update_data(chosen_news=message.text.lower())
    await message.answer(
        text='Загружаю свежие новости...',
        reply_markup=ReplyKeyboardRemove()
    )
    await send_news(message)
    await state.clear()


@router.message(Portal.choosing_news)
async def news_chosen_incorrectly(message: Message):
    """
    Обработчик ввода в режиме "Новости".
    Срабатывает, если не сработал предыдущий хэндлер,
    то есть если введённый текст не содержится в `news_urls`.

    :param message: сообщение пользователя
    """
    await message.answer(
        text='Я не знаю такого новостного портала.\n\n'
             'Пожалуйста, выберите из списка ниже:',
        reply_markup=make_two_in_row_keyboard(news_urls)
    )


@router.message(Command(commands=['fun']))
async def cmd_choose(message: Message, state: FSMContext):
    """
    Выбор режима "развлекательные порталы".
    Отвечаем, создавая клавиатуру с выбором названия развлекательного портала.

    :param message: сообщение пользователя
    :param state: текущее состояние
    """
    await message.answer(
        text='Выберите портал:',
        reply_markup=make_two_in_row_keyboard(fun_urls)
    )
    await state.set_state(Portal.choosing_fun)


@router.message(Portal.choosing_fun, F.text.in_(fun_urls))
async def news_chosen(message: Message, state: FSMContext):
    """
    Обработчик ввода в режиме "Развлекательные порталы".
    Срабатывает, если введённый текст содержится в `fun_urls`.

    :param message: сообщение пользователя
    :param state: текущее состояние
    """
    await state.update_data(chosen_fun=message.text.lower())
    await message.answer(
        text='Загружаю свежие посты...',
        reply_markup=ReplyKeyboardRemove()
    )
    await send_news(message)
    await state.clear()


@router.message(Portal.choosing_fun)
async def news_chosen_incorrectly(message: Message):
    """
    Обработчик ввода в режиме "Развлекательные порталы".
    Срабатывает, если не сработал предыдущий хэндлер,
    то есть если введённый текст не содержится в `fun_urls`.

    :param message: сообщение пользователя
    """
    await message.answer(
        text='Я не знаю такого развлекательного портала.\n\n'
             'Пожалуйста, выберите из списка ниже:',
        reply_markup=make_two_in_row_keyboard(fun_urls)
    )


async def send_news(message: types.Message):
    """
    Отправляет свежие посты,
    забирая из базы записи с соответствующим полем `domain`.
    Значение `domain` для фильтрации берёт из сообщения.

    :param message: сообщение пользователя
    """
    rss_url = rss_channels.get(message.text.lower())
    if rss_url is None:
        await message.answer(f'Вы выбрали: {message.text.lower()}. Пока новостей нет.\n\n')

    news = get_by_url(rss_url)
    for item in news:
        date = hbold(item.publish_date)
        header = hlink(item.title, item.link)
        await message.answer(
            f'{date}\n\n{header}\n\n',
            parse_mode='HTML'
        )
