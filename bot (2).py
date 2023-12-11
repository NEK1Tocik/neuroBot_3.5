import asyncio
import logging
import time
from asyncio import Lock
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from aiogram.types import InputFile
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from PIL import Image, ImageFont, ImageDraw

from main import prompt

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6701014079:AAFMdvjJ68op7f8h_ZjZzTRZYaL1A8qGwm0")
dp = Dispatcher(bot=bot, storage=MemoryStorage())

Base = declarative_base()
lock = Lock()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=True)

    def __init__(self, user_name):
        self.user_name = user_name

engine = create_engine("sqlite:///base.db")

session = scoped_session(sessionmaker(bind=engine))


@dp.message_handler(text='фото')
async def cmd_start(message: types.Message):
    photo = InputFile("r1.png")

    await message.answer_photo(photo=photo, caption='фото из интернета')
class Reg(StatesGroup):
    step1 = State()


class DB:
    answer_data = {}


@dp.message_handler(state=None)
async def start(message: types.Message):
   if message.text == '/start':
       if getIdByName(message.from_user.username) == 0:
           session.add(Users(message.from_user.username))
           session.commit()
           print('reg '+message.from_user.username)
           return await message.answer(message.from_user.username+", ты зарегистрирован!\nЗадавай мне свои вопросы :)")
       else: return await message.answer("Привет, "+message.from_user.username+", задавай мне свои вопросы :)")
   else:
       await message.answer_chat_action(action="typing")
       answer = prompt(message.text)
       return await message.answer(answer)


def getIdByName(name):
    info = session.query(Users).filter_by(user_name=name).distinct()
    shares = [x for x in info]
    if len(shares) == 0: return 0
    return shares[0]


@dp.message_handler(content_types='text', state=Reg.step1)
async def reg_step3(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer('Возраст не может содержать буквы!')
    async with lock:
        DB.answer_data['age'] = message.text
    await bot.send_message(message.from_user.id, text='Замечательный возраст!')
    await state.finish()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    asyncio.run(main())



