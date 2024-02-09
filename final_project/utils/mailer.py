import smtplib, ssl
from typing import List
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:
  def __init__(self, host: str, port: int, user: str, password: str):
    ctx = ssl.create_default_context()
    self._server = smtplib.SMTP(host, port)
    self._server.starttls(context=ctx)
    self._server.login(user, password)


  def send(self, sender: str, receipient: str, subject: str, text: str, html: str, attachments: List[str] = []) -> None:
    msg = self.__create_message(text, html)
    msg = self.__add_attachments(msg, attachments)

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receipient

    self._server.sendmail(sender, receipient, msg.as_string())

  def __create_message(self, text: str, html: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")

    if text:
      msg.attach(MIMEText(text, "plain"))

    if html:
      msg.attach(MIMEText(html, "html"))

    return msg

  def __add_attachments(self, msg: MIMEMultipart, attachments: List[str]) -> MIMEMultipart:
    for file_dir in attachments:
      with open(file_dir, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())

      dirs = file_dir.split("/")

      encoders.encode_base64(part)
      part.add_header("Content-Disposition", f"attachment; filename={dirs[-1]}")
      msg.attach(part)

    return msg


  def quit(self):
    self._server.quit()

