from aiogram import Dispatcher
from handlers.commands.start import cmd_start
from handlers.commands.credentials import cmd_credentials, process_url, process_email, process_password
from handlers.states.CredentialsForm import CredentialsForm
from handlers.commands.sales import cmd_sales
from handlers.callbacks.update_sales import callback_update_sales
from handlers.callbacks.continue_credentials import callback_continue
from handlers.callbacks.sales import callback_sales
from handlers.commands.help import cmd_help


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_help, commands=['help'])
    dp.register_message_handler(cmd_credentials, commands=['credentials'])
    dp.register_message_handler(cmd_sales, commands=['sales'])
    dp.register_message_handler(process_url, state=CredentialsForm.url)
    dp.register_message_handler(process_email, state=CredentialsForm.email)
    dp.register_message_handler(process_password, state=CredentialsForm.password)
    dp.register_callback_query_handler(callback_update_sales, lambda c: c.data == "update")
    dp.register_callback_query_handler(callback_continue, lambda c: c.data == "continue")
    dp.register_callback_query_handler(callback_sales, lambda c: c.data == "sales")
