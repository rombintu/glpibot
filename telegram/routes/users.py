from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from storage.storage import InMemStorage
from core.postapi import postapi
from core.api import api
from random import randint
from lib.models.user import EMAIL_SUFFIX_ATCONSULTING, UserStorage, UserOrigin
from telegram.keyboards import user as kbuser
from lib.helper import isEnglish

router = Router()
storage = InMemStorage()

def isreg(func):
    async def wrapper(message: types.Message):
        if storage.get_user(message.chat.id):
            await func(message)
        else:
            await message.answer("Пройдите авторизацию /auth")
    return wrapper

@router.message(Command('auth'))
async def handle_command_auth(message: types.Message, state: FSMContext):
    await state.set_state(Auth.login)
    await message.answer("Для авторизации введите логин от учетной записи Phoenixit")


@router.message(Command('profile'))
@isreg
async def handle_command_profile(message: types.Message):
    user = storage.get_user(message.chat.id)
    await message.answer(f"""👨‍💻 <b>{user.realname} {user.firstname}</b>
📨 {user.get_email_atconsulting()}
🆔 <code>{user.telegram_id}</code> ☎️ {user.phone}""", 
parse_mode=ParseMode.HTML, reply_markup=kbuser.user_config(message.chat.id))


class Auth(StatesGroup):
    login = State()
    user = State()
    code = State()

@router.message(Auth.login)
async def handle_client_login(message: types.Message, state: FSMContext):
    match message.text:
        case "/cancel":
            await message.answer("Отмена операции")
            await state.clear()
        case None:
            await state.set_state(Auth.login)
            await message.answer("Ожидается логин at-consulting\n/cancel - Отмена")
        case _:
            login = message.text.strip()
            if not isEnglish(login):
                await message.answer("Неправильный формат. Отмена операции")
                await state.clear()
                return
            
            users: list[UserOrigin] = api.get_users()
            founded_user = None
            for user in users:
                if user.name == login:
                    founded_user = user
                    break
            if not founded_user:
                await message.answer("Вы не зарегистрированы в системе. Отмена операции")
                await state.clear()
                return
            
            await state.update_data(user=founded_user)

            email_to = login + EMAIL_SUFFIX_ATCONSULTING
            await state.update_data(login=login)
            await state.set_state(Auth.code)
            code = randint(100000, 999999)
            await state.update_data(code=code)

            post_message = postapi.build_postmail_message(
            "Авторизация в системе Cloudesk", f"Код авторизации: <b>{code}</b><br><br><br>Сообщение сгенерировано автоматически",
            email_to, postapi.smtp_sender, True)
            error = postapi.send_email(email_to, post_message, postapi.smtp_sender)
            if error:
                await message.answer(error)
                return
            await message.answer(f"Введите код, который пришел вам на почту {email_to}")

@router.message(Auth.code)
async def handle_client_code(message: types.Message, state: FSMContext):
    match message.text:
        case "/cancel":
            await message.answer("Отмена операции")
            await state.clear()
        case None:
            await state.set_state(Auth.code)
            await message.answer("Ожидается код с почты\n/cancel - Отмена")
        case _:
            data_by_context = await state.get_data()
            if str(data_by_context.get("code")) == message.text:
                user: UserOrigin = data_by_context.get("user")
                if user:
                    userTelegram = UserStorage(**user.model_dump(), telegram_id=message.chat.id)
                    storage.add_user(userTelegram)
                    await message.answer("Авторизация прошла успешно ✅")
                else:
                    await message.answer("Авторизация не прошла, обратитесь к администратору")
            else:
                await message.answer("Авторизация не прошла, обратитесь к администратору")
