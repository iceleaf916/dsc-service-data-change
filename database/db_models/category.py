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
db_path = os.path.join(root_path, "data/category/new_category.db")

category_db = peewee.SqliteDatabase(db_path, autocommit=False)

class FirstCategory(peewee.Model):
    name = peewee.CharField()
    order = peewee.IntegerField(default=0)

    class Meta:
        database = category_db

class SecondCategory(peewee.Model):
    name = peewee.CharField()
    order = peewee.IntegerField(default=0)
    first_category = peewee.ForeignKeyField(FirstCategory, related_name="first_category")

    class Meta:
        database = category_db

if __name__ == "__main__":
    print FirstCategory.select().count()
    print SecondCategory.select().count()
