from aiogram import Dispatcher
from handlers.commands.start import cmd_start
from handlers.states.SalesForm import SalesForm
from handlers.commands.credentials import cmd_credentials, process_url, process_email, process_password
from handlers.states.CredentialsForm import CredentialsForm
from handlers.commands.sales import cmd_sales
from handlers.commands.sales_range import process_from_date
from handlers.commands.sales_range import process_to_date
from handlers.callbacks.update_sales import callback_update_sales
from handlers.callbacks.continue_credentials import callback_continue
from handlers.callbacks.sales import callback_sales
from handlers.callbacks.predict import callback_predict
from handlers.states.PredictForm import PredictForm
from handlers.callbacks.sales_data import callback_sales_data
from handlers.commands.unique_visitors import process_unique_visitors
from handlers.callbacks.sales_range import callback_sales_range
from handlers.callbacks.sales_last_month import callback_sales_last_month
from handlers.callbacks.fix_credentials import callback_fix_credentials
from handlers.callbacks.to_excel import callback_to_excel
from handlers.callbacks.sales_today import callback_sales_today
from handlers.callbacks.full_scan import callback_full_scan
from handlers.callbacks.brief_scan import callback_brief_scan
from handlers.commands.help import cmd_help


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_help, commands=['help'])
    dp.register_message_handler(cmd_credentials, commands=['credentials'])
    dp.register_message_handler(cmd_sales, commands=['sales'])
    dp.register_message_handler(process_url, state=CredentialsForm.url)
    dp.register_message_handler(process_email, state=CredentialsForm.email)
    dp.register_message_handler(process_password, state=CredentialsForm.password)
    dp.register_message_handler(process_from_date, state=SalesForm.from_date)
    dp.register_message_handler(process_to_date, state=SalesForm.to_date)
    dp.register_message_handler(process_unique_visitors, state=PredictForm.unique_visitors)
    dp.register_callback_query_handler(callback_update_sales, lambda c: c.data == "update")
    dp.register_callback_query_handler(callback_continue, lambda c: c.data == "continue")
    dp.register_callback_query_handler(callback_sales, lambda c: c.data == "menu")
    dp.register_callback_query_handler(callback_predict, lambda c: c.data == "predict")
    dp.register_callback_query_handler(callback_sales_data, lambda c: c.data == "sales_data")
    dp.register_callback_query_handler(callback_sales_range, lambda c: c.data == "sales_range")
    dp.register_callback_query_handler(callback_sales_today, lambda c: c.data == "sales_day")
    dp.register_callback_query_handler(callback_sales_last_month, lambda c: c.data == "sales_month")
    dp.register_callback_query_handler(callback_fix_credentials, lambda c: c.data == "fix_credentials")
    dp.register_callback_query_handler(callback_brief_scan, lambda c: c.data == "brief_scan")
    dp.register_callback_query_handler(callback_full_scan, lambda c: c.data == "full_scan")
    dp.register_callback_query_handler(callback_to_excel, lambda c: c.data == "to_excel")
