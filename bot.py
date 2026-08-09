import nest_asyncio
nest_asyncio.apply()

import json
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = 8051030380

MOVIES_FILE = "movies.json"

if os.path.exists(MOVIES_FILE):
    with open(MOVIES_FILE, "r") as f:
        movies = json.load(f)
else:
    movies = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Salom!\n\n"
        "Kino kodini yuboring.\n"
        "Masalan: 7"
    )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "❌ Siz kino qo‘sha olmaysiz."
        )
        return

    context.user_data["video_id"] = update.message.video.file_id

    await update.message.reply_text(
        "✅ Video qabul qilindi!\n"
        "Endi kino kodini yuboring. Masalan: 7"
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()

    # Admin yangi kino qo‘shmoqda
    if (
        update.effective_user.id == ADMIN_ID
        and "video_id" in context.user_data
    ):
        movies[code] = context.user_data.pop("video_id")

        with open(MOVIES_FILE, "w") as f:
            json.dump(movies, f)

        await update.message.reply_text(
            f"✅ Kino {code} kodi bilan saqlandi!"
        )
        return

    # Foydalanuvchi kino kodini yubormoqda
    if code in movies:
        await update.message.reply_video(
            video=movies[code],
            caption=f"🎬 Kino kodi: {code}"
        )
    else:
        await update.message.reply_text(
            "❌ Bu koddagi kino topilmadi."
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.VIDEO, handle_video)
)
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text
    )
)

print("Bot ishga tushdi...")
app.run_polling(close_loop=False)
