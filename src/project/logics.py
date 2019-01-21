import sendgrid
import os
from sendgrid.helpers.mail import Personalization, Email, Content, Mail


class MailLogics:
    def send(self, data):
        to_list = Personalization()

        self.__add_to(data, to_list)
        self.__add_cc(data, to_list)
        self.__add_bcc(data, to_list)

        sg = sendgrid.SendGridAPIClient(
            apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email(data['from'])

        subject = data['subject']

        content = Content("text/html", data['body'])
        mail = Mail(from_email, subject, None, content)

        if 'reply_to' in data:
            mail.reply_to = Email("csilva@gusisoft.cl")

        mail.add_personalization(to_list)
        sg.client.mail.send.post(request_body=mail.get())

    def __add_to(self, data, list):
        if 'to' in data and data['to']:
            for mail in data['to']:
                list.add_to(Email(mail))

    def __add_cc(self, data, list):
        if 'cc' in data and data['cc']:
            for mail in data['cc']:
                list.add_cc(Email(mail))

    def __add_bcc(self, data, list):
        if 'bcc' in data and data['bcc']:
            for mail in data['bcc']:
                list.add_bcc(Email(mail))
