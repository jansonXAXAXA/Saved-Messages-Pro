import asyncio
import os
import logging
from dotenv import load_dotenv
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import urllib.parse

load_dotenv()
API_BASE_URL = "http://127.0.0.1:8000"
BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class BoardCreation(StatesGroup): waiting_for_name = State(); waiting_for_emoji = State()
class ItemSaving(StatesGroup): waiting_for_title = State()
class SearchState(StatesGroup): waiting_for_query = State()

async def api_request(method, url, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, f"{API_BASE_URL}{url}", **kwargs) as response:
            if 200 <= response.status < 300:
                try: return await response.json()
                except aiohttp.ContentTypeError: return {"ok": True}
            logging.error(f"API Error: {response.status} on {method} {url}")
            return None

async def generate_boards_menu(user_id: int, mode: str):
    boards = await api_request("get", f"/users/{user_id}/boards/")
    if not boards: return None
    builder = InlineKeyboardBuilder()
    for board in boards:
        action = "view_board" if mode == "view" else "delete_board"
        builder.add(InlineKeyboardButton(text=f"{board.get('emoji_icon', '📁')} {board['name']}", callback_data=f"{action}:{board['id']}"))
    builder.adjust(1)
    return builder.as_markup()

async def process_and_save_item(message: Message, final_item_data: dict):
    user_id = message.from_user.id
    item = await api_request("post", f"/users/{user_id}/items/", json=final_item_data)
    if not item: return await message.answer("❌ Не удалось сохранить элемент.")
    item_id = item['id']
    boards = await api_request("get", f"/users/{user_id}/boards/")
    if not boards: return await message.answer(f"✅ Сохранено в 'неотсортированное'.\nСоздайте доски, нажав '✨ Создать доску'")
    builder = InlineKeyboardBuilder()
    for board in boards:
        builder.add(InlineKeyboardButton(text=f"{board.get('emoji_icon', '📁')} {board['name']}", callback_data=f"move_item:{item_id}:{board['id']}"))
    builder.adjust(2)
    await message.answer("✅ Сохранено! Куда добавить?", reply_markup=builder.as_markup())

@dp.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    await state.clear()
    kb = [
        [KeyboardButton(text="🧐 Просмотр досок")],
        [KeyboardButton(text="✨ Создать доску"), KeyboardButton(text="✏️ Управление")],
        [KeyboardButton(text="🔍 Поиск")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await api_request("post", "/users/", json={"telegram_id": message.from_user.id, "username": message.from_user.username})
    await message.answer("Привет! Я твой архив идей. Используй кнопки ниже для навигации.", reply_markup=keyboard)

@dp.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено.")
    await handle_start(message, state)

@dp.message(F.text == "🧐 Просмотр досок")
async def show_boards_for_viewing(message: Message):
    markup = await generate_boards_menu(message.from_user.id, "view")
    if markup: await message.answer("Выберите доску для просмотра:", reply_markup=markup)
    else: await message.answer("У вас нет досок. Создайте первую, нажав '✨ Создать доску'")

@dp.message(F.text == "✨ Создать доску")
async def new_board_start(message: Message, state: FSMContext):
    await state.set_state(BoardCreation.waiting_for_name)
    await message.answer("Введите название для новой доски:", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text == "✏️ Управление")
async def show_boards_for_editing(message: Message):
    markup = await generate_boards_menu(message.from_user.id, "edit")
    if markup: await message.answer("Выберите доску для удаления:", reply_markup=markup)
    else: await message.answer("Нечего удалять.")

@dp.message(F.text == "🔍 Поиск")
async def search_start(message: Message, state: FSMContext):
    await state.set_state(SearchState.waiting_for_query)
    await message.answer("Что ищем?", reply_markup=types.ReplyKeyboardRemove())

@dp.message(SearchState.waiting_for_query)
async def process_search_query(message: Message, state: FSMContext):
    await state.clear()
    query = message.text.strip()
    if len(query) < 2:
        await message.answer("Введите минимум 2 символа для поиска.")
        await handle_start(message, state)
        return
    safe_query = urllib.parse.quote(query)
    results = await api_request("get", f"/users/{message.from_user.id}/search/?q={safe_query}")
    
    # СНАЧАЛА отправляем результаты или сообщение об их отсутствии
    if not results:
        await message.answer("Ничего не найдено.")
    else:
        builder = InlineKeyboardBuilder()
        for item in results:
            title = (item['title'][:40] + '..') if len(item['title']) > 40 else item['title']
            builder.add(InlineKeyboardButton(text=f"▪️ {title}", callback_data=f"show_item:{item['id']}"))
        builder.adjust(1)
        await message.answer("Результаты поиска:", reply_markup=builder.as_markup())
    
    # ПОТОМ возвращаем основную клавиатуру, но без приветствия
    kb = [
        [KeyboardButton(text="🧐 Просмотр досок")],
        [KeyboardButton(text="✨ Создать доску"), KeyboardButton(text="✏️ Управление")],
        [KeyboardButton(text="🔍 Поиск")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Главное меню:", reply_markup=keyboard)

@dp.message(BoardCreation.waiting_for_name)
async def process_board_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BoardCreation.waiting_for_emoji)
    await message.answer("Отлично! Теперь отправьте один эмодзи для иконки:")

@dp.message(BoardCreation.waiting_for_emoji)
async def process_board_emoji(message: Message, state: FSMContext):
    user_data = await state.get_data()
    payload = {"name": user_data['name'], "emoji_icon": message.text}
    await state.clear()
    new_board = await api_request("post", f"/users/{message.from_user.id}/boards/", json=payload)
    await handle_start(message, state)
    if new_board: await message.answer(f"✅ Доска '{message.text} {user_data['name']}' создана!")
    else: await message.answer("❌ Ошибка при создании доски.")

@dp.message(ItemSaving.waiting_for_title)
async def process_item_title(message: Message, state: FSMContext):
    user_data = await state.get_data()
    item_data = user_data['item_data']
    title = message.text if message.text != "." else item_data['title']
    final_item_data = {"item_type": item_data['item_type'], "title": title, "content": item_data['content']}
    await state.clear()
    await process_and_save_item(message, final_item_data)
    await handle_start(message, state)

@dp.message(StateFilter(None), F.photo | F.video | F.voice | F.document | F.video_note | F.location | F.text)
async def handle_any_content(message: Message, state: FSMContext):
    item_data = {}
    if message.text:
        if message.text in ["🧐 Просмотр досок", "✨ Создать доску", "✏️ Управление", "🔍 Поиск"]: return
        item_data = {'item_type': 'text', 'title': message.text[:50], 'content': message.text}
    elif message.photo: item_data = {'item_type': 'photo', 'title': "Фотография", 'content': message.photo[-1].file_id}
    elif message.video: item_data = {'item_type': 'video', 'title': f"Видео ({message.video.duration} сек.)", 'content': message.video.file_id}
    elif message.voice: item_data = {'item_type': 'voice', 'title': f"Голосовое ({message.voice.duration} сек.)", 'content': message.voice.file_id}
    elif message.document: item_data = {'item_type': 'document', 'title': f"Документ: {message.document.file_name}", 'content': message.document.file_id}
    elif message.video_note: item_data = {'item_type': 'video_note', 'title': "Видеосообщение", 'content': message.video_note.file_id}
    elif message.location: item_data = {'item_type': 'location', 'title': "Геометка", 'content': f"{message.location.latitude},{message.location.longitude}"}
    if not item_data: return
    await state.set_state(ItemSaving.waiting_for_title)
    await state.update_data(item_data=item_data)
    await message.answer(f"Принято! Введите название или отправьте '.', чтобы использовать: '{item_data['title']}'", reply_markup=types.ReplyKeyboardRemove())

@dp.callback_query(F.data.startswith("view_board:"))
async def cb_show_board_contents(callback: CallbackQuery):
    board_id = callback.data.split(":")[1]
    items = await api_request("get", f"/boards/{board_id}/items/")
    board_info = await api_request("get", f"/boards/{board_id}")
    board_name = board_info.get('name', '') if board_info else ''
    builder = InlineKeyboardBuilder()
    if not items: builder.add(InlineKeyboardButton(text="В этой доске пока пусто", callback_data="do_nothing"))
    else:
        for item in items:
            title = (item['title'][:40] + '..') if len(item['title']) > 40 else item['title']
            builder.add(InlineKeyboardButton(text=f"▪️ {title}", callback_data=f"manage_item:{item['id']}:{board_id}"))
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="⬅️ Назад к списку досок", callback_data="back_to_view_list"))
    await callback.message.edit_text(f"Содержимое доски «{board_name}»:", reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data.startswith("manage_item:"))
async def cb_manage_item(callback: CallbackQuery):
    _, item_id, board_id = callback.data.split(":")
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="➡️ Показать", callback_data=f"show_item:{item_id}"))
    builder.add(InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_item:{item_id}:{board_id}"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"view_board:{board_id}"))
    await callback.message.edit_text("Выберите действие:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("delete_item:"))
async def cb_delete_item(callback: CallbackQuery):
    _, item_id, board_id = callback.data.split(":")
    result = await api_request("delete", f"/items/{item_id}")
    if result and result.get("ok"):
        await callback.answer("✅ Элемент удален!", show_alert=True)
        callback.data = f"view_board:{board_id}"
        await cb_show_board_contents(callback)
    else: await callback.answer("❌ Ошибка при удалении.", show_alert=True)

@dp.callback_query(F.data == "back_to_view_list")
async def cb_back_to_boards(callback: CallbackQuery):
    markup = await generate_boards_menu(callback.from_user.id, "view")
    await callback.message.edit_text("Выберите доску для просмотра:", reply_markup=markup)
    await callback.answer()

@dp.callback_query(F.data.startswith("show_item:"))
async def cb_show_item(callback: CallbackQuery):
    item_id = callback.data.split(":")[1]
    item = await api_request("get", f"/items/{item_id}")
    if not item: return await callback.answer("Ошибка: не удалось найти этот элемент.", show_alert=True)
    chat_id, item_type, content = callback.message.chat.id, item['item_type'], item['content']
    if item_type == 'photo': await bot.send_photo(chat_id=chat_id, photo=content)
    elif item_type == 'video': await bot.send_video(chat_id=chat_id, video=content)
    elif item_type == 'voice': await bot.send_voice(chat_id=chat_id, voice=content)
    elif item_type == 'document': await bot.send_document(chat_id=chat_id, document=content)
    elif item_type == 'video_note': await bot.send_video_note(chat_id=chat_id, video_note=content)
    elif item_type == 'location':
        try:
            lat, lon = map(float, content.split(','))
            await bot.send_location(chat_id=chat_id, latitude=lat, longitude=lon)
        except (IndexError, ValueError): await bot.send_message(chat_id=chat_id, text=f"Не распознана геометка: {content}")
    else: await bot.send_message(chat_id=chat_id, text=content)
    await callback.answer()

@dp.callback_query(F.data.startswith("delete_board:"))
async def cb_confirm_delete_board(callback: CallbackQuery):
    board_id = callback.data.split(":")[1]
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🗑️ Да, удалить", callback_data=f"confirm_delete:{board_id}"))
    builder.add(InlineKeyboardButton(text="Отмена", callback_data="cancel_delete"))
    await callback.message.edit_text("Вы уверены?", reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data.startswith("confirm_delete:"))
async def cb_delete_board_confirmed(callback: CallbackQuery):
    board_id = callback.data.split(":")[1]
    result = await api_request("delete", f"/boards/{board_id}")
    if result and result.get("ok"): await callback.message.edit_text("✅ Доска удалена.")
    else: await callback.message.edit_text("❌ Ошибка при удалении.")
    await callback.answer()

@dp.callback_query(F.data == "cancel_delete")
async def cb_cancel_deletion(callback: CallbackQuery):
    await callback.message.edit_text("Удаление отменено.")
    await callback.answer()

@dp.callback_query(F.data.startswith("move_item:"))
async def cb_move_item(callback: CallbackQuery):
    _, item_id, board_id = callback.data.split(":")
    if await api_request("put", f"/items/{item_id}/move/{board_id}"):
        await callback.message.edit_text("✅ Готово! Элемент перемещен.")
    else: await callback.message.edit_text("❌ Ошибка! Не удалось переместить элемент.")
    await callback.answer()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())