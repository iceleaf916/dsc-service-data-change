# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Package(models.Model):
    pkg_name = models.CharField(max_length=255)
    display_flag = models.BooleanField(default=True)
    first_category_name = models.CharField(max_length=255)
    second_category_name = models.CharField(max_length=255)
    start_pkg_names = models.CharField(max_length=255, blank=True)

class Desktop(models.Model):
    desktop_path = models.CharField(max_length=255)
    desktop_name = models.CharField(max_length=255)
    pkg_names = models.CharField(max_length=255)
    first_category_name = models.CharField(max_length=255, blank=True)

class PackageDesktop(models.Model):
    desktop = models.ForeignKey("Desktop")
    package = models.ForeignKey("Package")

