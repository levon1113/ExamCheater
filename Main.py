import keyboard as k 
import clipboard as cb
import pyautogui as pag
import smtplib
import imaplib
import email
import base64	

from email.mime.text import MIMEText
from email.header import decode_header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from time import sleep


# Configure it
RECEIVER_EMAIL = "armen14102003@mail.ru"
SENDER_EMAIL = "monkey.d.luffy.best.king@gmail.com"
PASSWORD = "unitazmet"

# Shortcuts
START = 'shift+s'
PAUSE = 'shift+p'
QUIT =  'shift+q'

SCREENSHOT = 'shift+z'
SEND_TEXT = 'shift+x'
PASTE_TEXT = 'shift+c'
REFRESH = 'shift+v'


CHARACTERS = """a b c d e f g h i j k l m n o p q r s t u v w x y z - . , ; [ ] \\ / = ` 1 2 3 4 5 6 7 8 9 0 space""".split()

FILENAME = 'file.png'
SUBJECT = "SQL"


def sendmail(Screenshot=True):
	with open(FILENAME, 'rb') as f:
		img_data = f.read()

	msg = MIMEMultipart()
	msg['Subject'] = SUBJECT
	msg['From'] = SENDER_EMAIL
	msg['To'] = RECEIVER_EMAIL

	if Screenshot:
		with open(FILENAME, 'rb') as f:
			img_data = f.read()
		image = MIMEImage(img_data, name=FILENAME)
		msg.attach(image)
	else:
		text = MIMEText(cb.paste())
		msg.attach(text)

	with smtplib.SMTP('64.233.184.108', 587) as server:
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login(SENDER_EMAIL, PASSWORD)

		server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())


def screenshot():
	shot = pag.screenshot()
	shot.save(FILENAME)


def readmail(answer=True):
	with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
		mail.login(SENDER_EMAIL, PASSWORD)
		mail.select('inbox')

		data = mail.search(None, f'(FROM "{RECEIVER_EMAIL}")')
		mail_ids = data[1]
		id_list = list(map(int, mail_ids[0].split()))

		for i in id_list[::-1]:
			data = mail.fetch(str(i), '(RFC822)')
    
			for response_part in data:
				arr = response_part[0]
				if isinstance(arr, tuple):
					msg = email.message_from_string(str(arr[1],'utf-8'))
					code = base64.b64decode(msg.get_payload()[0].get_payload()).decode()
					subject = decode_header(msg.get('subject'))[0][0].decode()

					if not answer and SUBJECT.lower() not in subject.lower():
						return code
					
					elif answer and SUBJECT.lower() in subject.lower():
						return code


def main():
	prev_text = ''
	idx = 1
	text = ' '

	while True:
		if k.is_pressed(PASTE_TEXT):
			sleep(0.1)
			k.write(readmail(answer=False))

		if k.is_pressed(SCREENSHOT):
			sleep(0.1)
			screenshot()
			sendmail(Screenshot=True)

		if k.is_pressed(SEND_TEXT):
			sleep(0.1)
			sendmail(Screenshot=False)

		if k.is_pressed(PAUSE):
			sleep(0.2)
			
			while True:
				if k.is_pressed(PAUSE):
					sleep(0.2)
					break

		if k.is_pressed(QUIT):
			return

		if k.is_pressed(REFRESH):
			sleep(0.1)
			if text != " ":
				prev_text = text
			temp_text = readmail(answer=True)
			if temp_text == text or temp_text == prev_text:
				text = " "
			else:
				text = temp_text
			idx = 1


		if text != " ":
			for i in CHARACTERS:
				if k.is_pressed(i):
					k.press("backspace")
					k.write(text[idx])

					if idx < len(text)-1:
						idx += 1

					while True:
						if not k.is_pressed(i):
							break



main()
