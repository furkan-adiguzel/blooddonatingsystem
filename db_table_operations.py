import os
import sys
import psycopg2 as dbapi2
from datetime import datetime, date

def get_users():
	query ='SELECT * FROM USERS'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query)
		users = cursor.fetchall()
		cursor.close()
	return users

def search_users_id(temp_id):
	query ='SELECT * FROM USERS WHERE USER_ID = %s'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (temp_id,))
		user = cursor.fetchone()
		cursor.close()
	return user

def search_users_username(temp_username):
	query ='SELECT * FROM USERS WHERE USERNAME = %s'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (temp_username,))
		user = cursor.fetchone()
		cursor.close()
	return user

def search_users_password(temp_username):
	query ='SELECT * FROM USERS WHERE USERNAME = %s'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (temp_username,))
		user = cursor.fetchone()
		cursor.close()
	return user[3]

def add_new_user(users):
	query = 'INSERT INTO USERS (USER_ID, USER_EMAIL, USERNAME, PASSWORD, IS_ADMIN)' \
			'VALUES(%s, %s, %s, %s, %s)'
	url = get_db_url()
	user_id = datetime.now().strftime("%Y%m%d%H%M%S")
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (user_id, users.user_email, users.username,  users.password,  users.is_admin))
		cursor.close()

def update_users(user_id, users):
	query = 'UPDATE USERS ' \
			'SET IS_ADMIN = %s, ' \
			'PASSWORD = %s ' \
			'WHERE USER_ID = %s '
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (users.is_admin, users.password, user_id,))
		cursor.close()




def add_new_donor(donors):
	query = 'INSERT INTO DONORS (DONOR_ID, NAME, SURNAME, PHONE_NUMBER, BIRTH_DATE, BLOOD_TYPE, ADDRESS)' \
			'VALUES(%s, %s, %s, %s, %s, %s, %s)'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (donors.donor_id, donors.name, donors.surname, donors.phone_number, donors.birth_date, donors.blood_type, donors.address))
		cursor.close()

def add_new_patient(patients):
	query = 'INSERT INTO PATIENTS (PATIENT_ID, NAME, SURNAME, PHONE_NUMBER, BIRTH_DATE, BLOOD_TYPE, ADDRESS)' \
			'VALUES(%s, %s, %s, %s, %s, %s, %s)'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (patients.patient_id, patients.name, patients.surname, patients.phone_number, patients.birth_date, patients.blood_type, patients.address))
		cursor.close()

def add_new_bloodbag(bloodbags):
	query = 'INSERT INTO BLOODBAGS (BLOODBAG_ID, BLOOD_TYPE, DONOR_ID, PATIENT_ID, EXPIRATION)' \
			'VALUES(%s, %s, %s, %s, %s)'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (bloodbags.bloodbag_id, bloodbags.blood_type, bloodbags.donor_id, bloodbags.patient_id, bloodbags.expiration))
		cursor.close()


def update_donors(donor_id, donors):
	query = 'UPDATE DONORS ' \
			'SET NAME = %s, ' \
			'SURNAME = %s, ' \
			'PHONE_NUMBER = %s, ' \
			'BIRTH_DATE = %s, ' \
			'BLOOD_TYPE = %s, ' \
			'ADDRESS = %s, ' \
			'LAST_DONATE_DATE = %s ' \
			'WHERE DONOR_ID = %s '
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (donors.name, donors.surname, donors.phone_number, donors.birth_date, donors.blood_type, donors.address, donors.last_donate_date, donors.donor_id,))
		cursor.close()

def update_patients(patient_id, patients):
	query = 'UPDATE PATIENTS ' \
			'SET NAME = %s, ' \
			'SURNAME = %s, ' \
			'PHONE_NUMBER = %s, ' \
			'BIRTH_DATE = %s, ' \
			'BLOOD_TYPE = %s, ' \
			'ADDRESS = %s ' \
			'WHERE PATIENT_ID = %s '
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (patients.name, patients.surname, patients.phone_number, patients.birth_date, patients.blood_type, patients.address, patients.patient_id,))
		cursor.close()

def update_bloodbags(bloodbag_id, bloodbags):
	query = 'UPDATE BLOODBAGS ' \
			'SET BLOOD_TYPE = %s, ' \
			'DONOR_ID = %s, ' \
			'PATIENT_ID = %s, ' \
			'EXPIRATION = %s ' \
			'WHERE BLOODBAG_ID = %s '
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (bloodbags.blood_type, bloodbags.donor_id, bloodbags.patient_id, bloodbags.expiration, bloodbags.bloodbag_id,))
		cursor.close()


def delete_donors(donor_id):
	query = 'DELETE FROM DONORS WHERE DONOR_ID = CAST(%s AS BIGINT)'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (donor_id,))
		cursor.close()

def delete_patients(patient_id):
	query = 'DELETE FROM PATIENTS WHERE PATIENT_ID = CAST(%s AS BIGINT)'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (patient_id,))
		cursor.close()


def search_donors(temp_id):
	query ='SELECT * FROM DONORS WHERE DONOR_ID = %s'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (temp_id,))
		donor = cursor.fetchone()
		cursor.close()
	return donor

def search_patients(temp_id):
	query ='SELECT * FROM PATIENTS WHERE PATIENT_ID = %s'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (temp_id,))
		patient = cursor.fetchone()
		cursor.close()
	return patient

def search_bloodbags(temp_id):
	query ='SELECT * FROM BLOODBAGS WHERE BLOODBAG_ID = %s'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query, (temp_id,))
		bloodbag = cursor.fetchone()
		cursor.close()
	return bloodbag


def get_donors():
	query ='SELECT * FROM DONORS'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query)
		donors = cursor.fetchall()
		cursor.close()
	return donors

def get_patients():
	query ='SELECT * FROM PATIENTS'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query)
		patients = cursor.fetchall()
		cursor.close()
	return patients

def get_bloodbags():
	query ='SELECT * FROM BLOODBAGS'
	url = get_db_url()
	with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		cursor.execute(query)
		bloodbags = cursor.fetchall()
		cursor.close()
	return bloodbags



def get_db_url():
	NEW_URL = os.getenv("DATABASE_URL")
	if not NEW_URL:
		url = "postgres://postgres:test123@localhost:5432/bds"
		return url
	else:
		return NEW_URL
	if url is None:
		print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
		sys.exit(1)
