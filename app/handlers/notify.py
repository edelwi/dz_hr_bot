import logging
from typing import Optional

from aiogram import Router, F
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from app.bot import bot
from app.kbd.send_cancel import get_send_cancel_kb
from app.middlewares.store import StoreMiddleware

router = Router()
router.message.middleware(StoreMiddleware())

# Вообще говоря, можно на роутер навесить кастомный фильтр
# с проверкой, лежит ли айди вызывающего во множестве admins.
# Тогда все хэндлеры в роутере автоматически будут вызываться
# только для людей из admins, это сократит код и избавит от лишнего if
# Но для примера сделаем через if-else, чтобы было нагляднее

action_names = ["Отправить", "Отменить", "Выйти"]
user_data = {}  # TODO: replace on state


class Notification(StatesGroup):
    edit = State()
    send = State()
    cancel = State()
    exit = State()
    # ready = State()


class EditAnswersCallbackFactory(CallbackData, prefix="answer"):
    action: str
    owner: int
    text_msg: Optional[str] = None


@router.message(Command("my_id"))
async def cmd_my_id(message: Message):
    logging.info("my_id")
    await message.answer(f"{message.from_user.id}")
    logging.info("got my_id")


@router.message(Command("chat_id"))
async def cmd_chat_id(message: Message):
    logging.info("chat_id")
    chat_id = message.chat.id if message.chat.id < 0 else "🤷"
    await message.answer(f"{chat_id} {message.chat.title}")
    logging.info("got chat_id")


@router.message(Command("help"))
async def cmd_help(message: Message):
    logging.info("help")
    msg = """/<b>my_id</b> - информация об id пользователя
/<b>chat_id</b> - информация о группе (идентификатор и название)
/<b>notify</b> - рассылка сообщений в заданные чаты (<i>только для доверенных пользователей</i>)
/<b>help</b> - получение справки по командам.
    """
    await message.answer(msg, parse_mode="HTML")

@router.message(Command("notify"))
async def cmd_notify(message: Message, editors: set[int], state: FSMContext):
    logging.info("notify")
    if message.from_user.id not in editors:
        await message.answer("У вас недостаточно прав для совершения этого действия 🧐")
    else:
        await message.answer("Напишите сообщение для рассылки ...")
        await state.set_state(Notification.edit)
        logging.info("State -> edit")


@router.message(Notification.edit)
async def edit_message(message: Message, state: FSMContext):
    logging.info(f"message: {message.text}")

    user_data[message.from_user.id] = message.md_text
    await message.reply(
        text="Выберите вариант действия:",
        reply_markup=get_send_cancel_kb(),
        # reply_markup=make_row_keyboard(action_names)
        # reply_markup=get_send_cancel_kb_fab(owner=message.from_user.id, text_msg=message.text)
    )
    await state.set_state(Notification.send)
    logging.info("State -> send")


@router.callback_query(F.data == "send_out")
async def send_confirm(callback: CallbackQuery, state: FSMContext):

    text = user_data.get(callback.from_user.id)
    logging.info(f"send_confirm {text=}")
    if text:
        await callback.answer("Отправляю!", show_alert=True, reply_markup=ReplyKeyboardRemove())
        try:
            await bot.send_message(-4067453977, text, parse_mode="MarkdownV2")
        except TelegramForbiddenError as e:
            logging.error(e.message)
        user_data[callback.from_user.id] = None
    else:
        await callback.answer("Upss! Nothing to send.", show_alert=True, reply_markup=ReplyKeyboardRemove())
    await state.set_state(Notification.edit)


@router.callback_query(F.data == "cancel")
async def send_cancel(callback: CallbackQuery, state: FSMContext):
    user_data.setdefault(callback.from_user.id, None)
    await callback.answer("Отменено!", show_alert=True)
    await state.set_state(Notification.edit)


@router.callback_query(F.data == "exit_notify")
async def exit_dialog(callback: CallbackQuery, state: FSMContext):
    user_data.setdefault(callback.from_user.id, None)
    await callback.answer("Выход!", show_alert=True)
    await state.set_state(Notification.exit)
