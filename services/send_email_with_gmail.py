import smtplib

from decouple import config


def send_email_notification(message):
    gmail_user = config("GMAIL_ADDRESS")
    gmail_password = config("GMAIL_PASSWORD")

    sent_from = "Parking api"
    to = [gmail_user]
    subject = "Super Important Message, new user was register"
    body = f"{message}"

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (
        sent_from,
        ", ".join(to),
        subject,
        body,
    )
    try:
        # For 587 use this
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.ehlo()
        # server.starttls()

        # For 465 use this
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        print("That is good, connection is ok")
        server.login(gmail_user, gmail_password)
        print("Login is good, credential is good")
        server.sendmail(sent_from, to, email_text)
        server.close()
        print("Email sent successfully!")
    except:
        print("Something went wrong...")


if __name__ == "__main__":
    send_email_notification("Test")
