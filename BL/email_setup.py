"""

Reference file for sending the weather report

"""

from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.application import encoders

from DL.account_data import personal_email, mail_login


def send_email(target_email, report_date):
    """

    Send the email with the linked pdf

    :param target_email:
    :param report_date:
    :return:
    """

    message = MIMEMultipart()
    message['Subject'] = "Attachment Test"
    message['From'] = personal_email
    message['To'] = target_email

    text = MIMEText("Please find attached your complimentary weather report!")
    message.attach(text)

    directory = "/Users/aurelien/PycharmProjects/temperature_report/Report/Report_generated/" \
                "Weather report {}.pdf".format(report_date)
    with open(directory, 'rb') as opened:
        openedfile = opened.read()
    attachedfile = MIMEApplication(openedfile, _subtype="pdf", _encoder=encoders.encode_base64)
    attachedfile.add_header('content-disposition', 'attachment',
                            filename="Weather report {}.pdf".format(report_date))
    message.attach(attachedfile)

    server = SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login(personal_email, mail_login)
    server.sendmail(message['From'], message['To'], message.as_string())
    server.quit()
