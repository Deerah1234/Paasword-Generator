import string

from rich.console import Console

from project import generate_password, main, password_pattern, send_password
from send_to_mail import sender


console = Console()
CHARS = "".join(
    (
        string.ascii_letters,
        string.digits,
        string.punctuation,
    )
)


def test_main() -> None:
    assert main() is None


def test_password_pattern_special_characters_and_numbers() -> None:
    assert password_pattern(r"[\W0-9]", 4) is None


def test_password_pattern_Letters_Upper_Lower_and_numbers() -> None:
    assert password_pattern(r"\w*9", 8) is None


def test_generate_password() -> None:
    assert generate_password(8, CHARS) is not None


def test_send_password() -> None:
    # Picked a random characters to test.
    assert send_password("dkssj4") is not None


def test_sender() -> None:
    assert sender("dkssj4") is not None


if __name__ == "__main__":
    test_password_pattern_special_characters_and_numbers()
    test_password_pattern_Letters_Upper_Lower_and_numbers()
    test_generate_password()
    test_send_password()
    test_main()
    test_sender()
