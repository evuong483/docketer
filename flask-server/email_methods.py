#------------------------------------------------------------------------------
# email_methods.py
# Author: Erin Vuong
# Methods for sending emails
#------------------------------------------------------------------------------

# for email stuff
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText

EMAIL = 'docketer.notifications@gmail.com'
PWD = 'EMAIL_PWD_HERE'

def send_host_refresh_email(host_email, login_url):
    msg_body = ('The Google connection with your Docketer account is broken. '
                'Please login via <a href="{}">this link</a> to fix it.')\
                    .format(
                        login_url
                    )
    msg_subject = 'Docketer Google connection problem'
    send_email(host_email, msg_subject, msg_body)

def send_host_email(args, host_email):
    msg_body = ('<strong>{}</strong>(email: <strong>{}</strong>) scheduled a meeting '
           'on <strong>{}</strong> from <strong>{}</strong> to <strong>{}</strong>. '
           'Please contact the guest to reschedule or cancel.'
           '<br><br><strong>Meeting notes:</strong> {}').format(args['name'],
                                                           args['email'],
                                                           args['pretty_date'],
                                                           args['start'],
                                                           args['end'],
                                                           args['notes'])

    msg_subject = '{} {} meeting with {}'.format(args['date'],
                                                 args['start'],
                                                 args['name'])

    send_email(host_email, msg_subject, msg_body)

def send_guest_email(args, host_email, host_name):
    msg_body = ('You scheduled a meeting on <strong>{}</strong> from '
                '<strong>{}</strong> to <strong>{}</strong> with {}. '
                'Please contact the host at {} to reschedule or cancel.'
                '<br><br><strong>Meeting notes:</strong> {}').format(args['pretty_date'],
                                                                args['start'],
                                                                args['end'],
                                                                host_name,
                                                                host_email,
                                                                args['notes'])

    msg_subject = '{} {} meeting with {}'.format(args['date'],
                                                 args['start'],
                                                 host_name)

    send_email(args['email'], msg_subject, msg_body, bcc=host_email)

# send email
def send_email(msg_to, msg_subject, msg_body, bcc=None):
    # prepare message
    msg = MIMEText(msg_body, 'html')
    msg['To'] = msg_to
    msg['From'] = EMAIL
    msg['Subject'] = msg_subject
    if bcc:
        msg['Bcc'] = bcc

    # send email
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(EMAIL, PWD)
    s.send_message(msg)
    s.quit()