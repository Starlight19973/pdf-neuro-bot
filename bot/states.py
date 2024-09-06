from aiogram.fsm.state import StatesGroup, State


class DocumentState(StatesGroup):
    waiting_for_document = State()
    document_uploaded = State()