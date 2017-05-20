from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
from collections import defaultdict
import sys
import operator

class Report:
	def __init__(self, phones, new_phones, removed_phones, updated_phones):
		self.sender = "EMAIL"
		self.password = "PASSWORD"
		self.recipient = "RECIPIENT"
		self.phones = phones
		self.new_phones = new_phones
		self.removed_phones = removed_phones
		self.updated_phones = updated_phones

	def load_template(self):
		f = open('template.html', 'r')
		return f.read()

	def group_phones(self):
		g = defaultdict(list)
		for phone in self.phones:
			g[phone.model].append(phone)
		return g

	def get_all_phones(self):
		grouped_phones = self.group_phones();
		l = []
		for group in grouped_phones:
			l.append('<h2>' + group + '</h2>')
			l.append('<div class="datagrid">')
			l.append('<table>')
			l.append('<thead>')
			l.append('<tr>')
		   	l.append('<th>Model Name</th>')
		   	l.append('<th>Price</th>')
			l.append('</tr>')
			l.append('</thead>')
			l.append('<tbody>')
			grouped_phones[group].sort(reverse = True)
			for phone in grouped_phones[group]:
				l.append('<tr>')
				l.append('<td><a href="' + phone.url + '">' + phone.name + "</a></td>")
				l.append('<td>' + phone.price + "</td>")
				l.append('</tr>')
			l.append('</tbody>')
			l.append('</table>')
			l.append('</div>')
		return "".join(l)

	def get_updates(self):
		l = []
		l.append('<h2>New Phones</h2>')
		if self.new_phones:
			l.append('<div class="datagrid">')
			l.append('<table>')
			l.append('<thead>')
			l.append('<tr>')
			l.append('<th>Model Name</th>')
			l.append('<th>Price</th>')
			l.append('</tr>')
			l.append('</thead>')
			l.append('<tbody>')
			for phone in self.new_phones:
				l.append('<tr>')
				l.append('<td class="added-phone"><a href="' + phone.url + '">' + phone.name + "</a></td>")
				l.append('<td class="added-phone">' + phone.price + "</td>")
				l.append('</tr>')
			l.append('</tbody>')
			l.append('</table>')
			l.append('</div>')
		else:
			l.append('<p>No new phones.</p>')

		l.append('<br>')
		l.append('<h2>Removed Phones</h2>')
		if self.removed_phones:
			l.append('<div class="datagrid">')
			l.append('<table>')
			l.append('<thead>')
			l.append('<tr>')
			l.append('<th>Model Name</th>')
			l.append('<th>Price</th>')
			l.append('</tr>')
			l.append('</thead>')
			l.append('<tbody>')
			for phone in self.removed_phones:
				l.append('<tr>')
				l.append('<td class="removed-phone"><a href="' + phone.url + '">' + phone.name + "</a></td>")
				l.append('<td class="removed-phone">' + phone.price + "</td>")
				l.append('</tr>')
			l.append('</tbody>')
			l.append('</table>')
			l.append('</div>')
		else:
			l.append('<p>No removed phones.</p>')

		l.append('<br>')
		l.append('<h2>Updated Prices</h2>')
		if self.updated_phones:
			l.append('<div class="datagrid">')
			l.append('<table>')
			l.append('<thead>')
			l.append('<tr>')
			l.append('<th>Model Name</th>')
			l.append('<th>Old Price</th>')
			l.append('<th>New Price</th>')
			l.append('</tr>')
			l.append('</thead>')
			l.append('<tbody>')
			for phone in self.updated_phones:
				l.append('<tr>')
				l.append('<td><a href="' + phone[0].url + '">' + phone[0].name + "</a></td>")
				l.append('<td>' + phone[0].price + "</td>")
				l.append('<td>' + phone[1].price + "</td>")
				l.append('</tr>')
			l.append('</tbody>')
			l.append('</table>')
			l.append('</div>')
		else:
			l.append('<p>No updated prices.</p>')
		return "".join(l)

	def send_mail(self, msg):
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(self.sender, self.pass)
		text = msg.as_string()
		server.sendmail(self.sender, self.recipient, text)

	def prepare_msg(self, subject):
		msg = MIMEMultipart()
		msg['From'] = self.sender
		msg['To'] = self.recipient
		msg['Subject'] = subject
		return msg

	def send_summary(self):
		msg = self.prepare_msg("Latest Phone Prices")
		body = self.load_template()
		body = body.replace("TABLE_1", self.get_all_phones())
		msg.attach(MIMEText(body, 'html'))
		self.send_mail(msg)

	def send_updates(self):
		msg = self.prepare_msg("Updates of Latest Phone Prices")
		body = self.load_template()
		body = body.replace("TABLE_1", self.get_updates())
		msg.attach(MIMEText(body, 'html'))
		self.send_mail(msg)
