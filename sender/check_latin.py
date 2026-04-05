import string


async def is_latin_only(text):
    allowed_chars = string.ascii_letters.lower()
    return all(char in allowed_chars for char in text)

