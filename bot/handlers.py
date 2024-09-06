import logging
import os
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, Command
from bot_init import bot
from bot.states import DocumentState
from app.gemini_api import generate_summary, answer_question
from app.config import settings
from app.users import add_user_to_redis, add_user_to_db, get_user_count_redis
import requests
import io
import pdfplumber



router = Router()


ADMINS = list(map(int, os.getenv("ADMINS").split(',')))  # Список ID администраторов


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Добавляем пользователя в Redis
    await add_user_to_redis(user_id)
    await message.answer("Привет, загрузи документ в формате PDF и я пришлю тебе summary!")
    await state.set_state(DocumentState.waiting_for_document)
    current_state = await state.get_state()
    logging.info(f"Current state after /start: {current_state}")


# Обработчик команды /stat
@router.message(Command("stat"))
async def get_bot_statistics(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.reply("У вас нет прав для выполнения этой команды.")
        return

    # Получаем количество пользователей через Redis
    user_count = await get_user_count_redis()

    # Ответ администратору
    await message.reply(f"Количество пользователей бота: {user_count}")


@router.message(F.document, StateFilter(DocumentState.waiting_for_document))
async def handle_document_upload(message: types.Message, state: FSMContext):
    logging.info("Document handler triggered.")

    # Проверим текущее состояние
    current_state = await state.get_state()
    logging.info(f"State in document handler: {current_state}")

    document = message.document
    logging.info(f"Document info: {document}")

    document = message.document
    logging.info(f"Document info: {document}")
    file_info = await bot.get_file(document.file_id)
    logging.info(f"File info: {file_info}")
    file_path = file_info.file_path
    file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'
    logging.info(f"File URL: {file_url}")
    file_data = requests.get(file_url).content

    try:
        with pdfplumber.open(io.BytesIO(file_data)) as pdf:
            document_text = ''.join([page.extract_text() for page in pdf.pages])
            logging.info(f"Extracted text: {document_text}")
    except Exception as e:
        await message.answer(f"Ошибка при обработке PDF: {e}")
        logging.error(f"Error during PDF processing: {e}")
        return

    summary = generate_summary(document_text)
    await state.update_data(document_summary=summary)
    await message.reply(f"Document summarized: {summary}")
    await state.set_state(DocumentState.document_uploaded)
    current_state = await state.get_state()
    logging.info(f"State after document upload: {current_state}")


@router.message(Command("reset"))
async def reset_document_context(message: types.Message, state: FSMContext):
    await state.clear()  # Сбрасываем все состояния
    await message.reply("Пожалуйста, загрузите новый документ!")
    await state.set_state(DocumentState.waiting_for_document)


@router.message(StateFilter(DocumentState.document_uploaded))
async def handle_question(message: types.Message, state: FSMContext):
    logging.info("Question handler triggered.")
    user_data = await state.get_data()
    document_summary = user_data.get('document_summary')

    question = message.text
    await message.reply(f"Your question: {question}. Processing...")
    try:
        answer = answer_question(document_summary, question)
        await message.reply(f"Answer: {answer}")
    except Exception as e:
        await message.reply(f"Error: {e}")





