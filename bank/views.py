# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

max_per_page = 4

# Create your views here.
def home(request):

	select = request.GET.get('option','')

	if select == "IFSC":
		ifsc = request.GET.get('ifsc','')
		return search_by_ifsc(request, ifsc)
	else:
		bank = request.GET.get('bank','')
		city = request.GET.get('city','')
		return search_by_bank(request, bank, city)

def search_by_ifsc(request, ifsc):
	from bank.models import Bank

	branch = list(Bank.objects.filter(ifsc=ifsc))
	return render(request, 'card.html', {"branch": branch})

def search_by_bank(request, bank_name, city):
	from bank.models import Bank
	page = int(request.GET.get('page', '1'))

	branch = list(Bank.objects.filter(bank_name=bank_name).filter(city=city))
	args = get_paging_index(branch, page) if len(branch) else {}

	if not len(branch) and bank_name and city:
		args.update({"fallback": "No data to display. Please search again!"})

	return render(request, 'list.html', args)

def get_paging_index(data, page):
	''' create a paging like view '''
	start_index, end_index = ((page-1)*max_per_page), (page*max_per_page)

	args = {"last": False}
	if end_index < len(data):
		args["data"] = data[start_index:end_index]
	else:
		args["data"], args["last"] = data[start_index:end_index], True

	args["page"] = page

	return args
