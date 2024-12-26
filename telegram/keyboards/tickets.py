from aiogram.utils.keyboard import InlineKeyboardBuilder as ikbuilder

from lib.helper import CategoryOrigin

btns = {
    "options": {
        "push": "Отправить",
        "cancel": "Отменить"
    }
}

def ticket_new(categories: dict[int, CategoryOrigin]):
    builder = ikbuilder()
    for idc, c in categories.items():
        builder.button(
            text=c.name, 
            callback_data=f"ticket_category_{c.id}")
    builder.adjust(1, 1)
    return builder.as_markup()

def ticket_options(push=False):
    builder = ikbuilder()
    for action, ru in btns["options"].items():
        if not push and action == "push":
            continue
        builder.button(
            text=ru, 
            callback_data=f"ticket_{action}")
    builder.adjust(1, 1)
    return builder.as_markup()