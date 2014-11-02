from django.conf import settings

from celery import shared_task
from postmark import PMMail

@shared_task
def send_mail(**kwargs):
    '''
    Keyword arguments are:
    api_key:        Your Postmark server API key
    sender:         Who the email is coming from, in either
                    "name@email.com" or "First Last <name@email.com>" format
    to:             Who to send the email to, in either
                    "name@email.com" or "First Last <name@email.com>" format
                    Can be multiple values separated by commas (limit 20)
    cc:             Who to copy the email to, in either
                    "name@email.com" or "First Last <name@email.com>" format
                    Can be multiple values separated by commas (limit 20)
    bcc:            Who to blind copy the email to, in either
                    "name@email.com" or "First Last <name@email.com>" format
                    Can be multiple values separated by commas (limit 20)
    subject:        Subject of the email
    tag:            Use for adding categorizations to your email
    html_body:      Email message in HTML
    text_body:      Email message in plain text
    track_opens:    Whether or not to track if emails were opened or not
    custom_headers: A dictionary of key-value pairs of custom headers.
    attachments:    A list of tuples or email.mime.base.MIMEBase objects
                    describing attachments.
    '''
    from_name = kwargs.pop('from_name', None)
    if from_name:
        sender = '%s <%s>' % (from_name, settings.POSTMARK_SENDER)
        mail = PMMail(sender=sender, **kwargs)
    else:
        mail = PMMail(**kwargs)
    mail.send()
