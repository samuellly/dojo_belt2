from django.shortcuts import render, redirect, reverse
from .models import User, Appointment
from datetime import datetime
from django.contrib import messages

def validation(request):
	if request.method == 'POST':
		return process_validation(request)
	return render(request, 'belt2_app/validation.html')

def process_validation(request):
	results = User.objects.UserValidation(request.POST)

	if results[0]: # success
		request.session['id'] = results[2].id
		request.session['name'] = results[2].name
		return redirect(reverse('belt2:index'))

	for error in results[1]: # error
			messages.error(request, error)
	return redirect(reverse('belt2:validation'))

def index(request):
	if 'id' not in request.session:
		return redirect(reverse('belt2:validation'))

	if request.method == 'POST':
		return create(request)

	context = {
		'apts': Appointment.objects.filter(user=request.session['id']).order_by('time'),
		'today': datetime.now().date(),
		'done': 'Done'
	}
	return render(request, 'belt2_app/index.html', context)

def create(request):
	results = Appointment.objects.AppointmentValidation(request.POST, request.session['id'])
	print results
	if not results[0]: # if errors
		for error in results[1]:
			messages.error(request, error)
	return redirect(reverse('belt2:index'))

def show(request, id):
	if 'id' not in request.session:
		return redirect(reverse('belt2:validation'))

	if request.method == 'POST':
		return update(request, id)

	context = {
		'apt': Appointment.objects.get(id=id)
	}
	return render(request, 'belt2_app/edit.html', context)

def update(request, id):

	results = Appointment.objects.UpdateAppointment(request.POST, id, request.session['id'])

	if not results[0]: # if errors
		for error in results[1]:
			messages.error(request, error)
		return redirect(reverse('belt2:show', kwargs={'id':id}))

	return redirect(reverse('belt2:index'))

def destroy(request, id):
	Appointment.objects.get(id=id).delete()
	return redirect(reverse('belt2:index'))

def logout(request):
	for key in request.session.keys():
		del request.session[key]
	return redirect(reverse('belt2:validation'))
