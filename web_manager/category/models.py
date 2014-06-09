#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from language.models import Language

class Firstcategory(models.Model):
    id_name = models.CharField(max_length=255, verbose_name=u'名称ID')
    alias_name = models.CharField(max_length=255, verbose_name=u"显示名称")
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.alias_name

    class Meta:
        verbose_name = u"一级分类"
        verbose_name_plural = verbose_name

class FirstcategoryL10n(models.Model):
    alias_name = models.CharField(max_length=255, verbose_name=u'别名')
    first_category = models.ForeignKey(Firstcategory, verbose_name=u'一级分类')
    language_code = models.ForeignKey(Language, verbose_name=u"语言")

    def __unicode__(self):
        return "%s [%s]" % (self.alias_name, self.language_code)

    class Meta:
        verbose_name = u"一级分类国际化"
        verbose_name_plural = verbose_name

class Secondcategory(models.Model):
    id_name = models.CharField(max_length=255, verbose_name=u'名称ID')
    alias_name = models.CharField(max_length=255, verbose_name=u"显示名称")
    order = models.IntegerField(default=0)
    first_category = models.ForeignKey("Firstcategory", verbose_name=u'一级分类')

    def __unicode__(self):
        return self.alias_name

    class Meta:
        verbose_name = u"二级分类"
        verbose_name_plural = verbose_name

class SecondcategoryL10n(models.Model):
    alias_name = models.CharField(max_length=255, verbose_name=u'别名')
    second_category= models.ForeignKey(Secondcategory, verbose_name=u'名称ID')
    language_code = models.ForeignKey(Language, verbose_name=u"语言")

    def __unicode__(self):
        return "%s [%s]" % (self.alias_name, self.language_code)

    class Meta:
        verbose_name = u"二级分类国际化"
        verbose_name_plural = verbose_name
