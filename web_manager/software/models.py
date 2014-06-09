#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from language.models import Language

class Software(models.Model):
    pkg_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.pkg_name

    class Meta:
        verbose_name = u'软件描述信息'
        verbose_name_plural = verbose_name

class SoftwareL10n(models.Model):
    alias_name = models.CharField(max_length=255, blank=True, verbose_name=u'别名')
    short_desc = models.CharField(max_length=255, blank=True, verbose_name=u'短描述')
    long_desc = models.TextField(blank=True, verbose_name=u'长描述')
    software = models.ForeignKey(Software, verbose_name=u'软件包')
    language_code = models.ForeignKey(Language, verbose_name=u'语言')

    def __unicode__(self):
        return "%s [%s]" % (self.alias_name, self.language_code)

    class Meta:
        verbose_name = u'软件描述信息国际化'
        verbose_name_plural = verbose_name
