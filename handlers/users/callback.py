from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from handlers.users import misc as ms, lt
from loader import dp
from keyboards import ik, kb
from aiogram.dispatcher import FSMContext
from states import st
from utils.db_api import database as db


@dp.callback_query_handler(state="*")
async def main(call: types.CallbackQuery, state: FSMContext):
    params = call.data.split("-")
    match params[0]:
        case 'off_state':
            await state.finish()
            await call.message.answer("❌Действие отменено")
        case "im_subscribed":
            sub_status = await ms.check_subscribes(call.from_user.id)
            if sub_status:
                await call.message.edit_text("Спасибо за поддержку нашего проекта!\n"
                                             "<b>Благодаря Вам бот остается бесплатным!</b>\n"
                                             "")
            else:
                await call.answer("☹️Вы не подписаны на один из каналов")
        case "start_chatting":
            await call.message.delete()
            await call.message.answer("<b>Привет, я ChatGPT.</b> Задай свой вопрос.\n\n"
                                      "Чтобы выйти из чата введите /close")
            await st.UserState.chat.set()
        case "send":
            await call.message.delete()
            message_id = int(params[1])
            data = await state.get_data()
            await state.finish()
            if len(data) != 0:
                name = data['name']
                url = data['url']
            else:
                name = "0"
                url = "0"
            from_chat_id = call.from_user.id
            await call.message.answer("Рассылка запущена")
            await ms.sender(message_id, from_chat_id, name, url)
        case 'add_button_to_send':
            message_id = int(params[1])
            await call.message.answer("Введите ссылку кнопки", reply_markup=ik.off_state)
            await st.UserState.add_btn_url.set()
            await state.update_data(message_id=message_id)

        case "st":
            url = str(call.data.split("*")[1])
            match params[1]:
                case "add_projects":
                    await call.message.delete()
                    await call.message.answer("Введите ccылку", reply_markup=ik.off_state)
                    await st.Add_projects.c_url.set()
                case "parse_projects":
                    await call.message.delete()
                    await call.message.answer(lt.adv_projects(url), reply_markup=ik.admin_delete_projects(url))

                case "delete":
                    db.delete_adv_projects(url)
                    await call.message.delete()
                    await call.message.answer("✅Чат удален")

        case "chat_manage":
            chat_id = int(call.data.split("*")[1])
            match params[1]:
                case 'add_channel':
                    await call.message.delete()
                    await call.message.answer("Введите ID канала", reply_markup=ik.off_state)
                    await st.Add_Channel.c_id.set()
                case 'show':
                    await call.message.delete()
                    await call.message.answer(lt.adv_chat_stat(chat_id), reply_markup=ik.admin_delete_adv_chat(chat_id))
                case 'delete':
                    db.delete_adv_chat(chat_id)
                    await call.message.delete()
                    await call.message.answer("✅Чат удален")
