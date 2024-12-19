from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from telegram.keyboards.tickets import ticket_new, ticket_options
from core.api import api
from storage.storage import storage, UserStorage
from lib.models.ticket import TicketOrigin
from lib.helper import CategoryOrigin
from lib.logger import logging as log

router = Router()

class Ticket(StatesGroup):
    user = State()
    category = State()
    content = State()

@router.callback_query(F.data.startswith(f"profile_"))
async def tickets_callbacks(c: types.CallbackQuery, state: FSMContext):
    data = c.data.split("_")[1:]
    action = data[0]
    match action:
        case "newticket":
            categories = api.get_categories()
            if categories:
                await c.message.answer("Новая заявка 🟢", reply_markup=ticket_new(categories))
        case _:
            await c.answer("Функция сейчас не работает")
    await c.answer() 

@router.callback_query(F.data.startswith(f"ticket_"))
async def tickets_callbacks(c: types.CallbackQuery, state: FSMContext):
    data = c.data.split("_")[1:]
    action = data[0]
    match action:
        case "category":
            # TODO
            cat_id = int(data[-1]) if data[-1].isdigit() else -1
            categories = api.get_categories()
            category_name = categories.get(cat_id).name if categories.get(cat_id) else "Без категории"
            if categories:
                await c.message.edit_text(f"Новая заявка 🟢 {category_name}\nНапишите обращение...", reply_markup=ticket_options())
                
                user: UserStorage = storage.get_user(c.from_user.id)
                await state.update_data(user=user)
                await state.update_data(category=categories.get(int(cat_id)))
                await state.update_data(message_id=c.message.message_id)
                await state.set_state(Ticket.content)
                
        case _:
            await c.answer("Функция сейчас не работает")
    await c.answer() 


@router.message(Ticket.content)
async def handle_ticket_content(message: types.Message, state: FSMContext):
    match message.text:
        case None:
            await state.set_state(Ticket.content)
            await message.answer("Ожидается текст")
        case _:
            data_by_context = await state.get_data()
            user: UserStorage = data_by_context.get("user")
            category: CategoryOrigin = data_by_context.get("category")
            new_ticket = TicketOrigin(
                name=message.text, content=message.text, status=1, 
                priority=3, waiting_duration=0, close_delay_stat=0,
                solve_delay_stat=0, takeintoaccount_delay_stat=0, users_id_recipient=user.id,
                sla_waiting_duration=0, itilcategories_id=category.id, 
                )
            log.debug(new_ticket)
            # api.create_ticket(new_ticket.model_dump())
            await message.answer("Заявка отправлена")

