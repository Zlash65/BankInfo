# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Bank(models.Model):
	''' Bank model '''
	ifsc = models.CharField(max_length=20, primary_key=True)
	bank_id = models.IntegerField(default=0)
	branch = models.CharField(max_length=30)
	address = models.CharField(max_length=150)
	city = models.CharField(max_length=30)
	district = models.CharField(max_length=30)
	state = models.CharField(max_length=30)
	bank_name = models.CharField(max_length=50)
