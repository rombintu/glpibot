from aiogram.utils.keyboard import InlineKeyboardBuilder as ikbuilder

btns = {
    "profile": {
        "newticket": "Новая заявка ✉️",
        "mytickets": "Мои открытые заявки 📫",
        "worktickets": "Назначенные на меня 🛠"
    },
}

def user_config(telegram_id: int):
    builder = ikbuilder()
    for action, ru in btns["profile"].items():
        builder.button(
            text=ru, 
            callback_data=f"profile_{action}_{telegram_id}")
    builder.adjust(1, 1)
    return builder.as_markup()