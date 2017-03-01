from __future__ import unicode_literals
import re
from django.db import models
from django.contrib import messages
import bcrypt
from datetime import datetime

# Create your models here.
class ValidationManager(models.Manager):
	def UserValidation(self, form_info):
# REGISTRATION VALIDATION
		errors = []
		if 'password2' in form_info:
			EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
			name = form_info['name']
			email = form_info['email']
			password1 = form_info['password1']
			password2 = form_info['password2']
			dob = form_info['dob']

			if len(email)<1:
				errors.append('No email entered')
			elif not EMAIL_REGEX.match(email):
				errors.append('Not a valid email.')
			elif User.objects.filter(email=email):
				errors.append('Email already in use.')

			if len(str(dob.encode()))<1:
				errors.append('You forgot to add a date')
			if dob:
				dob = datetime.strptime(dob, "%Y-%m-%d")
				if dob.date() >= datetime.now().date():
					errors.append('Date is in the future.')

			if len(name) < 3:
				errors.append('Name is not valid.')

			if password1 != password2:
				errors.append('Passwords do not match.')
			elif len(password1)<8:
				errors.append('Not a valid password. Must be 8 characters.')

			if len(errors) > 0:
				return (False, errors)
			else:
				password = str(password1)
				hashed = bcrypt.hashpw(password, bcrypt.gensalt())
				User.objects.create(name=name, email=email, password=hashed, dob=dob)
				user = User.objects.get(email=email)

				return (True, errors, user)
		else:
# LOGIN VALIDATION
			email = form_info['email']
			password = form_info['password']
			if len(User.objects.filter(email=email))<1:
				errors.append('Invalid login information.')
				return (False, errors)
			user = User.objects.get(email=email)
			password_entered = password.encode()
			hashed_entered = bcrypt.hashpw(password_entered, bcrypt.gensalt())
			if email == user.email and bcrypt.hashpw(password_entered, user.password.encode()) == user.password:
				return (True, errors, user)
			else:
				errors.append('Password incorrect.')
				return (False, errors)

	def AppointmentValidation(self, form_info, userID):
		errors = []
		date = form_info['date']
		time = form_info['time']
		task = form_info['task']

		user = User.objects.get(id=userID)

		status = 'Pending'

		if len(str(date.encode()))<1:
			errors.append('You forgot to add a date')
		if len(str(time.encode()))<1:
			errors.append('You forgot to add a time')
		if len(task) < 1:
			errors.append('You forgot to add a task')

		if date and time:
			apt = Appointment.objects.filter(date=date, time=time, user=user)
			if len(apt) > 0:
				errors.append('Already have an appointment at this time and date')
			date = datetime.strptime(date, "%Y-%m-%d")
			time = datetime.strptime(time, "%H:%M")
			if date.date() < datetime.now().date():
				errors.append('Date is in the past')
		if len(errors) > 0:
			return (False, errors)

		Appointment.objects.create(user=user, task=task, status=status, date=date.date(), time=time.time())
		return (True, errors)
	def UpdateAppointment(self, form_info, aptID, userID):
		task = form_info['task']
		status = form_info['status']
		date = form_info['date']
		time = form_info['time']
		errors = []

		apt = Appointment.objects.get(id=aptID)
		user = User.objects.get(id=userID)

		if len(str(date.encode()))<1:
			errors.append('You forgot to add a date')
		if len(str(time.encode()))<1:
			errors.append('You forgot to add a time')
		if len(task) < 1:
			errors.append('You forgot to add a task')

		if date and time:
			new_apt = Appointment.objects.filter(date=date, time=time, user=user)
			if len(new_apt) > 0:
				if apt != new_apt[0]:
					errors.append('Already have an appointment at this time and date')
			date = datetime.strptime(date, "%Y-%m-%d")
			time = datetime.strptime(time, "%H:%M")
			if date.date() < datetime.now().date():
				errors.append('Date is in the past')

		if len(errors) > 0:
			return (False, errors)


		apt.task = task
		apt.status = status
		apt.date = date.date()
		apt.time = 	time.time()
		apt.save()
		return (True, errors)

class User(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	dob = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ValidationManager()

class Appointment(models.Model):
	user = models.ForeignKey('User')
	task = models.CharField(max_length=255)
	status = models.CharField(max_length=255)
	date = models.DateField()
	time = models.TimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ValidationManager()
