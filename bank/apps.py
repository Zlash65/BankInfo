# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class BankConfig(AppConfig):
	name = 'bank'
	ready_has_run = False

	def ready(self):
		if self.ready_has_run:
			return
		
		# this code is run on the very first start of server
		if db_table_exists("bank_bank"):
			from bank.models import Bank
			if not len(Bank.objects.all()):
				print("Setting up database")
				# dump_bank_data()
				dump_bank_data_to_mongo()
				create_dummy_users()

		self.ready_has_run = True

def db_table_exists(table_name):
	''' check if the tables are already created or not '''
	from django.db import connection
	return table_name in connection.introspection.table_names()

def dump_bank_data_to_mongo():
	import sys
	import pandas as pd
	from bank.models import Bank

	url = "https://raw.githubusercontent.com/snarayanank2/indian_banks/master/bank_branches.csv"
	bank_data = pd.read_csv(url)
	records = bank_data.to_dict(orient='records')

	# add entries to database in batches
	total = int(len(records)/50) + 1
	for i in range(0, 51):
		sys.stdout.write('Setting up database for Banks [%s%s]\r' % ("="*(i+1), " "*(50-(i+1))))
		sys.stdout.flush()

		entries = []
		for row in records[(i*total):((i+1)*total)]:
			entries.append(Bank(**row))

		# bulk insert batch entries
		Bank.objects.bulk_create(entries)

def dump_bank_data():
	import csv, sys
	from bank.models import Bank

	url = "https://raw.githubusercontent.com/snarayanank2/indian_banks/master/bank_branches.csv"

	try:
		import urllib2
		response = urllib2.urlopen(url)
		csv_reader = list(csv.reader(response, delimiter=str(',').encode('utf-8')))[1:]
	except ImportError:
		import urllib.request as urllib
		response = urllib.urlopen(url)

		csv_reader = response.read().decode('utf-8')
		csv_reader = list(csv.reader(csv_reader.splitlines()))[1:]

	# slice first row as it stores headers
	line_count, total = 0, len(list(csv_reader))/50

	for row in csv_reader:

		# show progress bar
		start = int(line_count / total)
		line_count += 1
		sys.stdout.write('Setting up database for Banks [%s%s]\r' % ("="*(start+1), " "*(50-start)))
		sys.stdout.flush()

		bank_detail = Bank()
		bank_detail.ifsc = row[0]
		bank_detail.bank_id = row[1]
		bank_detail.branch = row[2]
		bank_detail.address = row[3]
		bank_detail.city = row[4]
		bank_detail.district = row[5]
		bank_detail.state = row[6]
		bank_detail.bank_name = row[7]

		try:
			bank_detail.save()
		except Exception as e:
			print(e)
			# pass

def create_dummy_users():
	''' creates 1 superuser '''

	from django.contrib.auth.models import User

	try:
		User.objects.create_user(username="allen",
			password="asdf1234", is_superuser=1, is_staff=1)
	except Exception as e:
		print(e)
