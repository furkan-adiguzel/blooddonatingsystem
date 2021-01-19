from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, date, timedelta
from calendar import monthrange

from db_table_operations import *
from dbinit import *
from models import Donors, Patients, Bloodbags, Users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
	db_user = search_users_id(int(user_id))
	user = Users(db_user[1], db_user[2], db_user[3], db_user[4])
	user.set_id(db_user[0])
	return user


class LoginForm(FlaskForm):
	login_username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
	login_password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=30)])
	remember = BooleanField('Remember me')


@app.route('/')
@login_required
def index():
	return render_template("index.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()
	if request.method == "POST":
		if form.validate_on_submit():
			found_user = search_users_username(form.login_username.data)
			if found_user:
				found_password = search_users_password(form.login_username.data)
				if found_password == form.login_password.data:
					user = Users(found_user[1], found_user[2], found_user[3], found_user[4])
					user.set_id(found_user[0])
					login_user(user, remember=form.remember.data)
					print(user)
					return redirect(url_for('index'))
			error_statement = "There was a problem signing in. Username or Password is wrong."
			return render_template("login.html", form=form, error_statement=error_statement)
		error_statement = "There was a problem signing in. Username or Password is wrong."
		return render_template("login.html", form=form, error_statement=error_statement)		
	return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/user_panel', methods=['POST', 'GET'])
@login_required
def user_panel():
	temp_id = current_user.user_id
	user_to_update = search_users_id(temp_id)
	if request.method == "GET":
		return render_template("user_panel.html", user_to_update=user_to_update)
	else:
		password = request.form['password']
		updated_user = Users(user_to_update[1], user_to_update[2], password, user_to_update[4])
		update_users(temp_id, updated_user)
		return redirect(url_for("index"))


@app.route('/admin_panel')
@login_required
def admin_panel():
	if current_user.is_admin:
		users = get_users()
		return render_template("admin_panel.html", users=users)
	return redirect(url_for('index'))

@app.route('/add_user', methods=['POST', 'GET'])
@login_required
def add_user():
	if current_user.is_admin:
		if request.method == "POST":
			user_email = request.form['email']
			username = request.form['username']
			password = request.form['password']
			isadmin = False
			if request.form.get("is_admin"):
				isadmin = True

			new_user = Users(user_email, username, password, isadmin)
			temp_user = search_users_username(username)
			if temp_user:
				error_statement = "This User Id already exists."
				return render_template("add_user.html", error_statement=error_statement, user_email=email, username=username, 
										password=password, is_admin=isadmin)
			add_new_user(new_user)
			return redirect('/admin_panel')
		else:
			return render_template("add_user.html")
	else:
		return redirect(url_for('index'))

@app.route('/update_user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def update_user(user_id):
	if current_user.is_admin:
		user_to_update = search_users_id(user_id)
		if request.method == "GET":
			return render_template("update_user.html", user_to_update=user_to_update)
		else:
			isadmin = False
			if request.form.get("is_admin"):
				isadmin = True
			updated_user = Users(user_to_update[1], user_to_update[2], user_to_update[3], isadmin)
			update_users(user_id, updated_user)
			return redirect("/admin_panel")
	else:
		return redirect(url_for('index'))


@app.route('/add_donor', methods=['POST', 'GET'])
@login_required
def add_donor():
	if request.method == "POST":
		donor_id = request.form['donorid']
		donor_name = request.form['name']
		donor_surname = request.form['surname']
		donor_phone_number = request.form['phonenumber']
		donor_birth_date = request.form['birthdate']
		donor_blood_type = request.form['bloodtype']
		donor_address = request.form['address']
		last_donate_date = 'Has Not donated Yet'
		new_donor = Donors(donor_id, donor_name, donor_surname, donor_phone_number, donor_birth_date, donor_blood_type, donor_address, last_donate_date)

		temp_donor = search_donors(donor_id)
		if temp_donor:
			error_statement = "This Donors Id already exists."
			return render_template("add_donor.html", error_statement=error_statement, donorid=donor_id, 
									name=donor_name, surname=donor_surname, phonenumber=donor_phone_number, 
									birthdate=donor_birth_date, bloodtype=donor_blood_type, address=donor_address)
		add_new_donor(new_donor)
		return redirect('/list_donors')

	else:
		return render_template("add_donor.html")

@app.route('/add_patient', methods=['POST', 'GET'])
@login_required
def add_patient():
	if request.method == "POST":
		patiend_id = request.form['patientid']
		patient_name = request.form['name']
		patient_surname = request.form['surname']
		patient_phone_number = request.form['phonenumber']
		patient_birth_date = request.form['birthdate']
		patient_blood_type = request.form['bloodtype']
		patient_address = request.form['address']
		new_patient = Patients(patiend_id, patient_name, patient_surname, patient_phone_number, patient_birth_date, patient_blood_type, patient_address)

		temp_patient = search_patients(patiend_id)
		if temp_patient:
			error_statement = "This Patient Id already exists."
			return render_template("add_patient.html", error_statement=error_statement, patientid=patiend_id, 
									name=patient_name, surname=patient_surname, phonenumber=patient_phone_number, 
									birthdate=patient_birth_date, bloodtype=patient_blood_type, address=patient_address)

		add_new_patient(new_patient)
		return redirect('/list_patients')
	else:
		return render_template("add_patient.html")

@app.route('/add_bloodbag', methods=['POST', 'GET'])
@login_required
def add_bloodbag():
	if request.method == "POST":
		donor_id = request.form['donorid']
		patiend_id = request.form['patientid']
		temp_donor = search_donors(donor_id)
		if temp_donor:
			last_donate_datetime = ((datetime.now()))
			last_donate_date = last_donate_datetime.strftime("%Y-%m-%d")
			donated_donor = Donors(temp_donor[0], temp_donor[1], temp_donor[2], temp_donor[3], temp_donor[4], temp_donor[5], temp_donor[6], last_donate_date)
			update_donors(temp_donor[0], donated_donor)
			bloodbag_bloodtype = temp_donor[5]
			dateTimeObj = datetime.now()
			bloodbag_id = dateTimeObj.strftime("%Y%m%d%H%M%S")
			expiration_datetime = ((datetime.now() + timedelta(42)))
			expiration_date = expiration_datetime.strftime("%Y-%m-%d")
			if patiend_id:
				new_bloodbag = Bloodbags(bloodbag_id, bloodbag_bloodtype, donor_id, patiend_id, expiration_date)
				temp_patient = search_patients(patiend_id)
				if temp_patient:
					if temp_donor[5] == temp_patient[5]:				
						add_new_bloodbag(new_bloodbag)
						return redirect('/list_bloodbags')
					else:
						error_statement = "Donor Blood Type"+temp_donor[5]+" and Patient Blood Type"+temp_patient[5]+" does not match."
						return render_template("add_bloodbag.html", error_statement=error_statement, donorid=donor_id, patientid=patiend_id)
			elif not patiend_id:
				new_bloodbag = Bloodbags(bloodbag_id, bloodbag_bloodtype, donor_id, None, expiration_date)
				add_new_bloodbag(new_bloodbag)
				return redirect('/list_bloodbags')
			else:
				error_statement = "This patient does not exists."
				return render_template("add_bloodbag.html", error_statement=error_statement, donorid=donor_id, patientid=patiend_id)
		else:
			error_statement = "This donor does not exists."
			return render_template("add_bloodbag.html", error_statement=error_statement, donorid=donor_id, patientid=patiend_id)
	else:
		return render_template("add_bloodbag.html")



@app.route('/update_donor/<int:donor_id>', methods=['POST', 'GET'])
@login_required
def update_donor(donor_id):
	donor_to_update = search_donors(donor_id)
	if request.method == "GET":
		return render_template("update_donor.html", donor_to_update=donor_to_update)
	else:
		donor_id = request.form['donorid']
		donor_name = request.form['name']
		donor_surname = request.form['surname']
		donor_phone_number = request.form['phonenumber']
		donor_birth_date = request.form['birthdate']
		donor_blood_type = request.form['bloodtype']
		donor_address = request.form['address']
		updated_donor = Donors(donor_id, donor_name, donor_surname, donor_phone_number, donor_birth_date, donor_blood_type, donor_address, donor_to_update[7] )
		update_donors(donor_id, updated_donor)
		return redirect("/list_donors")

@app.route('/update_patient/<int:patient_id>', methods=['POST', 'GET'])
@login_required
def update_patient(patient_id):
	patient_to_update = search_patients(patient_id)
	if request.method == "GET":
		return render_template("update_patient.html", patient_to_update=patient_to_update)
	else:
		patient_id = request.form['patientid']
		patient_name = request.form['name']
		patient_surname = request.form['surname']
		patient_phone_number = request.form['phonenumber']
		patient_birth_date = request.form['birthdate']
		patient_blood_type = request.form['bloodtype']
		patient_address = request.form['address']
		updated_patient = Patients(patient_id, patient_name, patient_surname, patient_phone_number, patient_birth_date, patient_blood_type, patient_address)
		update_patients(patient_id, updated_patient)
		return redirect("/list_patients")


@app.route('/update_bloodbag/<int:bloodbag_id>', methods=['POST', 'GET'])
@login_required
def update_bloodbag(bloodbag_id):
	bloodbag_to_update = search_bloodbags(bloodbag_id)
	if request.method == "GET":
		return render_template("update_bloodbag.html", bloodbag_to_update=bloodbag_to_update)
	else:
		patient_id = request.form['patientid']
		patient_to_receive = search_patients(patient_id)
		if patient_to_receive[5] == bloodbag_to_update[1]:
			updated_bloodbag = Bloodbags(bloodbag_to_update[0], bloodbag_to_update[1], bloodbag_to_update[2], patient_id, bloodbag_to_update[4])
			update_bloodbags(bloodbag_to_update[0], updated_bloodbag)
			return redirect("/list_bloodbags")
		else:
			error_statement = "Bloodbag Blood Type"+bloodbag_to_update[1]+" and Patient Blood Type"+patient_to_receive[5]+" does not match."
			return render_template("update_bloodbag.html", error_statement=error_statement, bloodbag_to_update=bloodbag_to_update)


@app.route('/delete_donor/<int:donor_id>')
@login_required
def delete_donor(donor_id):
	donor_to_delete = search_donors(donor_id)
	delete_donors(donor_to_delete[0])
	return redirect('/list_donors')

@app.route('/delete_patient/<int:patiend_id>')
@login_required
def delete_patient(patiend_id):
	patient_to_delete = search_patients(patiend_id)
	delete_patients(patient_to_delete[0])
	return redirect('/list_patients')



@app.route('/list_donors')
@login_required
def list_donors():
	donors = get_donors()
	return render_template("list_donors.html", donors=donors)

@app.route('/list_patients')
@login_required
def list_patients():
	patients = get_patients()
	return render_template("list_patients.html", patients=patients)

@app.route('/list_bloodbags')
@login_required
def list_bloodbags():
	bloodbags = get_bloodbags()
	return render_template("list_bloodbags.html", bloodbags=bloodbags)
		


if __name__ == "__main__":
    app.run()