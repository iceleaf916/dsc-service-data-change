""" Basic todo list using webpy 0.3 """
import web
import model

urls = (
    '/', 'Home',
    '/(.*)/', 'Redirect',
    '/description', 'DescriptionIndex',
    '/description/search', 'Search',
)

render = web.template.render('templates/')

class Redirect:
    def GET(self, path):
        web.seeother('/' + path)
        
class Home:
    def GET(self):
        web.seeother('/description')

class DescriptionIndex:
    def GET(self):
        """ Show page """
        return render.index(None, None)

class Search:
    
    def POST(self):
        language, package =  web.data().split("&")
        language = language.split("=")[1]
        package = package.split("=")[1]

        package_info = model.get_package_info(package, language)
        if package_info:
            return render.index( package_info, None)
        else:
            return render.index(None, model.get_confirm_info(package))

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
