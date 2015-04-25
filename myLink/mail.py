# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from urllib import parse


def sendVerificationEmail(recipient):
    me = 'ISendEmailForYou@gmail.com'
    user = recipient.email

    msg = MIMEText("Follow the provided link to activate your account. http://localhost:5000/user/verify/{0}".format(parse.quote_plus(recipient.emailToken)))

    msg['Subject'] = 'Please activate your account'
    msg['From'] = me
    msg['To'] = user

    # Credentials (if needed)
    username = 'ISendEmailForYou@gmail.com'
    password = '67Hqjo6rjJCnJMkfa2'

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(me, [user], msg.as_string())
    server.quit()
