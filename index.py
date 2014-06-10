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

from flask import Flask
from flask import g
from flask import request
from flask import url_for, abort, render_template, flash

from database.db_models.software import Software
from database.db_models.software import Language as SoftwareLanguage
from database.db_models.category import FirstCategory, SecondCategory

from database.db_models.desktop import Package


app = Flask(__name__)

def get_language_obj(code):
    try:
        language_obj = SoftwareLanguage.select().where(SoftwareLanguage.language_code == code).get()
    except:
        language_obj = SoftwareLanguage(language_code=code, alias_name=code)
        language_obj.save()
    return language_obj

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/software/", methods=['GET'])
def software_search():
    result_list = []
    key = ""
    if request.method == 'GET':
        key = request.args.get('s', '')
        if key:
            search_key = "*%s*" % key
            software_list = Software.select().where(Software.pkg_name % search_key)
            for software in software_list:
                pkg_name = software.pkg_name
                if not (pkg_name in result_list or pkg_name.endswith(":i386")):
                    result_list.append(pkg_name)

    return render_template("software/search_page.html", result_list=result_list, key=key)

@app.route("/software/<pkg_name>/")
def software_details(pkg_name):
    software_list = []
    for lang in SoftwareLanguage.select():
        try:
            soft_obj = Software.select().where(Software.pkg_name == pkg_name, Software.language==lang).get()
            soft_dict = {
                    "language": lang.language_code,
                    "alias_name": soft_obj.alias_name,
                    "short_desc": soft_obj.short_desc,
                    "long_desc": soft_obj.long_desc,
                    }
        except:
            soft_dict = {
                    "language": lang.language_code,
                    "alias_name": "",
                    "short_desc": "",
                    "long_desc": "",
                    }
        software_list.append(soft_dict)

    return render_template("software/detail_edit.html", pkg_name=pkg_name, software_list=software_list)

@app.route("/software/<pkg_name>/edit/", methods=['GET', 'POST'])
def software_edit(pkg_name):
    if request.method == "POST":
        alias_name = request.form['alias_name']
        short_desc = request.form['short_desc']
        long_desc = request.form['long_desc']
        language = request.form['language']
        language_obj = get_language_obj(language)

        try:
            software_obj = Software.select().where(Software.language==language_obj, Software.pkg_name==pkg_name).get()
            software_obj.alias_name = alias_name
            software_obj.short_desc = short_desc
            software_obj.long_desc = long_desc
            software_obj.save()
        except:
            software_obj = Software(pkg_name=pkg_name, language=language_obj, alias_name=alias_name, short_desc=short_desc, long_desc=long_desc)
            software_obj.save()

        return render_template("software/edit_result.html", success=True, pkg_name=pkg_name)
    else:
        return render_template("software/edit_result.html", success=False, pkg_name=pkg_name)

@app.route("/desktop/", methods=['GET'])
def desktop_search():
    result_list = []
    key = ""
    if request.method == 'GET':
        key = request.args.get('s', '')
        if key:
            search_key = "*%s*" % key
            package_list = Package.select().where(Package.pkg_name % search_key)
            for package in package_list:
                pkg_name = package.pkg_name
                if not (pkg_name in result_list or pkg_name.endswith(":i386")):
                    result_list.append(pkg_name)

    return render_template("desktop/search_page.html", result_list=result_list, key=key)

@app.route("/desktop/<pkg_name>/", methods=['GET'])
def desktop_details(pkg_name):
    try:
        package_obj = Package.select().where(Package.pkg_name==pkg_name).get()
        print package_obj.first_category_name
    except:
        pass
    return "OK"

@app.route("/desktop/<pkg_name>/edit/", methods=['GET', 'POST'])
def desktop_edit():
    pass

@app.route("/category/")
def category():
    category_list = FirstCategory.select()
    return render_template("category/category.html", category_list=category_list)

@app.route("/category/<first_category_name>/")
def category_first(first_category_name):
    category_list = []
    try:
        first_obj = FirstCategory.select().where(FirstCategory.name==first_category_name).get()
    except:
        pass
    category_list = SecondCategory.select().where(SecondCategory.first_category==first_obj)
    return render_template("category/category_first.html", category_list=category_list, first_category=first_obj)

@app.route("/category/edit/", methods=["GET", "POST"])
def category_edit():
    if request.method == "POST":
        category_type = request.form['type']
        name = request.form['name']
        alias_name = request.form['alias_name']
        if category_type == "first_category":
            try:
                category_obj = FirstCategory.select().where(FirstCategory.name==name).get()
                category_obj.alias_name = alias_name
                category_obj.save()
                return "OK"
            except:
                return "Failed"
        elif category_type == "second_category":
            try:
                category_obj = SecondCategory.select().where(SecondCategory.name==name).get()
                category_obj.alias_name = alias_name
                category_obj.save()
                return "OK"
            except:
                return "Failed"
        else:
            return "Failed"

if __name__ == "__main__":
    app.run(debug=True)
