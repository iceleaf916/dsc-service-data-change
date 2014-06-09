#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Language(models.Model):
    lang_code = models.CharField(max_length=255, unique=True, verbose_name="语言代码")
    alias_name = models.CharField(max_length=255, blank=True, verbose_name="名称",
            help_text='比如: "zh_CN"对应的的名称为"中文", "en_US"对应的名称为"English"')
    
    def __unicode__(self):
        return self.lang_code

    class Meta:
        verbose_name = u"语言模块"
        verbose_name_plural = verbose_name
