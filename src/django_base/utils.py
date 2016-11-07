import os
from django_base import settings
from smtplib import SMTPException
from django_base.settings import BASE_DIR
from django.core.mail import get_connection, EmailMultiAlternatives


def send_email(subject, body, to_email):
    """
    :param subject: Тема письма
    :param message_body: Тело письма
    :param email: E-mail адресата
    :return: Boolean
    """
    connection = get_connection()
    connection.open()

    msg = EmailMultiAlternatives(
        subject, body, settings.EMAIL_HOST_USER, [to_email]
    )
    msg.attach_alternative(body, "text/html")

    try:
        msg.send()
    except SMTPException:
        return False

    connection.close()
    return True


def get_filenames(rel_path, ext):
    '''
    Функция возвращает список файлов в заданном каталоге, с заданным расширением
    '''
    filenames = []

    template_dir = os.path.join(BASE_DIR, rel_path)
    root_len = len(template_dir.split(os.sep))

    for path, _, files in os.walk(template_dir):
        rel_path = os.sep.join(path.split(os.sep)[root_len:])
        for f in files:
            if f.endswith('.%s' % ext):
                flname = os.path.join(rel_path, f)
                filenames.append((flname, os.path.splitext(os.path.basename(flname))[0]))

    filenames = sorted(filenames, key=lambda x: x[1])

    return filenames
