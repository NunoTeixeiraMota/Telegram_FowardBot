from telegram import Update, ChatMemberUpdated
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ChatMemberHandler
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG level for more detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

TOKEN = ""
TARGET_GROUP_ID = ""
YOUR_USER_ID = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"Start command received from user {user.id} ({user.first_name})")
    await update.message.reply_text('Hi! I am your message forwarding bot. Send me any message or photo and I will forward it to the group.')

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"Message received from user {user.id} ({user.first_name})")

    if str(user.id) != YOUR_USER_ID:
        logger.warning(f"Unauthorized message attempt from user {user.id} ({user.first_name})")
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return

    try:
        if update.message.photo:
            photo = update.message.photo[-1]
            logger.info(f"Forwarding photo from user {user.id} with file_id: {photo.file_id}")
            await context.bot.send_photo(
                chat_id=TARGET_GROUP_ID,
                photo=photo.file_id,
                caption=update.message.caption
            )
        elif update.message.document and update.message.document.mime_type.startswith("image/"):
            logger.info(f"Forwarding document-type image from user {user.id} with file_id: {update.message.document.file_id}")
            await context.bot.send_photo(
                chat_id=TARGET_GROUP_ID,
                photo=update.message.document.file_id,
                caption=update.message.caption
            )
        else:
            logger.info(f"Forwarding text message from user {user.id}: {update.message.text[:50]}...")
            await context.bot.send_message(
                chat_id=TARGET_GROUP_ID,
                text=update.message.text
            )
        
        logger.info(f"Message successfully forwarded to group {TARGET_GROUP_ID}")
        await update.message.reply_text("Message forwarded successfully!")
    except Exception as e:
        logger.error(f"Error forwarding message from user {user.id}: {str(e)}")
        await update.message.reply_text(f"Error forwarding message: {str(e)}")

async def handle_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle chat member updates."""
    logger.debug(f"Received member update: {update.chat_member}")
    
    # Log the full update object for debugging
    logger.debug(f"Full update object: {update}")
    
    try:
        chat_member: ChatMemberUpdated = update.chat_member
        
        # Log the change in member status
        logger.debug(f"Member status change - Old: {chat_member.old_chat_member.status}, New: {chat_member.new_chat_member.status}")
        
        # Check various joining conditions
        is_join = (
            chat_member.old_chat_member.status in ['left', 'restricted', 'kicked'] and
            chat_member.new_chat_member.status in ['member', 'administrator']
        )
        
        if is_join:
            new_member = chat_member.new_chat_member.user
            logger.info(f"New member joined: {new_member.id} ({new_member.first_name})")
            
            welcome_message = (
                f"🟢 Bem-vindo ao ApostaInteligente {new_member.first_name}! 🟢\n\n"
                "Aqui, estratégia e análise se unem para transformar apostas em oportunidades. 🎯💰\n\n"
                "📊 Dicas de valor\n"
                "📈 Análises detalhadas\n"
                "🔥 Palpites assertivos\n\n"
                "💡 Jogue com inteligência, aposte com responsabilidade!\n\n"
                "Participe, interaja e aproveite o melhor do mundo das apostas esportivas. Vamos lucrar juntos! 🚀🔥"
            )
            
            try:
                # Try to send private message
                await context.bot.send_message(
                    chat_id=new_member.id,
                    text=welcome_message
                )
                logger.info(f"Welcome message sent to user {new_member.id}")
                
            except Exception as e:
                logger.error(f"Failed to send welcome message to user {new_member.id}: {str(e)}")
        else:
            logger.debug("Member update did not match joining conditions")
            
    except Exception as e:
        logger.error(f"Error in handle_member_update: {str(e)}")
        logger.exception(e)  # This will log the full traceback

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.error(f"Update {update} caused error {context.error}")
    logger.exception(context.error)  # This will log the full traceback

def main():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Set up daily rotating log file
    log_filename = f"logs/bot_log_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    logger.info("Bot starting up...")
    
    try:
        application = Application.builder().token(TOKEN).build()
        
        # Command handlers
        application.add_handler(CommandHandler("start", start))
        
        # Message handlers
        application.add_handler(MessageHandler(
            (filters.TEXT | filters.PHOTO) & ~filters.COMMAND, 
            forward_message
        ))
        
        # Add handler for new chat members with high priority
        application.add_handler(
            ChatMemberHandler(handle_member_update, ChatMemberHandler.CHAT_MEMBER),
            group=1
        )

        # Error handler
        application.add_error_handler(error_handler)

        logger.info("Bot handlers configured, starting polling...")
        print("Bot is running...")
        
        # Get bot information
        async def print_bot_info():
            bot = application.bot
            bot_info = await bot.get_me()
            logger.info(f"Bot Username: @{bot_info.username}")
            logger.info(f"Bot ID: {bot_info.id}")
            
            try:
                chat = await bot.get_chat(TARGET_GROUP_ID)
                logger.info(f"Target group title: {chat.title}")
                bot_member = await chat.get_member(bot_info.id)
                logger.info(f"Bot permissions in group: {bot_member.status}")
            except Exception as e:
                logger.error(f"Error getting group info: {e}")
        
        # Run the bot info check
        import asyncio
        asyncio.get_event_loop().run_until_complete(print_bot_info())
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        logger.exception(e)

if __name__ == '__main__':
    main()
