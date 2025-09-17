import logging
from pyrogram import Client, emoji, filters
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument, InlineQuery
from database.ia_filterdb import get_search_results
from utils import is_req_subscribed, get_size, temp
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
from database.connections_mdb import active_connection
from database.users_chats_db import db

logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME

async def inline_users(query: InlineQuery):
    if AUTH_USERS:
        if query.from_user and query.from_user.id in AUTH_USERS:
            return True
        else:
            return False
    if query.from_user and query.from_user.id not in temp.BANNED_USERS:
        return True
    return False

@Client.on_inline_query()
async def answer(bot, query):
    """Show search results for given inline query"""
    chat_id = await active_connection(str(query.from_user.id))
    
    if not await inline_users(query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='okDa',
                           switch_pm_parameter="hehe")
        return

    if AUTH_CHANNEL and not await is_req_subscribed(bot, query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='You have to subscribe my channel to use the bot',
                           switch_pm_parameter="subscribe")
        return

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    
    # Check if FTM Gamma Mode is enabled and if query is from a group
    bot_id = bot.me.id
    gamma_mode_enabled = False
    try:
        gamma_mode_enabled = await db.gamma_mode_status(bot_id)
        # Only enable gamma mode features for group searches
        if gamma_mode_enabled and hasattr(query, 'chat_type'):
            from pyrogram import enums
            if query.chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                gamma_mode_enabled = False
    except Exception as e:
        logger.error(f"Error checking gamma mode status: {e}")
        gamma_mode_enabled = False
    
    reply_markup = get_reply_markup(query=string, gamma_mode=gamma_mode_enabled)
    files, next_offset, total = await get_search_results(
                                                  chat_id,
                                                  string,
                                                  file_type=file_type,
                                                  max_results=10,
                                                  offset=offset)

    for file in files:
        title=file.file_name
        size=get_size(file.file_size)
        f_caption=file.caption
        
        if gamma_mode_enabled:
            # Enhanced gamma mode formatting - matching screenshot format
            user_full_name = f"{query.from_user.first_name}"
            if query.from_user.last_name:
                user_full_name += f" {query.from_user.last_name}"
            
            # HTML escape user inputs to prevent formatting issues
            user_full_name = user_full_name.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            string_escaped = string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            title_escaped = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            f_caption = f"Hey 👋🏻 <b>Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ</b> 😍\n\n{user_full_name}\n\nHey 👋🏻 <b>Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ</b> 😍\n\n📝 <b>Title :</b> {string_escaped}\n📫 <b>Your File is Ready Below</b> 👇\n\n{title_escaped}"
        else:
            # Standard formatting with fallback
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption = f"{title}" if title else f"{file.file_name}"
            else:
                f_caption = f"{title}" if title else f"{file.file_name}"
        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                document_file_id=file.file_id,
                caption=f_caption,
                description=f'Size: {get_size(file.file_size)}\nType: {file.file_type}',
                reply_markup=reply_markup))

    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} Results - {total}"
        if string:
            switch_pm_text += f" for {string}"
        try:
            await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))
    else:
        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'

        await query.answer(results=[],
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")


def get_reply_markup(query, gamma_mode=False):
    buttons = []
    
    if gamma_mode:
        # FTM Gamma Mode - Enhanced buttons
        buttons.extend([
            [
                InlineKeyboardButton('✚ Add Me To Your Group 🤖', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],
            [
                InlineKeyboardButton('🔍 Search again', switch_inline_query_current_chat=query)
            ]
        ])
    else:
        # Standard mode
        buttons = [
            [
                InlineKeyboardButton('🔍 Search again', switch_inline_query_current_chat=query)
            ]
        ]
    
    return InlineKeyboardMarkup(buttons)


