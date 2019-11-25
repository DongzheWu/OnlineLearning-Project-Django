__author__ = 'wdz'
__date__ = '2019/10/21 16:19'
from random import Random
import  logging

from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from OnlineStudy.settings import EMAIL_FROM

logger = logging.getLogger(__name__)
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()


    if send_type == "register":
        email_title = "OnlineStudy register verify code: "
        email_body ="Please click the url to activate your account: http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            logger.error("sent---------------")
            pass
    elif send_type == "forget":
        email_title = "OnlineStudy change your password"
        email_body ="Please click the url to reset your account: http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            logger.error("sent---------------")
            pass

    elif send_type == "update_email":
        email_title = "OnlineStudy modify your email"
        email_body = "The code is {0}".format(code[:4])
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass

