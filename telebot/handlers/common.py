from aiogram import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command(commands=['start']))
async def cmd_start(message: Message, state: FSMContext):
    """
    Главный экран, отображаемый после команды `/start`.

    :param message: сообщение пользователя
    :param state: текущее состояние
    """
    await message.answer(
        'Привет! Здесь вы можете получить последние '
        'статьи из интесующего вас новостного /news или '
        'развлекательного /fun ресурса'
    )


@router.message(Command(commands=['choose']))
async def cmd_choose(message: Message, state: FSMContext):
    """
    Экран выбора команды,
    отображаемый после команды `/choose`.

    :param message: сообщение пользователя
    :param state: текущее состояние
    """
    await message.answer(text='Новости /news или развлекательный контент /fun ?')


@router.message(Command(commands=['cancel']))
@router.message(Text(text='отмена', text_ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    """
    Хэндлер для команды `/cancel`.
    Сбрасывает состояние конечного автомата на исходное.

    :param message: сообщение пользователя
    :param state: текущее состояние
    """
    await state.clear()
    await message.answer(
        text='Действие отменено',
        reply_markup=ReplyKeyboardRemove()
    )
