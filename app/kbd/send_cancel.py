from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# from app.handlers.notify import EditAnswersCallbackFactory


def get_send_cancel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Отправить", callback_data="send_out")
    kb.button(text="Отменить", callback_data="cancel")
    kb.button(text="Выйти", callback_data="exit_notify")
    return kb.as_markup()


# def get_send_cancel_kb_fab(owner: int, text_msg: str):
#     builder = InlineKeyboardBuilder()
#     builder.button(
#         text="Отправить", callback_data=EditAnswersCallbackFactory(action="Отправить", owner=owner, text_msg=text_msg)
#     )
#     builder.button(
#         text="Отменить", callback_data=EditAnswersCallbackFactory(action="Отменить", owner=owner, text_msg=text_msg)
#     )
#     builder.button(
#         text="Выйти", callback_data=EditAnswersCallbackFactory(action="Выйти", owner=owner, text_msg=text_msg)
#     )
#
#     # Выравниваем кнопки по 3 в ряд
#     builder.adjust(3)
#     return builder.as_markup()
