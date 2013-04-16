import os

DATA_PATH = "../data"
PKG_INFO = os.path.join(DATA_PATH, "pkg_info")

class NewObject(object):
    def __init__(self, args):
        for key in args:
            setattr(self, key, args[key])

def get_package_info(package, language):
    path = os.path.join(PKG_INFO, language, package)
    print path
    if os.path.exists(path):
        info = eval(open(path).read())
        info_dict = {}
        info_dict['package'] = package
        info_dict["alias_info"] = package
        info_dict["short_desc"] = unicode(info[1])
        info_dict["long_desc"] = unicode(info[2])
        return NewObject(info_dict)
    else:
        return None

def get_confirm_info(package):
    info_dict = {}
    info_dict["package_name"] = package
    return NewObject(info_dict)

def touch_file(package, language):
    path = os.path.join(PKG_INFO, language, package)
    fp = open(path, "w")
    fp.write(str(("", "", "")))
    fp.close()
