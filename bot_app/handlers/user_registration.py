from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.keyboards.reply import (
    REGISTER_KBRD,
    MAIN_MENU_ACTIVE_KBRD,
    CANCEL_KBRD,
)
from bot_app.database.models import User

logger.add("error_logs.log", level="ERROR")

REGISTER = 'Регистрация'
CANT_REGISTER = 'Вы уже зарегистрированы'
ADD_NAME = 'Введите своё имя'
CANCEL = 'отмена'
CANCSEL_MSG = 'Действия отменены'
BACK = 'назад'
NO_STEP = 'Предыдущего шага нет, введите имя напишите "отмена"'
ADD_LAST_NAME = 'Введите фамилию'
ADD_EMAIL = 'Введите почту'
EMAIL_DOMAIN = '@groupeseb'
COMPLITE_MSG = 'Регистрация прошла успешно'
INVALID_EMAIL = 'Вы ввели не корпоративную почту'
EMAIL_EXIST = 'Пользователь с такой почтой уже существует. Введите другую почту'

NAME_RULES = 'Имя должно содержать только буквы. Пожалуйста, введите имя снова'
LAST_NAME_RULES = 'Фамилия должна быть только из букв. Введите её заново.'


user_reg_router = Router()


class AddUser(StatesGroup):
    name = State()
    last_name = State()
    email = State()

    texts = {
        'AddUser:name': 'Введите имя заново:',
        'AddUser:last_name': 'Введите фамилию заново:',
        'AddUser:mail': 'Введите мэйл заново:',
    }


@user_reg_router.message(StateFilter(None), F.text == REGISTER)
async def add_name(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """Start of user registration."""
    try:
        if await User.get(session, int(message.from_user.id)):
            await message.answer(
                CANT_REGISTER,
                reply_markup=MAIN_MENU_ACTIVE_KBRD
            )
            await state.clear()
            return
        else:
            await message.answer(
                ADD_NAME,
                reply_markup=CANCEL_KBRD
            )
            await state.set_state(AddUser.name)
    except Exception as e:
        logger.error(f"Error in add_name function: {e}")


@user_reg_router.message(StateFilter('*'), Command(CANCEL))
@user_reg_router.message(StateFilter('*'), F.text.casefold() == CANCEL)
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Cancels all registration actions."""
    try:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.clear()
        await message.answer(CANCSEL_MSG, reply_markup=REGISTER_KBRD)
    except Exception as e:
        logger.error(f"Error in cancel_handler function: {e}")


@user_reg_router.message(StateFilter('*'), Command(BACK))
@user_reg_router.message(StateFilter('*'), F.text.casefold() == BACK)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    """Step back to register."""
    try:
        current_state = await state.get_state()
        if current_state == AddUser.name:
            await message.answer(NO_STEP)
            return
        previous = None
        for step in AddUser.__all_states__:
            if step.state == current_state:
                await state.set_state(previous)
                await message.answer(
                    f"""Вы вернулись к предыдущему шагу
                    {AddUser.texts[previous.state]}"""
                )
                return
            previous = step
    except Exception as e:
        logger.error(f"Error in back_step_handler function: {e}")


@user_reg_router.message(AddUser.name, F.text)
async def add_last_name(message: types.Message, state: FSMContext):
    """Adding last name."""
    try:
        name = message.text
        if check_alpha(name):
            await state.update_data(name=name)
            await message.answer(ADD_LAST_NAME)
            await state.set_state(AddUser.last_name)
        else:
            await message.answer(NAME_RULES)
            await state.set_state(AddUser.name)
    except Exception as e:
        logger.error(f"Error in add_last_name function: {e}")


@user_reg_router.message(AddUser.last_name, F.text)
async def add_mail(message: types.Message, state: FSMContext):
    """Adding mail."""
    try:
        last_name = message.text
        if check_alpha(last_name):
            await state.update_data(last_name=last_name)
            await message.answer(ADD_EMAIL)
            await state.set_state(AddUser.email)
        else:
            await message.answer(LAST_NAME_RULES)
            await state.set_state(AddUser.last_name)
    except Exception as e:
        logger.error(f"Error in add_mail function: {e}")


@user_reg_router.message(AddUser.email, F.text.contains(EMAIL_DOMAIN))
async def refister(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """End of registration."""
    try:
        tg_user = await User.get_by_email(session, message.text)
        if tg_user:
            await message.answer(EMAIL_EXIST)
        else:
            await state.update_data(email=message.text)
            data = await state.get_data()
            data['tg_id'] = message.from_user.id
            await User.create(session, data)
            await state.clear()
            await message.answer(COMPLITE_MSG, reply_markup=MAIN_MENU_ACTIVE_KBRD)
    except Exception as e:
        logger.error(f"Error in refister function: {e}")


@user_reg_router.message(AddUser.email)
async def invalid_mail(message: types.Message, state: FSMContext):
    """Report about incorrect mail."""
    try:
        await message.answer(INVALID_EMAIL)
    except Exception as e:
        logger.error(f"Error in invalid_mail function: {e}")


def check_alpha(input_string):
    """Checking all symbols are letters."""
    try:
        return all(char.isalpha() or char.isspace() for char in input_string)
    except Exception as e:
        logger.error(f"Error in check_alpha function: {e}")
