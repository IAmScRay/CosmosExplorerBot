import math

import data_fetcher
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler


fetcher = data_fetcher.DataFetcher()
validators = fetcher.sorted_by_votes()
pages = 0
offset = 4

if len(validators) % 5 == 0:
    pages = math.floor(len(validators) / 5)
else:
    pages = math.floor(len(validators) / 5) + 1


def get_page(page: int):
    if page == 1:
        result = validators[page * offset - offset + (page - 1):page + offset:]
    else:
        result = validators[page * offset - offset + (page - 1):page * offset + page:]

    return result


def get_validator_buttons(page: int):
    validator_buttons = []

    pos = 1 + (page * offset - offset + (page - 1))
    for value in get_page(page):
        val_list = []

        text = f"{pos}: {value[1].get_moniker()}"
        val_list.append(
            InlineKeyboardButton(
                text,
                callback_data=f"{value[1].get_moniker()}"
            )
        )

        validator_buttons.append(val_list)

        pos += 1

    page_buttons = []
    if page == 1:
        page_buttons.append(
            InlineKeyboardButton(
                "▶",
                callback_data=f"{page + 1}"
            )
        )
    elif page == pages:
        page_buttons.append(
            InlineKeyboardButton(
                "◀",
                callback_data=f"{page - 1}"
            )
        )
    else:
        page_buttons.append(
            InlineKeyboardButton(
                "◀",
                callback_data=f"{page - 1}"
            )
        )
        page_buttons.append(
            InlineKeyboardButton(
                "▶",
                callback_data=f"{page + 1}"
            )
        )
    validator_buttons.append(page_buttons)
    return validator_buttons


def create_page_markup(page: int):
    return InlineKeyboardMarkup(
        get_validator_buttons(page)
    )


BACK_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("Back", callback_data="Back")]
])


def main_menu_text():
    result = f"Chain ID: <b>{fetcher.get_chain_id()}</b>\n\n"
    result += f"Active validators: <b>{len(fetcher.get_active_set())}/{fetcher.get_max_active_set()}</b>\n"
    result += f"Current block: <b>{fetcher.get_block_height()}</b>"

    return result


def menu(update: Update, context: CallbackContext) -> None:
    """
    This handler sends a menu with the inline buttons we pre-assigned above
    """

    context.bot.send_message(
        update.message.from_user.id,
        main_menu_text(),
        parse_mode=ParseMode.HTML,
        reply_markup=create_page_markup(1)
    )


def start(update: Update, context: CallbackContext) -> None:

    context.bot.send_message(
        update.message.from_user.id,
        "Welcome to Cosmos Monitoring Bot!\n\nUse <b>/menu</b> command to display the menu!",
        parse_mode=ParseMode.HTML
    )


def button_tap(update: Update, context: CallbackContext) -> None:
    """
    This handler processes the inline buttons on the menu
    """

    fetcher.update()

    data = update.callback_query.data
    if data == "Back":
        text = main_menu_text()
        markup = create_page_markup(1)
    elif data.isnumeric():
        text = main_menu_text()
        markup = create_page_markup(int(data))
    else:
        validator = fetcher.get_by_moniker(data)

        text = f"<b>Moniker</b>: {data}\n\n"
        text += f"<b>Address</b>: {validator.get_operator_address()}\n\n"
        text += f"<b>Description</b>: {validator.get_details()}\n\n"
        text += f"Commission: <b>{validator.get_commission()}%</b>\n"
        text += f"Maximum commission: <b>{validator.get_max_commission()}%</b>\n"
        text += f"Commission change rate: <b>{validator.get_change_rate()}</b>\n\n"
        text += f"Last time validator updated the commission: <b>{validator.get_last_commission_update()}</b>\n\n"

        if not (validator.get_website() == ""):
            text += f"<b>Website</b>: {validator.get_website()}"

        markup = BACK_MARKUP

    update.callback_query.answer()

    update.callback_query.message.edit_text(
        text,
        ParseMode.HTML,
        reply_markup=markup,
        disable_web_page_preview=True
    )


def main() -> None:
    updater = Updater("YOUR_TOKEN")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("menu", menu))
    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CallbackQueryHandler(button_tap))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
