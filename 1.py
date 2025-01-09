from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
API_TOKEN = '7403811529:AAFBYrUcnGq2FHQIRAhzrID4Ll-Mbigx0uY'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Transliteration rules (same as your previous example)
LOTIN_TO_KIRIL = {
    "a": "а", "b": "б", "d": "д", "e": "е", "f": "ф", "g": "г",
    "h": "ҳ", "i": "и", "j": "ж", "k": "к", "l": "л", "m": "м",
    "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с",
    "t": "т", "u": "у", "v": "в", "x": "х", "y": "й", "z": "з",
    "sh": "ш", "ch": "ч", "yo": "ё", "yu": "ю", "ya": "я",
    "o'": "ў", "g'": "ғ", "ng": "нг",
}

KIRIL_TO_LOTIN = {v: k for k, v in LOTIN_TO_KIRIL.items()}

# Function to translate text from Latin to Cyrillic and vice versa
def translate_text(text, to_kiril=True):
    result = []
    rules = LOTIN_TO_KIRIL if to_kiril else KIRIL_TO_LOTIN

    i = 0
    while i < len(text):
        # Check for two-character sequences first
        if i + 1 < len(text) and text[i:i+2].lower() in rules:
            # Check if both characters are uppercase
            translated = rules[text[i:i+2].lower()]
            if text[i:i+2].isupper():
                translated = translated.upper()  # Convert to uppercase if both are uppercase
            result.append(translated)
            i += 2
        # Check for single characters
        elif text[i].lower() in rules:
            translated = rules[text[i].lower()]
            if text[i].isupper():
                translated = translated.upper()  # Convert to uppercase if the character is uppercase
            result.append(translated)
            i += 1
        else:
            result.append(text[i])
            i += 1

    return ''.join(result)

# Command to handle start message
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Men Lotin va Kiril alifbolarini bir-biriga tarjima qiluvchi botman.\n\n"
                         "Matnni yuboring va men uni tarjima qilaman!")

# Command to handle incoming messages
@dp.message_handler()
async def handle_message(message: types.Message):
    input_text = message.text
    # Detect if input text is in Cyrillic or Latin
    if any(char in LOTIN_TO_KIRIL for char in input_text.lower()):
        # If Latin script is detected, convert to Cyrillic
        translated_text = translate_text(input_text, to_kiril=True)
        await message.reply(f"Lotin → Kiril:\n{translated_text}")
    elif any(char in KIRIL_TO_LOTIN for char in input_text.lower()):
        # If Cyrillic script is detected, convert to Latin
        translated_text = translate_text(input_text, to_kiril=False)
        await message.reply(f"Kiril → Lotin:\n{translated_text}")
    else:
        await message.reply("Iltimos, faqat Lotin yoki Kiril alifbosida yozing.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
