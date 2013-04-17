#!/usr/bin/env python
# coding: utf-8

import web
import model

urls = (
    '/', 'Home',
    '/(.*)/', 'Redirect',
    '/description', 'DescriptionIndex',
    '/description/search', 'Search',
    '/description/modify', 'ModifyDesc',
    '/description/create', 'CreateNewDesc',
)

render = web.template.render('templates/')

def get_post_data():
    return_dict = {}
    data = web.data().split("&")
    for d in data:
        _d = d.split("=")
        return_dict[_d[0]] = _d[1]
    return return_dict

class Redirect:
    def GET(self, path):
        web.seeother('/' + path)
        
class Home:
    def GET(self):
        web.seeother('/description')

class DescriptionIndex:
    def GET(self):
        """ Show page """
        return render.index(None, None, None)

class Search:
    
    def POST(self):
        post_data = get_post_data()
        package = post_data["package"]
        if not package:
            return 

        package_info = model.get_package_info(post_data)
        if package_info.exists:
            return render.index(package_info, None, None)
        else:
            return render.index(None, package_info, None)

class ModifyDesc:
    
    def POST(self):
        post_data = get_post_data()
        result_info = model.modify_description(post_data)
        if result_info.successful:
            return render.index(model.get_package_info(post_data), None, result_info)
        else:
            return render.index(model.get_package_info(post_data), None, result_info)

class CreateNewDesc:

    def POST(self):
        post_data = get_post_data()
        result_info = model.create_new_description(post_data)
        if result_info.successful:
            data = {'package': result_info.package, 'language': result_info.language}
            package_info = model.get_package_info(data)
            return render.index(package_info, None, None)
        else:
            return render.index(None, None, result_info)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
