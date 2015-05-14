import webapp2
import jinja2
import os
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
 autoescape=False)

COMMENT_FROM_PEOPLE_TABLE_NAME = 'comment_from_people_table_name'

def commentFromPeople_key():
    return ndb.Key('comment_from_people', COMMENT_FROM_PEOPLE_TABLE_NAME)

concepts=[
["Servers",
"A server is a piece of software which is designed to processing requests "
"from the clients. Theoretically servers could be run on any computer, but "
"in most cases they are running on the specially designed mainframes, "
"because a normal laptop or desktop is neither strong enough for nor good"
" at handeling millions of requests from other computers."],
["Protocol",
"Protocols are a set of rules, which are agreed by all people, for the "
"entities to communicate with each other."],
["HTTP",
"The protocol which is used on the web is the HTTP, which stands for "
"Hypertext Transfer Protocol. Basically if the client (for example, the "
"browser) need the server to do a particular job, it must send the "
"corresponding request following the rules in HTTP, otherwise the server "
"will not understand the intention of the client. HTTP is a simple "
"protocol. There are two main messages, which are GET and POST. "
"Basically, GET message is for the user to get some stuff (for "
"instance: text, images etc.) from the server, while POST message for "
"clients to change the data on the server (for instance: a user of "
"facebook just moved to a new city and wanna update his/her current "
"location). Although it is possible to make modification on the server "
"side when receiving a GET message, it is never a good idea to do this"
" because such violations of rules can bring magic (and undesirable in "
"most cases) consequences."],
["Validation",
"The message from the user could be incorrect or completely junk. Such kind"
" of things could happen because the user could make a mistake or there "
"maybe a problem of hardware somewhere on the path from the client to the "
"server, let alone the malicious, on-purpose attack. If we handle the "
"messages from the client without checking, it will look normal if the "
"messages happen to be OK. When they are not OK, then the result could be "
"problematic and beyond. For example, the web page may behave weirdly, "
"which could give the user a terrible experience and hence make them never "
"visit the web page again. The result could even be disastrous when the "
"message cause a unwanted modification on the data on the server side."
"Sometimes the user may input some raw HTML code, which could severely "
"disturb how we display the content. In this case, we need to escape the "
"characters which could lead to such kind of result."],
["HTML Templates",
"Template generally refer to a library which is used to build complicated "
"strings. And the template we are talking here is one used to generate "
"HTML code. Template like jinja2 have a feature called statement syntax "
"which enable us to write pieces of Python-like code in HTML file, which "
"means we can have for loop and if statement in our HTML file, which can "
"largely reduce repetition."]
]


class ExtraResource(ndb.Model):
    # for the comment submitted by user
    catagory = ndb.StringProperty(indexed=False)
    message = ndb.StringProperty(indexed=False)
    link = ndb.StringProperty(indexed=False)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
      self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
      t = jinja_env.get_template(template)
      return t.render(params)

    def render(self, template, **kw):
      self.write(self.render_str(template, **kw))

class MainPage(Handler):

  def render_front(self, error='', catagory='', link=''):
    comments_query = ExtraResource.query()
    comments = comments_query.fetch()
    self.render("note_template.html", concepts=concepts, 
      comments_from_user=comments, error=error, 
      catagory=catagory, link=link)

  def get(self):
    self.render_front()
    

  def post(self):
    messageFromUser = self.request.get("message")
    if messageFromUser:
      # valid input
      # store the data in datastore
      resourceFromUser = ExtraResource(parent=commentFromPeople_key())
      resourceFromUser.catagory = self.request.get("catagory")
      resourceFromUser.message = messageFromUser
      resourceFromUser.link = self.request.get("link")
      resourceFromUser.put()
      self.redirect('/')
    else:
      error = "the comment cannot be empty"
      self.render_front(error=error, catagory=self.request.get("catagory"),
       link=self.request.get("link"))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)