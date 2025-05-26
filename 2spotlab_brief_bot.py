
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging

API_TOKEN = '8149514714:AAEJWG3pJ-AMoEw7VmrAMV-ZOITC6A50u4o' 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class BriefForm(StatesGroup):
    company = State()
    contact = State()
    project = State()
    goal = State()
    audience = State()
    services = State()
    budget = State()
    deadline = State()
    references = State()
    values = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer("Привет! Мы — SpotLab. Заполни мини-бриф, это займёт 3–5 минут. Как называется твоя компания?")
    await BriefForm.company.set()

@dp.message_handler(state=BriefForm.company)
async def step_company(message: types.Message, state: FSMContext):
    await state.update_data(company=message.text)
    await message.answer("Кто контактное лицо? Имя, должность и как связаться.")
    await BriefForm.next()

@dp.message_handler(state=BriefForm.contact)
async def step_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer("Что продвигаем?")
    await BriefForm.next()

@dp.message_handler(state=BriefForm.project)
async def step_project(message: types.Message, state: FSMContext):
    await state.update_data(project=message.text)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Увеличить продажи", "Запустить продукт", "Строить бренд")
    markup.add("Привлечь подписчиков", "Личный бренд", "Другое")
    await message.answer("Какая цель проекта?", reply_markup=markup)
    await BriefForm.next()

@dp.message_handler(state=BriefForm.goal)
async def step_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer("Кто ваша ЦА?", reply_markup=types.ReplyKeyboardRemove())
    await BriefForm.next()

@dp.message_handler(state=BriefForm.audience)
async def step_audience(message: types.Message, state: FSMContext):
    await state.update_data(audience=message.text)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Коммуникации и PR", "Маркетинг и стратегия")
    markup.add("SMM и продвижение", "Инфлюенс-маркетинг")
    markup.add("Видеопродакшн", "Анимация", "Пока не определились")
    await message.answer("Что пригодится из наших направлений?", reply_markup=markup)
    await BriefForm.next()

@dp.message_handler(state=BriefForm.services)
async def step_services(message: types.Message, state: FSMContext):
    await state.update_data(services=message.text)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("До 100 000 ₽", "100 000 – 300 000 ₽", "300 000 – 700 000 ₽", "700 000+ ₽", "Не определились")
    await message.answer("Какой бюджет?", reply_markup=markup)
    await BriefForm.next()

@dp.message_handler(state=BriefForm.budget)
async def step_budget(message: types.Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await message.answer("Какие сроки и дедлайн?", reply_markup=types.ReplyKeyboardRemove())
    await BriefForm.next()

@dp.message_handler(state=BriefForm.deadline)
async def step_deadline(message: types.Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    await message.answer("Есть ли у тебя референсы или примеры?")
    await BriefForm.next()

@dp.message_handler(state=BriefForm.references)
async def step_references(message: types.Message, state: FSMContext):
    await state.update_data(references=message.text)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Скорость", "Креатив", "Глубокая стратегия")
    markup.add("Прозрачность", "Цена/качество", "Другое (напишу сам)")
    await message.answer("Что важно в работе с агентством?", reply_markup=markup)
    await BriefForm.next()


@dp.message_handler(state=BriefForm.values)
async def step_values(message: types.Message, state: FSMContext):
    await state.update_data(values=message.text)
    data = await state.get_data()
    summary = "\n".join([f"{k.capitalize()}: {v}" for k, v in data.items()])

  
    await message.answer(
        f"Спасибо! Вот кратко о тебе:\n\n{summary}\n\n"
        f"Мы свяжемся с тобой в ближайшее время. Или напиши: @SpotLabADV",
        reply_markup=types.ReplyKeyboardRemove()
    )

    
    CHAT_ID = -1002633703555
    await bot.send_message(CHAT_ID, f"📥 Новый бриф!\n\n{summary}")

    await state.finish()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
