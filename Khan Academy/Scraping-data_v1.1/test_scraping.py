import webapp2
import cgi
import jinja2
import os
from gaesessions import get_current_session

import urllib
import re
from operator import itemgetter, attrgetter
import json
import types


##################################################################################
def creat_user_projects_scratch_link(user_id):
    return "https://www.khanacademy.org/api/labs/user/scratchpads?username="+user_id

def load_page(tutorial_link):
    htmltext = urllib.urlopen(tutorial_link).read()
    data = json.loads(htmltext)
    return data

def isNull(data):
    if(data):
        return data
    else:
        if (type(data) is types.IntType):
            return 0
        else:
           return "N/A" 

def get_all_data(user_id):
    data = load_page(creat_user_projects_scratch_link(user_id))["scratchpads"]
    li = [[]] * len(data)
    for i in range(len(data)):
        li[i]= (isNull(data[i]["title"]),isNull(data[i]["url"]))
    li.sort(key=itemgetter(0), reverse = True)
    return li
	
def get_user_prject(user_id):
    return get_all_data(user_id)


##################################################################################################

class MainPage(webapp2.RequestHandler):

    def get(self):
        session = get_current_session()
        user_id = session.get('user_id','')
        message = session.get('message','')
        jinja_environment = jinja2.Environment(autoescape = True,
                                               loader = jinja2.FileSystemLoader(os.path.join(
                                                   os.path.dirname(__file__), 'templates')))
        tpl_vars = {'message': message,'user_id': user_id}
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(tpl_vars))

class user_detial(webapp2.RequestHandler):

    def post(self):
        user_id = self.request.get('user_id')
        session = get_current_session()
	session['user_id'] = user_id
	session['message'] = ''
        if len(user_id)<1:
            session['message'] = 'Empty!'
            self.redirect('/')
        #self.response.write(user_id)
        results = get_user_prject(user_id)
        self.response.write('<h2>user id: ' + user_id+'</h2>')
        self.response.write('<table border="0">')
        self.response.write('<tr><th>project_id</th><th>project_link</th></tr>')
        for i in range(len(results)):
            self.response.write('<tr>')
            for j in range(2):
                self.response.write('<td>')
                self.response.write(results[i][j])
                self.response.write('</td>')
            self.response.write('</tr>')
        self.response.write('</table>')
	#self.response.write(results)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/userDetial', user_detial),
], debug=True)
