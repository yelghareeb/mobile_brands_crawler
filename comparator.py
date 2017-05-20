import sys

class Comparator:
	def __init__(self, old_kb, new_kb):
		self.old_kb = old_kb
		self.new_kb = new_kb

	def get_new_phones(self):
		return [phone for phone in self.new_kb if phone not in self.old_kb]

	def get_removed_phones(self):
		return [phone for phone in self.old_kb if phone not in self.new_kb]

	def get_updated_phones(self):
		updated_phones = []
		for phone in self.new_kb:
			try:
				index = self.old_kb.index(phone)
				other_phone = self.old_kb[index]
				if phone.price != other_phone.price:
					updated_phones.append((other_phone, phone))
			except:
				# Phone not in old_kb list
				continue
		return updated_phones