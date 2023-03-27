import telegram
from telegram.ext import Updater, Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
import cv2
from io import BytesIO
import numpy as np
import random
import os


async def healthz(update: Update, context: CallbackContext):
    await update.message.reply_text('OK')


async def start(update: Update, context: CallbackContext):

    await update.message.reply_text('''
    Hello !
Welcome to Pencil-it bot!
I'm a bot that converts your images into pencil art :)
Use /help for commands or 
just go ahead and send an image to the bot 
and get a sketch as a reply.

    ''')


async def help(update: Update, context: CallbackContext):
    await update.message.reply_text('''
    Here are the commands:
/start-> to begin
/help-> to list commands
/about-> details about the bot
/donate->details for donation
/contact->developer details for contacting
No need to give any command for the image conversion,
just upload the image and watch the magic happen
    ''')


async def text_handler(update: Update, context: CallbackContext):
    await update.message.reply_text('''
    Please send an image to generate a sketch
or use /help command for help
    ''')


async def donate(update: Update, context: CallbackContext):
    await update.message.reply_text('''
    I know it's difficult times which is why I have made the bot free, but the bot also does have running costs which incase a certain quota exceeds, I have to pay.
If you think you can make a contibution, it would go a long way in helping me and motivating me to do more projects like this.
You can donate via the following links:
Buy me a coffee-> https://www.buymeacoffee.com/dev.stephno
Paypal-> https://paypal.me/aastlestephno
For Indian users:
UPI ID-> dev.stephno@apl
Thank you :)
    ''')


async def contact(update: Update, context: CallbackContext):
    await update.message.reply_text('''
    You can contact me via the username @gl1tch1e in telegram
Or hit me up via twitter-> https://twitter.com/dev_stephno
    ''')


async def about(update: Update, context: CallbackContext):
    await update.message.reply_text('''    
    For better results please provide a high resolution image. If you want to fine tune your image, you can go to your local editor and adjust the contrast and brightness as per your desire. It has proved to provide a more pencil-esque depth effect.
If you encounter any bugs or have any suggestions, feel free to /contact me.
This bot is built using python. It is absolutely free to use, however you can consider to /donate to help me cover the running costs.
    ''')


async def doc_handler(update: Update, context: CallbackContext):
    await update.message.reply_text('''
    Please send your image as a photo and not a document.
Refer to the below image for better understanding.
    ''')
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=open("demo.png", "rb"))


async def photo_handler(update: Update, context: CallbackContext):
    print('Photo received')
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    print(type(file))
    f = BytesIO(await file.download_as_bytearray())
    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    cnvrt = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(cnvrt)
    blur = cv2.GaussianBlur(invert, (21, 21), 0)
    invertedblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(cnvrt, invertedblur, scale=230.0)
    cv2.imwrite("s.png", sketch)
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open(
        "s.png", "rb"), caption="Here is your sketched image. Hope you like it!. Not satisfied? Head over to /about section.")
    if random.randint(1, 2) == 1:
        await update.message.reply_text('''
        Liking the bot so far? If so, happy to know! 
    Your contributions would go a long way in helping me cover the running costs. Go to /donate for more details.
        ''')


def main():
    # for local environment
    # f = open("token.txt", "r")
    # TOKEN = f.readline()
    # for production environment
    token = os.environ["TOKEN"]

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.TEXT, text_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, doc_handler))
    app.add_handler(MessageHandler(filters.regex('^/healthz$'), healthz))

    app.run_polling()


if __name__ == '__main__':
    main()
