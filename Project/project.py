import random
import re
import string

from rich.console import Console
from rich.markdown import Markdown

import send_to_mail


console = Console()
# Letters, Numbers and Special-characters.
CHARS = "".join(
    (
        string.ascii_letters,
        string.digits,
        string.punctuation,
    )
)

# A message asking the user what type of password to be generated.
MESSAGE = """
### How Do You Want Your Password?
    -> Choose Either 1, 2 or 3
    1. With Special Characters, Numbers And Letters: Upper&Lower
    2. With Special Characters And Numbers
    3. With Letters: Upper&Lower And Numbers
"""

OUTPUT_MESSAGE = """
Thanks for using my password generator.
Creator: Emmanuel James
   @cyiomDev - 2022
"""


def main() -> None:
    console.print(
        Markdown(" ### Welcome To The Password Generator "), style="bold blue"
    )
    # To check if the user types in the correct input
    while True:
        try:
            password_length = int(
                console.input("[bold yellow]What length of password do you want:[/] ")
            )
            message_markdown = Markdown(MESSAGE)
            console.print(message_markdown, style="bold white")

            # While loop to check if the user types in the correct range 1 to 3
            while True:
                try:
                    character_choice = int(console.input("[bold yellow]->[/] "))

                    # Chooses Special-Characters, Numbers And Letters: Upper&Lower
                    if character_choice == 1:
                        print(generate_password(password_length, CHARS))
                    # Chooses Special Characters And Numbers
                    elif character_choice == 2:
                        password_pattern(r"[\W0-9]", password_length)
                    # Chooses Letters: Upper&Lower And Numbers
                    elif character_choice == 3:
                        password_pattern(r"\w*9", password_length)
                    else:
                        console.print(
                            "[bold red]Error[/][bold white]: Only 1 to 3 are allowed[/]"
                        )
                        continue
                    break
                except ValueError:
                    console.print("[bold red]Error[/][white]: Please enter a number[/]")

        except ValueError:
            console.print("[bold red]Error[/][white]: Please enter a number[/]")
            continue

        except KeyboardInterrupt:
            exit()
        break


def password_pattern(given_pattern: str, password_length: int) -> None:
    """password_pattern: Create a pattern of which the password will be created from.

    Args:
        given_pattern (str): A pattern to follow from the CHARS variable.
        password_length (int): Takes the length of characters to be created.
    """
    pattern = re.compile(given_pattern)
    # Choice of password based on the given_pattern
    character_choice = "".join(re.findall(pattern, CHARS))
    print(generate_password(password_length, character_choice))


def generate_password(password_length: int, given_characters: str) -> str:
    """generate_password: Create a random string from the given_characters.

    Args:
        password_length (int): Takes the length of characters to be created.
        given_characters (str): Where the characters will be randomly picked.

    Returns:
        str: Returns a string of letters.
    """
    password = ""

    for _ in range(password_length):
        random_choice = "".join(random.choices(given_characters))
        password += random_choice
    return send_password(password)


def send_password(password: str) -> str:
    """send_password: Send the password to mail if the user answer is 'Y', otherwise prints the password.

    Args:
        password (str): A string of letters generated from the generate_password function.

    Returns:
        str: A string of letters.
    """
    console.print("[bold yellow]Will you like your Password sent to your mail?[/]")

    # To check if the user types y or n correctly
    while True:
        request = console.input("[bold yellow][i]Y[/i] or [i]N[/i] ->[/] ")
        match request:
            case request if request.lower() == "y":
                return send_to_mail.sender(password)
            case request if request.lower() == "n":
                return f"Your password: {password}\n{OUTPUT_MESSAGE}"
            case _:
                console.print(
                    "[bold red]Error[/][white]: Please enter either Y or N[/]"
                )
                continue


if __name__ == "__main__":
    main()
