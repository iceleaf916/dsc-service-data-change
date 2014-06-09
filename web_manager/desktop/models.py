#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from category.models import Secondcategory

class Package(models.Model):
    pkg_name = models.CharField(max_length=255, verbose_name=u"软件包名")
    display_flag = models.BooleanField(default=True, verbose_name=u"显示")
    start_pkg_names = models.CharField(max_length=255, blank=True, verbose_name=u"启动desktop所在的包",
            help_text=u"一般情况下为空，特殊情况，比如common包中包含desktop，此处要填写common包名称，多个的话，用“,”分隔")

    second_category_name = models.ForeignKey(Secondcategory, verbose_name=u'二级分类')

    def __unicode__(self):
        return "%s [%s]" % (self.pkg_name, self.second_category_name)

    class Meta:
        verbose_name = u"桌面软件包"
        verbose_name_plural = verbose_name

class Desktop(models.Model):
    desktop_path = models.CharField(max_length=255)
    desktop_name = models.CharField(max_length=255)
    pkg_names = models.CharField(max_length=255)
    first_category_name = models.CharField(max_length=255, blank=True)

class PackageDesktop(models.Model):
    desktop = models.ForeignKey("Desktop")
    package = models.ForeignKey("Package")

