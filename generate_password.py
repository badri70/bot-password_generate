import random
import string

def generate_password_logic(length, digits, letters, specials):
    characters = ""
    if digits:
        characters += string.digits
    if letters:
        characters += string.ascii_letters
    if specials:
        characters += string.punctuation

    if not characters:
        return "Вы не выбрали ни одного типа символов!"

    return "".join(random.choice(characters) for _ in range(length))
