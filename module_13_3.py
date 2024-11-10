import aiogram
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

API_TOKEN = '8178599573:AAEXyUs1WG3Hz56ZtF8t6cVKTu48o9XIiZA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message(Command('Calories'))
async def set_age(message: Message, state=FSMContext):
    await state.set_state(UserState.age)
    await message.answer('Введите ваш возраст')


@dp.message(UserState.age)
async def get_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(UserState.growth)
    await message.answer('Введите свой рост:')


@dp.message(UserState.growth)
async def get_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await state.set_state(UserState.weight)
    await message.answer('Введите свой вес:')


@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 88.362 + (13.397 * weight) + (4.799 * growth) - (5.677 * age)

    await message.answer(f'Ваша норма калорий:{calories} ')
    await state.clear()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет, я бот помогающий твоему здоровью")


@dp.message()
async def all_message(message: Message):
    await message.answer('Нажмите команду /start, чтобы начать общение')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
