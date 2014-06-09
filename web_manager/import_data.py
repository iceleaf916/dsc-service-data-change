#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_manager.settings")

import sys
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0,  os.path.join(root_dir, "database"))
from db_models.software import Software as SoftwareData

from language.models import Language
from software.models import Software, SoftwareL10n

def get_languages():
    langs = []
    for i in Language.objects.all():
        langs.append(i)

    return langs

def insert_description(lang):
    if not SoftwareData.init_language(lang.lang_code):
        print "No data for lang:", lang
    else:
        print "\ntotal for %s: %s" % (lang.lang_code, SoftwareData.select().count())
        i = 0
        for s in SoftwareData.select():
            try:
                software_obj = Software.objects.get(pkg_name=s.pkg_name)
            except:
                software_obj = Software(pkg_name=s.pkg_name)
                software_obj.save()

            try:
                l10n_obj = SoftwareL10n.objects.get(software=software_obj, language_code=lang)
            except:
                l10n_obj = SoftwareL10n(software=software_obj, language_code=lang, alias_name=s.alias_name, short_desc=s.short_desc, long_desc=s.long_desc)
                l10n_obj.save()

            i += 1
            print "\rProgress: %s" % i,

if __name__ == "__main__":
    for l in get_languages():
        if l.lang_code != "en_US":
            insert_description(l)
