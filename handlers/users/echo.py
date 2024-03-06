from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp,bot
from states import st
from data import config as cfg
from keyboards import ik,kb
from handlers.sender_handlers import sender
from handlers.users import misc as ms
from utils.db_api import database as db

@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    if message.chat.type != 'private':
        return
    match message.text:
        case "💬 Начать общаться":
            db.clear_chat(message.from_user.id)
            image = "https://assets.ithillel.ua/images/blog/cover/_transform_blogSplash_desktop_2x/Hillel-Blog-ChatGPT.jpg"
            await message.answer_photo(photo=image,caption="<b>👻Привет, я Chat-GPT.</b>\n\n"
                                 "✏️Задай свой вопрос!\n\n"
                                "",reply_markup=kb.chat)
            await st.UserState.chat.set()
            return
        case "👻 Сгенерировать картинку":
            image = "https://threwthelookingglass.com/wp-content/uploads/2022/12/Midjourney-Bot-Commands.png"
            await message.answer_photo(photo=image,caption="<b>👨‍🎨Привет, я Да Винчи!</b>\n\n"
                                 "Введи описание, а я нарисую по нему картину ✏️\n\n"
                                 "",reply_markup=kb.image_generate)
            await st.UserState.draw.set()
            return
        case "Midjourney":
            image = "https://threwthelookingglass.com/wp-content/uploads/2022/12/Midjourney-Bot-Commands.png"
            await message.answer_photo(photo=image, caption="<b>👨‍🎨Привет, я MidJourney.</b>\n\n"
                                                            "✏️Введи описание, а я нарисую по нему картину!✏️\n\n"
                                                            "❌Чтобы выйти из чата введите /close.",
                                       reply_markup=kb.image_generate)
            await st.UserState.midjourney.set()
        case "😈 Midjourney":
            await message.answer_photo(caption="""
Дорогие пользователи *Chat GPT!*

*Вы также можете бесплатно использовать наш* [Midjourney](https://t.me/Pro_Midjourney_bot)

_С уважением, @iwrestledabearonse 💜_""",photo="https://imgur.com/a/TFYmarv",parse_mode='Markdown',
                                       reply_markup=ik.use_new_bot)
            return

        case "😈 Наши проекты":
            stick = 'CAACAgIAAxkBAAEJnCBkpp52rpoAAVhxJjjz_qJc_vrE35QAAmsDAAJtsEIDAcazH9xI-xovBA'
            await bot.send_sticker(message.from_user.id,sticker=stick)
            await message.answer('Список других наших проектов:', reply_markup=ik.projects())
            return
    if str(message.from_user.id) in cfg.ADMINS:
        match message.text:
            case 'Админ':
                await message.answer("Админ меню",reply_markup=kb.admin)
                return 
            case "💬Рассылка":
                await message.answer("Пришлите мне сообщение, которое будет разослано пользователям")
                await st.UserState.sender.set()
                return
            case "📊Статистика":
                await message.answer(ms.admin_stat_text())
                return
            case "🔃Выгрузить дб":
                document = ms.get_ids_files()
                await message.answer_document(document=document,
                                              caption="Файл с ID пользователей")
                return
            case "👥Управление каналами":
                await message.answer("<b>Ваши каналы:</b>",reply_markup=ik.admin_adv_chats())
                return
            case "🗑Удалить мертвых пользователей":
                await message.answer('Пришлите .txt файл с ID пользователей, которых нужно удалить из дб',reply_markup=ik.off_state)
                await st.UserState.delete_users.set()
                return
            case "📄Мои проекты":
                await message.answer("Список:", reply_markup=ik.admin_projects())
                return
    await message.answer("Введите /start, а после воспользуйтесь меню")