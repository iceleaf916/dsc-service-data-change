#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2013 Deepin, Inc.
#               2011~2013 Kaisheng Ye
#
# Author:     Kaisheng Ye <kaisheng.ye@gmail.com>
# Maintainer: Kaisheng Ye <kaisheng.ye@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import peewee

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
db_dir = os.path.join(root_path, "data/software")

def get_support_languages():
    lauanges = []
    for d in os.listdir(db_dir):
        db_path = os.path.join(db_dir, d, "software.db")
        if os.path.exists(db_path):
            lauanges.append(d)
    return lauanges

class Software(peewee.Model):
    pkg_name = peewee.CharField()
    alias_name = peewee.CharField()
    short_desc = peewee.CharField()
    long_desc = peewee.TextField()

    @classmethod
    def init_language(cls, lang):
        support_languages = get_support_languages()
        if lang in support_languages:
            db_path = os.path.join(db_dir, lang, "software.db")
            software_db = peewee.SqliteDatabase(db_path, autocommit=False)
            cls._meta.database = software_db
            return software_db
        else:
            return None

if __name__ == "__main__":
    lang = "en_US"
    if Software.init_language(lang):
        print Software.select().count()
    else:
        print "No data for lang:", lang
