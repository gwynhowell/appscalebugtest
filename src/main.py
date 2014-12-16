from google.appengine.ext import ndb
import webapp2


class A(ndb.Model):
    name = ndb.StringProperty()
  
class B(ndb.Model):
    name = ndb.StringProperty()
  
class C(ndb.Model):
    name = ndb.StringProperty()

def create_data(i):
    a = A(name='A%s'%i).put()
    
    b1 = B(parent=a, name='A%s-B1'%i)
    b2 = B(parent=a, name='A%s-B2'%i)
    b3 = B(parent=a, name='A%s-B3'%i)
    b4 = B(parent=a, name='A%s-B4'%i)
    b5 = B(parent=a, name='A%s-B5'%i)
    
    bs = [b1, b2, b3, b4, b5]
    
    ndb.put_multi(bs)
    
    for b in bs:
        for i in range(10):
            name = '%s-C%s' % (b.name, i)
            C(parent=b.key, name=name).put()

class Page(webapp2.RequestHandler):
    def get(self):
        a = A.query().get()
        if not a:
            create_data(1)
        
        test1 = C.query(ancestor = a.key).fetch(limit=100)
        test2 = C.query(ancestor = a.key).order(C.name).fetch(limit=100)
        
        html = '<div style="display: inline-block; width: 50%">'
        html += '<h4>Test 1: C.query(ancestor = a).fetch(limit=100)</h4>'
        html += '<div>Results = %s</div>' % len(test1)
        html += ''.join(['<li>%s</li>' % result.name for result in test1])
        html += '</div>'
        
        
        html += '<div style="display: inline-block; width: 50%">'
        html += '<h4>Test 2: C.query(ancestor = a.key).order(C.name).fetch(limit=100)</h4>'
        html += '<div>Results = %s</div>' % len(test2)
        html += ''.join(['<li>%s</li>' % result.name for result in test2])
        html += '</div>'
        
        self.response.out.write(html)

app = webapp2.WSGIApplication([
  ('/', Page)
])
