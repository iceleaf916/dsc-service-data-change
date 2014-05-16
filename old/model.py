#!/usr/bin/env python
# coding: utf-8

import os
import json
import urllib

DATA_PATH = "../deepin-software-center-service-private/dsc-software-data/input_data"
PKG_INFO = os.path.join(DATA_PATH, "pkg_description")

class NewObject(object):
    def __init__(self, args):
        for key in args:
            setattr(self, key, args[key])

def get_package_info(data):
    language = data["language"]
    package = data["package"]
    path = os.path.join(PKG_INFO, language, package)
    info_dict = {}
    if os.path.exists(path):
        info = json.load(open(path))
        info_dict['package'] = package
        info_dict["alias"] = info["alias"] if info["alias"]!="" else package
        info_dict["short_desc"] = info["short_desc"] if info["short_desc"]!="" else package
        info_dict["long_desc"] = info["long_desc"] if info["long_desc"]!="" else package
        info_dict["language"] = language
        info_dict['exists'] = True
    else:
        info_dict['package'] = package
        info_dict['language'] = language
        info_dict['exists'] = False
    return NewObject(info_dict)

def touch_file(package, language):
    path = os.path.join(PKG_INFO, language, package)
    fp = open(path, "w")
    js = {}
    js["alias"] = ""
    js["short_desc"] = ""
    js["long_desc"] = ""
    json.dump(js, fp)
    fp.close()

def create_new_description(data):
    result_info = {
            "package": data["package"],
            "language": data["language"],
            "successful": False,
            "info": "",
            }
    try:
        touch_file(data["package"], data["language"])
        result_info["successful"] = True
        result_info["info"] = " "
    except Exception, e:
        result_info["successful"] = False
        result_info["info"] = "%s新的信息创建失败: %s" % (data["package"], e)
    return NewObject(result_info)

def modify_description(data):
    path = os.path.join(PKG_INFO, data["language"], data["package"])
    js = {}
    js["alias"] = urllib.unquote(data["alias"]).replace("+", " ")
    js["short_desc"] = urllib.unquote(data["short_desc"]).replace("+", " ")
    js["long_desc"] = urllib.unquote(data["long_desc"]).replace("+", " ")
    result_info = {}
    if os.path.exists(path):
        old_info = open(path).read()
        try:
            fp = open(path, "w")
            json.dump(js, fp)
            fp.close()
            result_info["successful"] = True
            result_info["info"] = "信息修改成功"
        except Exception, e:
            os.remove(path)
            fp = open(path, "w")
            fp.write(old_info)
            fp.close()
            result_info["successful"] = False
            result_info["info"] = "信息修改失败: %s" % e
    else:
        try:
            fp = open(path, "w")
            json.dump(js, fp)
            fp.close()
            result_info["successful"] = True
            result_info["info"] = "信息修改成功"
        except Exception, e:
            os.remove(path)
            result_info["successful"] = False
            result_info["info"] = "信息修改失败: %s" % e
    return NewObject(result_info)
