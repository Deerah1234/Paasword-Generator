import re
import smtplib
import ssl
from email.message import EmailMessage
from time import sleep
from getpass import getpass

from rich.console import Console
from rich.progress import track

import project


console = Console()


def sender(password: str) -> str:
    """sender: Sends the password to the receiver

    Args:
        password (str): This is the password generated from the generate_password function in project.py.

    Returns:
        str: A message informing the user that the password has been sent to there mail.
    """
    while True:
        try:
            email_sender = input("[bold yellow]Enter Email as sender:[/] ")
            # Note for Gmail Users, you need to generate an app password instead of your normal email password.
            # This also requires enabling 2-step authentication. Follow the instructions here to set-up
            # 2-Step Factor Authentication as well as App Password Generation:https://support.google.com/accounts/answer/185833?hl=en/.
            # Set-up 2 Factor Authentication, then create the App Password, choose Mail as the App and give it any name you want.
            # This will output a 16 letter password for you. Pass in this password here as your login password for the smtp.
            # But if you are using a different email like yahoo, outlook etc, just type in the password here.
            email_password = getpass("[bold yellow]Enter your App password:[/] ")
            email_receiver = console.input("[bold yellow]Enter Email as receiver:[/] ")

            # To check if the user type in the correct parameters
            match email_receiver:
                case email_receiver if email_receiver == "":
                    continue
                case email_receiver if not re.match(r"\w.+@\w+", email_receiver):
                    console.print(
                        "[bold red]Error[/][white]: Please enter a correct email[/]"
                    )
                    continue

            subject = console.input("[bold yellow]What is this for:[/] ")
            body = f"""Your password: {password}"""

            # Creating an EmailMessage(em) to set headers
            em = EmailMessage()
            em["From"] = email_sender
            em["To"] = email_receiver
            em["Subject"] = subject

            em.set_content(body)
            # A secure SSL context
            context = ssl.create_default_context()

            # Setting up the SMTP server and send email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email_sender, email_password)
                server.sendmail(email_sender, email_receiver, em.as_string())

            # The processing bar
            for _ in track(range(100), description="[bold green]Sending..."):
                sleep(0.1)

            return (
                f"Your password: <{password}> has been sent to your email: <{email_receiver}>"
                f"\n{project.OUTPUT_MESSAGE}"
            )

        except OSError:
            # Any error message should be caught
            console.print(
                "[bold red]Error[/][white]: Make sure you entered your correct email, check your internet "
                "connection and try again![/] "
            )
        continue


if __name__ == "__main__":
    sender()
