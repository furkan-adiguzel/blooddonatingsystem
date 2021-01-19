from flask_login import UserMixin

class Users(UserMixin):
	def __init__(self, user_email, username, password, is_admin):
		self.user_id = 0
		self.user_email = user_email
		self.username = username
		self.password = password
		self.is_admin = is_admin
		self.is_authenticated

	def set_id(self, user_id):
		self.user_id = user_id	

	def get_id(self):
		return self.user_id

	def set_authentication(self):
		self.is_authenticated = True

	def __repr__(self):
		return '<User %r>' % self.user_email

	@property
	def is_active(self):
		return True

	@property
	def is_authenticated(self):
		return True

class Donors:
	def __init__(self, donor_id, name, surname, phone_number, birth_date, blood_type, address, last_donate_date):
		self.donor_id = donor_id
		self.name = name
		self.surname = surname
		self.phone_number = phone_number
		self.birth_date = birth_date
		self.blood_type = blood_type
		self.address = address
		self.last_donate_date = last_donate_date

class Patients:
	def __init__(self, patient_id, name, surname, phone_number, birth_date, blood_type, address):
		self.patient_id = patient_id
		self.name = name
		self.surname = surname
		self.phone_number = phone_number
		self.birth_date = birth_date
		self.blood_type = blood_type
		self.address = address

class Bloodbags:
	def __init__(self, bloodbag_id, blood_type, donor_id, patient_id, expiration):
		self.bloodbag_id = bloodbag_id
		self.blood_type = blood_type
		self.donor_id = donor_id
		self.patient_id = patient_id
		self.expiration = expiration
		
