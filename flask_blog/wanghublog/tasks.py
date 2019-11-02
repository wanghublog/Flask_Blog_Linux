import smtplib
import datetime
from email.mime.text import MIMEText
from flask import current_app
from flask_mail import Message
from wanghublog.models import Reminder
from wanghublog.extensions import flask_celery, mail

@flask_celery.task
def add(x):
    return str(x)

@flask_celery.task
def flask_app_context():
    with current_app.app_context():
        return str(current_app.config)

@flask_celery.task(
    bind=True,
    igonre_result=True,
    default_retry_delay=300,
    max_retries=5)
def remind(self,primary_key):
    """Send the remind email to user when registered.
       Using Flask-Mail.
    """

    reminder = Reminder.query.get(primary_key)

    msg = MIMEText(reminder.text,'plain','utf-8')
    msg['Subject'] = 'Welcome!'
    msg['FROM'] = 'wjamesh@qq.com'
    msg['To'] = reminder.email

    try:
        smtp_server = smtplib.SMTP('smtp.qq.com')
        # smtp_server.set_debuglevel(1)
        smtp_server.starttls()
        # smtp_server.ehlo()
        smtp_server.login('wjamesh@qq.com', 'fipwmcrdxdithgha')
        smtp_server.sendmail('wjamesh@qq.com',
                         [reminder.email],
                         msg.as_string())
        smtp_server.close()
        return 'sucessfully'
    except Exception as e:
        self.retry(exc=e)#重新执行任务
        # return 'failed'
        


def on_reminder_save(mapper, connect, self):
    """Callbask for task remind."""
    # remind.apply_async(args=(self.id,), countdown=3)
    remind.delay(self.id)

